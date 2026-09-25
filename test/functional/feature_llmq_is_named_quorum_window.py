#!/usr/bin/env python3
# Copyright (c) 2026 The Defcon Developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

'''
feature_llmq_is_named_quorum_window.py

A node that is not a masternode must accept an InstantSend lock signed by the
quorum that has just stopped being one of the `signingActiveQuorumCount`
newest -- in the blocks right after a new quorum's commitment is mined.

The signer chooses among the quorums that were signing-active
SIGN_HEIGHT_OFFSET blocks below its tip, so for a few blocks after a new
commitment it can still pick the oldest of the previous set. The receiver
takes the quorum the lock names only if it counts that quorum as active; with
`signingActiveQuorumCount` as the bound, the one that had just dropped out was
not, the lock fell back to replaying the selection, and the replay could land
on an older quorum and reject the lock as "invalid sig in islock". The bound
is now IsQuorumActive, the one the node already applies to sig shares and
recovered signatures: one quorum more.

Constructed, not waited for. Four quorums are mined; the third newest signs,
on a transaction whose old replay prefers the fourth; the receiver is restarted
with no peers and no recovered signatures (see feature_llmq_is_nonrotated_verify.py
for why both are needed) and its tip is taken back to the block that mined the
newest commitment, which is where the window is; the lock is then delivered
over P2P.

On the unfixed binary this test fails where it waits for the lock.
'''

import os
import shutil

from test_framework.messages import (
    COutPoint,
    hash256,
    msg_isdlock,
    ser_compact_size,
    ser_string,
)
from test_framework.p2p import P2PInterface
from test_framework.test_framework import DashTestFramework
from test_framework.util import assert_equal

LLMQ_TYPE_TEST_INSTANTSEND = 104
DKG_INTERVAL = 24


def internal(hex_hash):
    """A hash's bytes as the node serialises them: the printed hex, reversed."""
    return bytes.fromhex(hex_hash)[::-1]


def score(llmq_type, quorum_hash_hex, selection_hash):
    """One candidate's score: SHA256d(uint8 type || quorumHash || selectionHash)."""
    return hash256(bytes([llmq_type]) + internal(quorum_hash_hex) + selection_hash)


def lowest_scoring(llmq_type, quorum_hashes, selection_hash):
    """The quorum the selection picks: the lowest score, compared as bytes."""
    return min(quorum_hashes, key=lambda q: score(llmq_type, q, selection_hash))


