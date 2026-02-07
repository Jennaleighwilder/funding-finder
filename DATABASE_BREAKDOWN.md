# Complete Database Breakdown – Funding Finder

**Grand total: 3,500+ sources** (loaded from batch JSONs for search and report generation)

---

## Source breakdown

| Batches | Count | Description |
|--------|-------|-------------|
| **Batches 1–10** (BATCH_2 … BATCH_10 + FIRST_100) | 1,000 | State programs – all 50 states |
| **Batches 11–20** | 1,000 | Mega industries |
| **Batches 21–27** | 700 | Demographics + crisis + heritage |
| **Batches 28–29** | 200 | Emerging tech + social enterprises |
| **Batch 30** | 100 | Export & international trade |
| **Batch 31** | 100 | Foreign governments + private foundations + contests |
| **Batch 32** | 100 | Religious & faith-based |
| **Batch 33** | 100 | Corporate grants & sponsorships |
| **Batch 34** | 100 | University & research institutions |
| **Batch 35** | 100 | Regional & local foundations |

**Total: 3,500 sources**

---

## How it’s loaded

- **Loader:** `load_batches.py` finds all `batch_*.json`, `BATCH_*_SOURCES.json`, and `FIRST_100_SOURCES.json`.
- **Order:** FIRST_100 → BATCH_2…10 → batch_11…batch_35 (and any future batch_36+).
- **When:** On first run when the DB is empty (created from `schema.sql`, then seeded from batches).
- **Verify:** `GET /api/stats` returns `"funding_sources": 3500` (or 3500+).

---

## Rigorous testing

1. **Load DB** (if fresh): run the app once so `data/funding_finder.db` is seeded, or run `load_batches.py` against the DB.
2. **Run test script:** `python3 test_database.py` — verifies DB exists, ≥3,500 active sources, sample rows, engine matches with URL.
3. **Load:** Deploy or run locally; confirm `/api/stats` shows 3,500+.
4. **Search:** Submit the questionnaire; confirm matches and full report (what to apply for, what you need, where to apply).
5. **Report:** Confirm each match shows full report; then try terms like faith-based, corporate grant, university, regional foundation for batches 31–35. Search for terms like “faith-based,” “corporate grant,” “university,” “regional foundation” to confirm new batches are in the pool.
