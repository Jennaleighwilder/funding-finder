#!/usr/bin/env python3
"""
FUNDING FINDER - Web App
Serves the questionnaire UI and /api/match using the Python matching engine.
"""

import os
import json
from pathlib import Path

from flask import Flask, request, jsonify, send_from_directory

# Set DB path before importing engine (engine uses it at init)
BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "data"
DB_PATH = os.environ.get("DATABASE_PATH", str(DB_DIR / "funding_finder.db"))

# Lazy DB init so app starts fast and Railway healthcheck passes
def _ensure_db():
    DB_DIR.mkdir(exist_ok=True)
    if not Path(DB_PATH).exists():
        import sqlite3
        schema_path = BASE_DIR / "schema.sql"
        if schema_path.exists():
            conn = sqlite3.connect(DB_PATH)
            conn.executescript(schema_path.read_text())
            conn.commit()
            conn.close()
        # Seed from batch JSONs (batches 11–20 + BATCH_*/FIRST_100) when DB is empty
        try:
            from load_batches import load_all_batches
            n = load_all_batches(DB_PATH)
            if n:
                pass  # optional: log n loaded
        except Exception:
            pass
    else:
        # DB exists but may be empty (e.g. schema has no INSERTs); seed if empty
        try:
            from load_batches import load_all_batches
            load_all_batches(DB_PATH)
        except Exception:
            pass

from engine import FundingMatchEngine, UserProfile, Match

app = Flask(__name__, static_folder=BASE_DIR, static_url_path="")

# Amount range mapping from form (amount: micro/small/medium/large)
AMOUNT_MAP = {
    "micro": (0, 5_000),
    "small": (5_000, 25_000),
    "medium": (25_000, 100_000),
    "large": (100_000, 1_000_000),
}


def _get_engine():
    _ensure_db()
    return FundingMatchEngine(DB_PATH)


def form_to_profile(data: dict) -> UserProfile:
    """Build UserProfile from form JSON (HTML form or API payload)."""
    # Form may send id as list (checkboxes) or single value
    ids = data.get("id") or data.get("identity") or []
    if not isinstance(ids, list):
        ids = [ids] if ids else []
    identity_factors = [str(x).capitalize() for x in ids if x]

    amount_key = (data.get("amount") or "medium").lower()
    funding_min, funding_max = AMOUNT_MAP.get(amount_key, (5_000, 100_000))

    state = (data.get("state") or "").strip().upper()[:2]
    city = (data.get("city") or "").strip()
    zip_code = (data.get("zip") or "").strip()
    # Rural heuristic: many small towns / non-metro state list
    rural_states = {"WV", "VT", "ME", "MT", "WY", "SD", "ND", "AK"}
    hidden = {"rural_status": state in rural_states or len(zip_code) == 5}

    story = (data.get("story") or data.get("vision") or "")[:500]
    vision = (data.get("vision") or data.get("project_vision") or "")[:500]
    project_desc = vision or story or "General business or project"
    # Use description for project_field so tag matching (small_business, tech_startup, etc.) finds overlap
    project_field = (vision or story or "general business startup").lower()[:200]

    stage_map = {
        "concept": "Just an idea I can't stop thinking about",
        "planning": "I've been planning this for a while",
        "launched": "I've started but need help to grow",
        "growing": "I'm already doing this and want to expand",
    }
    project_stage = stage_map.get((data.get("stage") or "").lower()) or "I've been planning this for a while"

    return UserProfile(
        user_id=1,
        profile_id=1,
        location={"city": city, "state": state, "zip": zip_code or "00000"},
        age=35,
        project_type="business",
        project_field=project_field,
        project_description=project_desc,
        project_stage=project_stage,
        funding_needed=(float(funding_min), float(funding_max)),
        education_level=data.get("edu") or "Some college",
        experience_years=2,
        licenses=[],
        income_range="Under $50K household income",
        credit_range="Under 650",
        identity_factors=identity_factors,
        heritage="",
        obstacles_overcome=story[:300] if story else "",
        community_ties="",
        unique_story=story[:300] if story else "",
        hidden_eligibility_factors=hidden,
        nuanced_qualifications={},
        competitive_advantages=["Strong personal story"] if story else [],
        urgency=data.get("time") or "Within 6 months",
        time_capacity=data.get("cap") or "10-20 hours per week",
    )


def match_to_json(m: Match) -> dict:
    """Full report payload so user knows what to apply for, how, and where."""
    s = m.source
    return {
        "source": {
            "source_id": s.source_id,
            "source_name": s.source_name,
            "provider_name": s.provider_name,
            "source_type": s.source_type,
            "min_amount": s.min_amount,
            "max_amount": s.max_amount,
            "deadline": s.deadline.isoformat() if s.deadline else None,
            "deadline_type": s.deadline_type,
            "application_url": getattr(s, "application_url", None),
            "requirements_text": (s.requirements_text or "").strip(),
        },
        "overall_score": round(m.overall_score, 1),
        "eligibility_score": round(m.eligibility_score, 1),
        "success_probability": round(m.success_probability, 1),
        "fit_score": round(m.fit_score, 1),
        "match_reasons": m.match_reasons,
        "eligibility_gaps": m.eligibility_gaps or [],
        "competitive_advantages": m.competitive_advantages or [],
    }


@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "FUNDING_FINDER_FUN.html")


@app.route("/api/match", methods=["POST"])
def api_match():
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = dict(request.form)
            # Checkboxes: id or identity can have multiple values
            data["id"] = request.form.getlist("id") or request.form.getlist("identity") or []

        profile = form_to_profile(data)
        engine = _get_engine()
        matches = engine.match(profile, max_results=50)
        return jsonify({
            "ok": True,
            "matches": [match_to_json(m) for m in matches],
            "count": len(matches),
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/health")
def health():
    # Fast response so Railway healthcheck passes; DB init happens on first /api/match
    return jsonify({"status": "ok", "database": Path(DB_PATH).exists()})


@app.route("/api/stats")
def stats():
    """Return funding source count for search/report verification (3000+ when all batches loaded)."""
    _ensure_db()
    try:
        import sqlite3
        conn = sqlite3.connect(DB_PATH)
        cur = conn.execute("SELECT COUNT(*) FROM funding_sources WHERE active = 1")
        total = cur.fetchone()[0]
        conn.close()
        return jsonify({"status": "ok", "funding_sources": total})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