class LLMQInstantSendNamedQuorumWindowTest(DashTestFramework):
    def set_test_params(self):
        self.set_dash_test_params(5, 4, [["-llmqtestinstantsenddip0024=llmq_test_instantsend"]] * 5)
        self.set_dash_llmq_test_params(4, 3)

    def run_test(self):
        node = self.nodes[0]

        node.sporkupdate("SPORK_17_QUORUM_DKG_ENABLED", 0)
        # 1 keeps InstantSend on but stops the masternodes signing mempool
        # transactions of their own accord, so the only lock is the one built here.
        node.sporkupdate("SPORK_2_INSTANTSEND_ENABLED", 1)
        node.sporkupdate("SPORK_3_INSTANTSEND_BLOCK_FILTERING", 0)
        self.wait_for_sporks_same()

        # The lock's transaction has to survive the receiver being taken back a
        # few blocks below. Spending freshly matured coinbases, it would not: the
        # rewind makes some of them immature again and the transaction leaves the
        # mempool. So it spends ordinary outputs made here, a hundred blocks deep
        # by the time it is built.
        self.log.info("Make ordinary outputs for the transactions to spend")
        addresses = [node.getnewaddress() for _ in range(40)]
        funding = node.sendmany("", {a: 5 for a in addresses})
        self.generate(node, 1)
        def address_of(script):
            return script.get("address") or (script.get("addresses") or [None])[0]

        self.spendable = [{"txid": funding, "vout": o["n"]}
                          for o in node.getrawtransaction(funding, True)["vout"]
                          if o["value"] == 5 and address_of(o["scriptPubKey"]) in addresses]
        assert_equal(len(self.spendable), 40)

        self.log.info("Mine four non-rotating InstantSend quorums")
        for _ in range(4):
            self.mine_quorum(llmq_type_name="llmq_test_instantsend", llmq_type=LLMQ_TYPE_TEST_INSTANTSEND)

        # Newest first, as the RPC reports them.
        quorums = node.quorum("list", 10)["llmq_test_instantsend"]
        assert len(quorums) >= 4, f"expected at least four quorums, got {quorums}"
        newest, signer, older = quorums[0], quorums[2], quorums[3]
        newest_mined = node.getblock(node.quorum("info", LLMQ_TYPE_TEST_INSTANTSEND, newest)["minedBlock"])["height"]
        signer_height = node.getblock(signer)["height"]
        self.log.info(f"newest quorum {newest[:16]} mined at {newest_mined}; the signer is {signer[:16]} "
                      f"(base {signer_height}), with {older[:16]} older than it")

        self.log.info("Pick a transaction the old replay gets wrong")
        txid, request_id, inputs = self.find_misleading_tx(signer, older)

        # The masternodes take sig shares from IsQuorumActive's set -- the three
        # newest here -- so the signer can still sign although it is no longer
        # among the two signing-active ones.
        self.log.info("The third newest quorum signs it, and only it")
        for mn in self.mninfo:
            mn.node.quorum("sign", LLMQ_TYPE_TEST_INSTANTSEND, request_id, txid, signer)
        self.wait_for_recovered_sig(request_id, txid, LLMQ_TYPE_TEST_INSTANTSEND, 15)
        rec_sig = self.mninfo[0].node.quorum("getrecsig", LLMQ_TYPE_TEST_INSTANTSEND, request_id, txid)
        assert_equal(rec_sig["quorumHash"], signer)

        self.log.info("Restart the receiver with no peers and no recovered signatures")
        recsigdb = os.path.join(node.datadir, self.chain, "llmq", "recsigdb")
        self.stop_node(0)
        assert os.path.isdir(recsigdb), f"no recovered-signature database at {recsigdb}"
        shutil.rmtree(recsigdb)
        self.start_node(0, extra_args=self.extra_args[0] + ["-connect=0"])
        assert_equal(node.quorum("hasrecsig", LLMQ_TYPE_TEST_INSTANTSEND, request_id, txid), False)

        # mine_quorum pads SIGN_HEIGHT_OFFSET blocks past each commitment, which
        # carries the tip out of the window. Take the receiver back to the block
        # that mined the newest commitment: there the signer is no longer
        # signing-active, but was so SIGN_HEIGHT_OFFSET blocks below.
        self.log.info(f"Take the receiver's tip back to {newest_mined}, inside the window")
        node.invalidateblock(node.getblockhash(newest_mined + 1))
        assert_equal(node.getblockcount(), newest_mined)
        active = node.quorum("list")["llmq_test_instantsend"]
        assert signer not in active, f"the signer is still signing-active at the receiver: {active}"
        assert newest in active, f"the newest quorum is not active at the receiver: {active}"
        assert node.getblockcount() > signer_height + DKG_INTERVAL, "the lock would not reach the replay"
        assert_equal(node.getrawtransaction(txid, True)["instantlock_internal"], False)

        peer = node.add_p2p_connection(P2PInterface())
        assert_equal(node.getconnectioncount(), 1)

        self.log.info("Deliver the lock over P2P, and expect it to be accepted")
        islock = msg_isdlock(1, inputs, int(txid, 16), int(signer, 16), bytes.fromhex(rec_sig["sig"]))
        peer.send_message(islock)
        peer.sync_with_ping()
        received = node.getpeerinfo()[0]["bytesrecv_per_msg"]
        assert "isdlock" in received, f"the lock never reached the node: {received}"

        def locked():
            self.bump_mocktime(1)
            return node.getrawtransaction(txid, True)["instantlock_internal"]

        self.wait_until(locked, timeout=30, sleep=1)

        self.log.info("And the stored lock names the quorum that signed it")
        islocks = node.getislocks([txid])
        assert_equal(len(islocks), 1)
        assert_equal(islocks[0]["cycleHash"], signer)

    def find_misleading_tx(self, signer, older, attempts=32):
        """
        A transaction whose request id makes the old replay prefer `older` to
        `signer`. As in feature_llmq_is_nonrotated_verify.py: thirty-two
        attempts fail one run in four billion by bad luck alone.
        """
        node = self.nodes[0]
        for _ in range(attempts):
            utxo = self.spendable.pop()
            raw_hex = node.createrawtransaction([utxo], {node.getnewaddress(): 4.999})
            signed = node.signrawtransactionwithwallet(raw_hex)
            assert signed["complete"], signed
            txid = node.sendrawtransaction(signed["hex"])
            self.sync_mempools()
            raw = node.getrawtransaction(txid, True)
            request_id_buf = ser_string(b"islock") + ser_compact_size(len(raw["vin"]))
            inputs = []
            for vin in raw["vin"]:
                point = COutPoint(int(vin["txid"], 16), int(vin["vout"]))
                request_id_buf += point.serialize()
                inputs.append(point)
            selection_hash = hash256(request_id_buf)
            if lowest_scoring(LLMQ_TYPE_TEST_INSTANTSEND, [signer, older], selection_hash) == older:
                return txid, selection_hash[::-1].hex(), inputs
            self.log.info(f"  {txid[:16]} would have resolved correctly; trying another")
        raise AssertionError("no transaction found whose replay lands on the older quorum")


if __name__ == '__main__':
    LLMQInstantSendNamedQuorumWindowTest().main()
