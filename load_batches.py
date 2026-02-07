#!/usr/bin/env python3
"""
Load batch JSON files (batches 11-20 and compatible formats) into funding_sources table.
Used for report generation and search so Funding Finder has the best data of its kind.
"""

import json
import re
import sqlite3
from pathlib import Path
from typing import List, Tuple, Optional, Any

BASE_DIR = Path(__file__).resolve().parent


def parse_funding_range(s: str) -> Tuple[Optional[float], Optional[float]]:
    """Parse funding_range string to (min_amount, max_amount). Returns (None, None) if unparseable."""
    if not s or not isinstance(s, str):
        return (None, None)
    s = s.strip()
    # "$50,000 - $500,000" or "$10,000,000 - $1,000,000,000"
    m = re.findall(r'\$[\d,]+(?:\.\d+)?', s)
    if len(m) >= 2:
        try:
            low = float(m[0].replace('$', '').replace(',', ''))
            high = float(m[1].replace('$', '').replace(',', ''))
            if low > high:
                low, high = high, low
            return (low, high)
        except ValueError:
            pass
    if len(m) == 1:
        try:
            val = float(m[0].replace('$', '').replace(',', ''))
            return (val, val)
        except ValueError:
            pass
    # "30% of investment" or percentage-based: treat as 0 to very high so it matches broadly
    if '%' in s or 'percent' in s.lower():
        return (0.0, 999_999_999.0)
    return (None, None)


def normalize_type(t: str) -> str:
    """Normalize source type to schema values: grant, loan, etc."""
    if not t:
        return 'grant'
    t = str(t).lower().strip()
    if t in ('grant', 'loan', 'contest', 'angel', 'microloan', 'crowdfund', 'tax_credit', 'scholarship'):
        return t
    if 'loan' in t:
        return 'loan'
    if 'tax' in t or 'credit' in t:
        return 'tax_credit'
    if 'contest' in t or 'prize' in t:
        return 'contest'
    return 'grant'


def batch_record_to_row(rec: dict) -> Optional[dict]:
    """Convert one batch JSON record to funding_sources row dict."""
    name = (rec.get('name') or '').strip()
    if not name:
        return None
    # Batch 11-20: source = provider
    provider = (rec.get('source') or rec.get('provider') or '').strip()
    source_type = normalize_type(rec.get('type') or 'grant')
    # Keep tags in requirements_text for display; use ALL so engine doesn't over-penalize (tags aren't literal field match)
    eligibility = rec.get('eligibility')
    if isinstance(eligibility, list):
        requirements_text = 'Eligibility: ' + ', '.join(str(x) for x in eligibility[:15])
    elif isinstance(eligibility, dict):
        requirements_text = 'Eligibility: ' + str(eligibility)
    else:
        requirements_text = ''
    eligible_fields = 'ALL'
    funding_range = rec.get('funding_range') or ''
    min_a, max_a = parse_funding_range(funding_range)
    if min_a is None and max_a is None:
        # Fallback from amount_min/amount_max (FIRST_100 style)
        min_a = rec.get('amount_min')
        max_a = rec.get('amount_max')
        if min_a is not None:
            min_a = float(min_a)
        if max_a is not None:
            max_a = float(max_a)
    if min_a is None:
        min_a = 0.0
    if max_a is None:
        max_a = 0.0
    obscurity = rec.get('obscurity_score') or rec.get('obscurity') or 5
    quality_score = max(1, min(100, 100 - (obscurity * 10)))
    url = (rec.get('url') or rec.get('application_url') or '').strip()
    prov = (provider or 'Unknown')[:500]
    # Heuristic: federal vs state vs private/corporate
    if 'U.S.' in prov or 'federal' in prov.lower() or 'irs.gov' in prov or 'energy.gov' in prov:
        provider_type = 'federal'
    elif 'Department of' in prov or 'State ' in prov or prov.endswith(' state') or any(s in prov for s in ('Alabama', 'Commerce', 'Labor', 'Economic', 'Revenue', 'SSBCI')):
        provider_type = 'state'
    else:
        provider_type = 'private'
    return {
        'source_name': name[:500],
        'source_type': source_type[:50],
        'provider_name': prov,
        'provider_type': provider_type,
        'min_amount': min_a,
        'max_amount': max_a,
        'typical_award': (min_a + max_a) / 2 if max_a else min_a,
        'application_deadline': None,
        'deadline_type': 'rolling',
        'eligible_states': 'ALL',
        'eligible_project_types': '["business", "nonprofit"]',
        'eligible_fields': eligible_fields,
        'requirements_text': (requirements_text or rec.get('description') or '')[:2000],
        'application_url': url or None,
        'application_complexity': 'moderate',
        'success_rate': 0.1,
        'number_awarded_last_year': 0,
        'quality_score': quality_score,
        'legitimacy_verified': 1,
        'active': 1,
    }


