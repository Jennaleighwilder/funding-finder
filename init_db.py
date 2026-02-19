#!/usr/bin/env python3
"""Pre-build DB at Docker image build time so API responds instantly."""
import sqlite3
from pathlib import Path

db = "/app/data/funding_finder.db"
schema = Path("/app/schema.sql")
if schema.exists():
    conn = sqlite3.connect(db)
    conn.executescript(schema.read_text())
    conn.commit()
    conn.close()

from load_batches import load_all_batches
n = load_all_batches(db)
print(f"Pre-loaded {n} funding sources into image")
