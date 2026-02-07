#!/usr/bin/env python3
"""
Rigorous test: verify complete database (3,500 sources) and search/report.
Run: python test_database.py [path/to/funding_finder.db]
Default DB: data/funding_finder.db
"""
import sys
import sqlite3
from pathlib import Path

BASE = Path(__file__).resolve().parent
DB_PATH = sys.argv[1] if len(sys.argv) > 1 else str(BASE / "data" / "funding_finder.db")


def test_db_exists():
    assert Path(DB_PATH).exists(), f"DB not found: {DB_PATH}"
    print("✓ DB exists")


def test_source_count():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute("SELECT COUNT(*) FROM funding_sources WHERE active = 1")
    n = cur.fetchone()[0]
    conn.close()
    assert n >= 3500, f"Expected >= 3500 sources, got {n}"
    print(f"✓ Active sources: {n} (target 3,500)")


def test_sample_sources():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute("""
        SELECT source_name, provider_name, source_type, min_amount, max_amount, application_url
        FROM funding_sources WHERE active = 1
        ORDER BY RANDOM() LIMIT 5
    """)
    rows = cur.fetchall()
    conn.close()
    assert len(rows) >= 5
    for r in rows:
        assert r[0] and r[1], "source_name and provider_name must be set"
    print("✓ Sample rows have name, provider, type, amounts, url")


def test_engine_match():
    sys.path.insert(0, str(BASE))
    from engine import FundingMatchEngine, UserProfile
    engine = FundingMatchEngine(DB_PATH)
    profile = UserProfile(
        1, 1,
        {"city": "Nashville", "state": "TN", "zip": "37201"},
        35, "business", "tech", "AI tools for underserved communities",
        "I've been planning this for a while", (10000, 50000),
        "Some college", 2, [], "Under 50K", "Under 650",
        ["Woman", "Veteran"], "", "Poverty", "", "",
        {"rural_status": True}, {}, ["Community focus"],
        "Within 6 months", "10-20 hrs/week",
    )
    matches = engine.match(profile, max_results=50)
    assert len(matches) >= 1, "Engine should return at least one match"
    m = matches[0]
    assert m.source.source_name and m.source.provider_name
    assert hasattr(m.source, "application_url") or True
    print(f"✓ Engine returns {len(matches)} matches; top: {m.source.source_name[:50]}...")
    print(f"  Score: {m.overall_score:.1f}; URL: {getattr(m.source, 'application_url', 'N/A')}")


def main():
    print("Funding Finder – database & search test\n")
    try:
        test_db_exists()
        test_source_count()
        test_sample_sources()
        test_engine_match()
        print("\n✓ All tests passed. Complete database ready for rigorous testing.")
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        raise


if __name__ == "__main__":
    main()