def find_batch_files() -> List[Path]:
    """Find ALL batch funding source JSON files for search (batch_11..35+, BATCH_2..10, FIRST_100 → 3,500 sources)."""
    seen = set()
    found: List[Path] = []
    # batch_11, batch_12, ..., batch_20, batch_21, ... (any batch_*.json)
    for p in BASE_DIR.glob('batch_*.json'):
        if p.resolve() not in seen:
            seen.add(p.resolve())
            found.append(p)
    # BATCH_2_SOURCES.json through BATCH_10, BATCH_11, etc.
    for p in BASE_DIR.glob('BATCH_*_SOURCES.json'):
        if p.resolve() not in seen:
            seen.add(p.resolve())
            found.append(p)
    # FIRST_100_SOURCES.json
    first100 = BASE_DIR / 'FIRST_100_SOURCES.json'
    if first100.exists() and first100.resolve() not in seen:
        seen.add(first100.resolve())
        found.append(first100)
    # Sort: FIRST_100 first, then BATCH_2..BATCH_10, then batch_11..batch_20..batch_30+
    def order_key(path: Path) -> tuple:
        name = path.stem.upper()
        if 'FIRST' in name:
            return (0, 0)
        m = re.search(r'BATCH_(\d+)', name)
        if m:
            return (1, int(m.group(1)))
        m = re.search(r'BATCH_?(\d+)', name)
        if m:
            return (2, int(m.group(1)))
        return (3, 0)
    found.sort(key=order_key)
    return found


def load_all_batches(db_path: str) -> int:
    """
    Load all batch JSON files into funding_sources. Returns count of rows inserted.
    Idempotent: only inserts if table is empty (caller can truncate first for full reload).
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.execute("SELECT COUNT(*) FROM funding_sources")
    if cur.fetchone()[0] > 0:
        conn.close()
        return 0
    files = find_batch_files()
    inserted = 0
    for path in files:
        try:
            raw = path.read_text(encoding='utf-8', errors='replace')
            data = json.loads(raw)
        except Exception:
            continue
        if not isinstance(data, list):
            continue
        for rec in data:
            if not isinstance(rec, dict):
                continue
            row = batch_record_to_row(rec)
            if not row:
                continue
            try:
                conn.execute("""
                    INSERT INTO funding_sources (
                        source_name, source_type, provider_name, provider_type,
                        min_amount, max_amount, typical_award,
                        application_deadline, deadline_type,
                        eligible_states, eligible_project_types, eligible_fields,
                        requirements_text, application_url, application_complexity,
                        success_rate, number_awarded_last_year, quality_score, legitimacy_verified, active
                    ) VALUES (
                        :source_name, :source_type, :provider_name, :provider_type,
                        :min_amount, :max_amount, :typical_award,
                        :application_deadline, :deadline_type,
                        :eligible_states, :eligible_project_types, :eligible_fields,
                        :requirements_text, :application_url, :application_complexity,
                        :success_rate, :number_awarded_last_year, :quality_score, :legitimacy_verified, :active
                    )
                """, row)
                inserted += 1
            except Exception:
                continue
    conn.commit()
    conn.close()
    return inserted


if __name__ == '__main__':
    import sys
    db_path = sys.argv[1] if len(sys.argv) > 1 else str(BASE_DIR / 'data' / 'funding_finder.db')
    BASE_DIR.mkdir(exist_ok=True)
    (BASE_DIR / 'data').mkdir(exist_ok=True)
    n = load_all_batches(db_path)
    print(f"Inserted {n} funding sources from batch files.")
