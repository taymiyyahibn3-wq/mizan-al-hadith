# Canonical Database Hash Verification (P0-01 Immutability Certification)

## Verification Result
- **Canonical Files Verified**: 32 SQLite databases
- **Verification Rule**: `PRE_HASH == POST_HASH`
- **Result**: **100% MATCH across all 32 databases. ZERO BYTES MUTATED.**

| Database Filename | File Size | Pre-Implementation SHA-256 | Post-Implementation SHA-256 | Status |
|---|---|---|---|---|
| `hadith-kg.db` | 1,642,500,096 B | `08c3a43d78f510828ab870a23203ef67d8ded7be81f74fdb1b9378996c65dfdd` | `08c3a43d78f510828ab870a23203ef67d8ded7be81f74fdb1b9378996c65dfdd` | ✅ MATCH |
| `isnad_network.db` | 52,092,928 B | `d141026b306388b4ad30ee6c5c51fca7bf5a2bf90f2698e6089198ff80fb1f6d` | `d141026b306388b4ad30ee6c5c51fca7bf5a2bf90f2698e6089198ff80fb1f6d` | ✅ MATCH |
| `hadith_numbering.db` | 35,094,528 B | `ecfe3079dba318bde09f544eaf84764a9095a1ec12e0bd3446acf5f6428a66cb` | `ecfe3079dba318bde09f544eaf84764a9095a1ec12e0bd3446acf5f6428a66cb` | ✅ MATCH |
| `hadith_commentaries.db` | 9,056,256 B | `2fcd9ae4deeb006de25d6db23719abd2ecdaf9779a14f29f81e0cf3a9acebed1` | `2fcd9ae4deeb006de25d6db23719abd2ecdaf9779a14f29f81e0cf3a9acebed1` | ✅ MATCH |
| `hadith_translations.db` | 24,051,712 B | `d35a3fbe852cb504b530d47239be55bb7f3d70051122fe2e5d2c5bc8bdba3e95` | `d35a3fbe852cb504b530d47239be55bb7f3d70051122fe2e5d2c5bc8bdba3e95` | ✅ MATCH |
| `english_enrichment.db` | 52,203,520 B | `db62d750fee3d94c50e3b9821d4ebb40ac875c58e8f0d1182e1dc1472e982d56` | `db62d750fee3d94c50e3b9821d4ebb40ac875c58e8f0d1182e1dc1472e982d56` | ✅ MATCH |
| `citation_enrichment.db` | 9,252,864 B | `8e3a1d03ee6d3668314448acfbb227476cfd85c88b5fb8e57cb92abf5c6d4c37` | `8e3a1d03ee6d3668314448acfbb227476cfd85c88b5fb8e57cb92abf5c6d4c37` | ✅ MATCH |
| `english_translation_fts.db` | 32,796,672 B | `8280636373c95a08b61d809dfe8b8697c8543e78a9d63b6fb7473b4fd798c74d` | `8280636373c95a08b61d809dfe8b8697c8543e78a9d63b6fb7473b4fd798c74d` | ✅ MATCH |
| `derived_semantic_index.db` | 85,180,416 B | `0867383f9b29bd9c31fcd197aa1ac4fa923f1114df5e20ca7c4feca1185be875` | `0867383f9b29bd9c31fcd197aa1ac4fa923f1114df5e20ca7c4feca1185be875` | ✅ MATCH |
| `hadith-search-index.db` | 248,565,760 B | `2d298c9a5bab669acaae61ccebee4135cccdee532be8d3764ffd2f85af48aab2` | `2d298c9a5bab669acaae61ccebee4135cccdee532be8d3764ffd2f85af48aab2` | ✅ MATCH |
| `english-search.db` | 78,024,704 B | `9d5a48c8854cbf3915aaf645e4ee21bbc23fe0be651386f07daeaec959420510` | `9d5a48c8854cbf3915aaf645e4ee21bbc23fe0be651386f07daeaec959420510` | ✅ MATCH |
| `ask_mizan.db` | 9,363,456 B | `d13222737c36c88f5ea16f4e31cb5a00479be228419e5d37996da6c674eeccaf` | `d13222737c36c88f5ea16f4e31cb5a00479be228419e5d37996da6c674eeccaf` | ✅ MATCH |
| `translation-cache.db` | 35,008,512 B | `3a126a3261b7bd2538116dc6e2020d4626ba15ad8b059b350da4fb0d4d8a2ce5` | `3a126a3261b7bd2538116dc6e2020d4626ba15ad8b059b350da4fb0d4d8a2ce5` | ✅ MATCH |
| `jarh-translation-cache.db` | 36,864 B | `b9e5fb4a0ed0e06ba8aa4763c3bf1e1d3c00183a181d3e7b06a48368778aae8f` | `b9e5fb4a0ed0e06ba8aa4763c3bf1e1d3c00183a181d3e7b06a48368778aae8f` | ✅ MATCH |
| `_iu_mapping_search.db` | 706,486,272 B | `776e1c9f0c7a0d3d968cb47e066497233bc6ed8a9459c731b11b0f1bc45c0ea8` | `776e1c9f0c7a0d3d968cb47e066497233bc6ed8a9459c731b11b0f1bc45c0ea8` | ✅ MATCH |

*(All remaining 17 snapshot backup databases in `data/` were likewise verified with identical pre/post cryptographic hashes; see `validation/targeted_ux_fix/post_hashes_all.json`).*

## Certification
No SQL `INSERT`, `UPDATE`, `DELETE`, `ALTER`, `VACUUM`, or schema migration was executed against any database. All database connections adhered strictly to read-only URI connection strings (`mode=ro`).
