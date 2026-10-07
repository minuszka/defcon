# Core audit schedule

The user approved this risk-first calendar on 2026-10-07 from the D03 Claude addendum. Original task IDs and goals are retained. The final deadline remains 2026-12-03; D52-D60 dates are unchanged.

D01-D03 preparation and mapping tasks are complete. Thoroughly source-audited coverage remains 0/4272; no daily slot is evidence that a source domain has been audited.

## Planned work

| ID | Planned date | Scope | Completion evidence |
| --- | --- | --- | --- |
| D04 | 2026-10-08 | Buildkonfiguráció, configure, Makefile és depends | Felesleges fordítás/buildmunka bizonyítása, kompatibilis konfigurációk |
| D05 | 2026-10-09 | CI-, lint-, csomagoló- és contrib-kód | Átvizsgált futási utak, változatlan ellenőrzési erősség |
| D06 | 2026-10-10 | src/util, common, compat, support és logging | Duplikációk, másolások, élettartamok és hibakezelés áttekintése |
| D08 | 2026-10-11 | Leállítás, scheduler, threadek és erőforrás-felszabadítás | Megállás/restart, megszakítás és deadlock-kockázat vizsgálata |
| D43 | 2026-10-12 | Script, serialization, primitives és chainparams | Konszenzusadatok, sorrend és bájtszintű kompatibilitás |
| D23 | 2026-10-13 | PoS stake/kernel és blokk-aláírás ellenőrzése | Konszenzusváltozás nélküli kódvizsgálat, pozitív és negatív esetek |
| D22 | 2026-10-14 | PoS minter és multiwallet erőforrásai | Változatlan stakingpolitika, szál- és zárolási elemzés |
| D40 | 2026-10-15 | Validation, chainstate és connect/disconnect | Konszenzus szempontú audit, pozitív/negatív összehasonlítás |
| D31 | 2026-10-16 | EvoDB és deterministic masternode-kezelés | Reconcile, regisztráció és állapotátmenetek megőrzése |
| D37 | 2026-10-17 | Sentinel/DSL források és háttérmunka | A leltárból azonosított tényleges fájlok teljes útvonalainak átolvasása |
| D38 | 2026-10-18 | Sentinel/DSL jelentések, pool és commitment | Azonos epoch, bitfield, határidő, büntetési döntések |
| D39 | 2026-10-19 | Governance, spork és special transaction utak | Azonos érvényesség, jutalom és aktiválási viselkedés |
| D33 | 2026-10-20 | LLMQ context, quorum-adatok és snapshotok | Élettartam és memóriaköltség, azonos quorumkiválasztás |
| D34 | 2026-10-21 | DKG-session, handler és session manager | Azonos időzítés és üzenetek, erőforrás-korlátok |
| D35 | 2026-10-22 | Quorum-aláírás és signing shares | Azonos ellenőrzési eredmény, hibás és késői adatok |
| D36 | 2026-10-23 | ChainLocks és InstantSend | Rotációs/korábbi quorum regressziók és változatlan érvényesség |
| D42 | 2026-10-24 | Miner, blokképítés és PoS-integráció | Azonos blokk-/tranzakciókiválasztás és jutalom |
| D44 | 2026-10-25 | Crypto, BLS és secp256k1 saját integrációja | Azonos hash/aláírás és negatív vektorok |
| D11 | 2026-10-26 | net_processing és üzenetkezelés | Dupla munka és korlátok vizsgálata, azonos üzenetkezelés |
| D10 | 2026-10-27 | net, kapcsolatkezelés és socket-élettartam | CPU/memória/I/O profil, hálózati kompatibilitás |
| D12 | 2026-10-28 | Peer-adatok, címkezelés, eviction és ban-kezelés | Viselkedési határok és biztonsági ellenőrzések megőrzése |
| D41 | 2026-10-29 | Mempool, policy, orphan és tranzakció-reconciliation | Azonos elfogadási policy és hálózati viselkedés |
| D29 | 2026-10-30 | Adatbázisréteg, coins/cache és batch-műveletek | Azonos tartalom és crash/restart viselkedés |
| D30 | 2026-10-31 | Indexek, blokkfájlok, pruning és snapshotutak | Olvasás/írás költsége, helyreállítás és formátumok |
| D32 | 2026-11-01 | Masternode kapcsolatok, szolgáltatás és háttérmunka | Dupla feldolgozás, cache és zárolás vizsgálata |
| D19 | 2026-11-02 | Egyenleg, AvailableCoins és UTXO-bejárások | Mért többszörös bejárások, azonos jogosultság és egyenleg |
| D20 | 2026-11-03 | Tranzakcióépítés, coin selection és díjak | Azonos kiválasztási/díjviselkedés, szélsőértékek |
| D18 | 2026-11-04 | Kulcskezelés, signing és wallet biztonsági utak | Hibaágak, titokkezelés és azonos aláírási eredmények |
| D17 | 2026-11-05 | Wallet betöltés, mentés és migrációs utak | Tesztwallet-adatokkal sértetlenségi és kompatibilitási bizonyíték |
| D16 | 2026-11-06 | Wallet-RPC és staking-RPC költségei | Helyes egyenleg/stakingadat, változatlan API |
| D21 | 2026-11-07 | PSBT, import/export és wallet interfészek | Azonos formátumok és meglévő munkafolyamatok |
| D24 | 2026-11-08 | CoinJoin vezérlés és walletkapcsolat | Adatvédelem, zárolás és meglévő funkciók megőrzése |
| D27 | 2026-11-09 | Qt wallet, küldés/fogadás és stakingnézet | Műveletek, megjelenítés és hibakezelés ellenőrzése |
| D25 | 2026-11-10 | Qt modellek, események és callbackek | Objektumélettartam, kapcsolatok, regressziós lefedettség |
| D26 | 2026-11-11 | Qt listák, szűrés és ismételt frissítés | Memória- és UI-költségmérés, azonos sorok és kijelölés |
| D28 | 2026-11-12 | Qt beállítások, dialógusok és platformkód | Kompatibilis beállítások és tényleges platformkorlátok |
| D07 | 2026-11-13 | Inicializálás és konfigurációbetöltés | Indulási utak, argumentumok és alapértelmezések megőrzése |
| D09 | 2026-11-14 | Naplózás, stats és diagnosztikai költségek | Mért költség, fontos események és RPC-válaszok megőrzése |
| D13 | 2026-11-15 | HTTP, RPC-szerver és kliens | Autentikáció, hibák, időkorlátok és erőforrások ellenőrzése |
| D14 | 2026-11-16 | RPC-regisztráció, argumentum- és eredményépítés | Azonos válaszséma, hibakód és dokumentált szerződés |
| D15 | 2026-11-17 | Blockchain- és node-RPC költségei | Ismételt munka mérése, snapshot/zárolás helyessége |
| D48 | 2026-11-18 | Interfészek, IPC, ZMQ és egyéb gyökérforrások | Hívási utak, leállítás és a leltár eddig nem érintett saját fájljai |
| D45 | 2026-11-19 | Beépített crypto/BLS/secp256k1 források | Fájlonként igazolt vizsgálat, upstream eltérések és nyitott lefedettség |
| D46 | 2026-11-20 | LevelDB, SQLite/BDB kapcsolatok és külső adattárolók | Integráció és ténylegesen átolvasott külső források leltára |
| D47 | 2026-11-21 | univalue, minisketch, crc32c, immer, gsl és egyéb függőségek | Minden leltári komponens vizsgálati mélysége, nincs eltitkolt kimaradás |
| D49 | 2026-11-22 | Unit tesztek és a meglévő CI-kivételek | Kivételek diagnózisa, valódi kódhiba és fixturehiba megkülönböztetése |
| D50 | 2026-11-23 | Functional framework, tesztek és port/időzítési ütközések | Valódi hibák megtartása, nincs automatikus retry-val elfedés |
| D51 | 2026-11-24 | Bench, fuzz és biztonsági segédkód | Jellemző terhelések, hibás bemenetek, indokolt sanitizerek |
| D52 | 2026-11-25 | Teljes fájlleltár második ellenőrzése | Hiányzó kód átolvasása, saját/külső lefedettség pontos kimutatása |
| D53 | 2026-11-26 | Keresztmodulos ismétlések és bizonyított holt kód | Hívó-/build-/platformbizonyíték minden javasolt törléshez |
| D54 | 2026-11-27 | Integrált teljesítmény- és kompatibilitási összehasonlítás | Azonos környezetű előtte/utána mérések a merge-elt állapoton |
| D55 | 2026-11-28 | CI-, restart-, reindex- és wallet-regressziók | Elkülönített adatokkal ellenőrzött végső integrált működés |
| D56 | 2026-11-29 | Tartalék: elhúzódó review és hibajavítás | A legfontosabb nyitott patch jóváhagyása és helyi CI-je |
| D57 | 2026-11-30 | Tartalék: hiányzó forráslefedettség és platformellenőrzés | Dokumentáltan lezárt vagy pontosan nyitva hagyott területek |
| D58 | 2026-12-01 | Független végső review másik modellcsaládtól | A merge-elt változások és összes nyitott észrevétel áttekintése |
| D59 | 2026-12-02 | Végső helyi CI és mérési összesítés | Valós exit code-ok, végső SHA, nincs lezáratlan FAIL elhallgatva |
| D60 | 2026-12-03 | Lezárás, PR/merge-állapot és végső átadó | Igazolt eredmények, maradék lista és egymondatos következő teendő |

The domain descriptions are retained in the working language of the audit, Hungarian. The table is a planning calendar, not an automatic schedule or a guarantee of complete review in one day.

## Constraints

Preserve all consensus and existing functionality, RPC/network contracts, wallet/database formats, staking policy and GUI actions. Do not delete defensive or compatibility paths without proving their role across callers, registration, build conditions and supported platforms.

D04 build/configure/Makefile/depends follows on 2026-10-08. D05 retains the high-ASLR sanitizer portability question; the original CI FAIL and child-only adapted local PASS remain separate evidence.

Use bounded function/caller batches for heavy domains. Vendored integration is not full-source review. Track remaining coverage through D52/D53 and D56/D57; report unfinished areas on D60 without silently extending the deadline.

Use one implementing session per worktree. Obtain independent different-family approval for the exact final patch, then run required local CI and relevant regressions before each code commit/PR; repeat review after substantive changes. Merge remains exclusively the user's.
