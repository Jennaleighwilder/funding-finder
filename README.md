# Funding Finder

Match users to funding opportunities using the Python matching engine and a multi-step questionnaire. Built by Jennifer Leigh West / The Forgotten Code Research Institute.

## Live site (GitHub Pages)

After you push, the app is deployed automatically to **GitHub Pages** and works without any backend:

- **URL:** `https://jennaleighwilder.github.io/funding-finder/`
- The form uses **client-side matching** (10 real funding sources) when the API isn’t available, so it works for everyone.

**Enable Pages (one time):** Repo → **Settings** → **Pages** → under “Build and deployment”, set **Source** to **GitHub Actions**. The workflow in `.github/workflows/pages.yml` runs on every push to `main`.

**Backup deploy (Render):** If Railway has issues, go to [render.com](https://render.com) → **New** → **Blueprint** → connect this repo. Render will use `render.yaml` and the Dockerfile.

## What’s included

- **Backend**: `engine.py` (matching logic), `app.py` (Flask API + static serve)
- **Frontend**: `FUNDING_FINDER_FUN.html` (multi-step form, calls `/api/match`)
- **Data**: `schema.sql` (DB schema + sample funding sources), JSON source batches
- **Deploy**: Dockerfile, Railway config, Procfile

## Run locally

```bash
# Create venv and install deps
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# DB is created on first run from schema.sql (in ./data/)
python app.py
```

Open **http://localhost:5000**. Submit the form; results come from the Python engine via `/api/match`.

## Build (Docker)

```bash
docker build -t funding-finder .
docker run -p 5000:5000 funding-finder
```

## Deploy (recommended: Railway)

This app is a **Python backend + SQLite + static HTML**. The best fit is **Railway** (or any host that runs Docker), so the DB and API run together.

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Funding Finder app"
git remote add origin https://github.com/YOUR_USERNAME/funding-finder.git
git push -u origin main
```

### 2. Deploy on Railway

1. Go to [railway.app](https://railway.app) and sign in (e.g. with GitHub).
2. **New Project** → **Deploy from GitHub repo** → choose your repo.
3. Railway will detect the **Dockerfile** and build the image.
4. In **Settings** → **Networking** → **Generate Domain** to get a public URL.
5. Optional: set **PORT** in Variables (Railway usually sets it automatically).

Your app will be at `https://your-app.up.railway.app`. The first request creates the SQLite DB from `schema.sql`.

### Alternative: Render

- **New** → **Web Service** → connect repo.
- **Build**: Docker (use existing Dockerfile).
- **Start**: leave default (uses Dockerfile `CMD`).
- Set **PORT** in Environment if required (Render sets it for you).

### Other hosts

- **Vercel**: Best for static sites. This app needs a persistent DB and a long-running process, so use **Railway or Docker** for the full stack. You could deploy only the HTML to Vercel and point the form at a Railway API URL if you split frontend/backend.
- **Fly.io / Render / Heroku**: Use the same Dockerfile or Procfile; set `PORT` in the environment.

## API

- **POST /api/match**  
  Body: form-urlencoded or JSON with `name`, `email`, `city`, `state`, `zip`, `vision`, `stage`, `amount`, `id` (array, e.g. woman, veteran), `story`, `edu`, `time`, `cap`.  
  Returns: `{ "ok": true, "matches": [...], "count": N }`.

- **GET /api/health**  
  Returns: `{ "status": "ok", "database": true/false }`.

## Files

| File | Purpose |
|------|--------|
| `app.py` | Flask app: serves HTML, `/api/match`, `/api/health`, DB init from schema |
| `engine.py` | Matching engine (UserProfile → funding source scores) |
| `questionnaire.py` | Question definitions for intake |
| `schema.sql` | DB schema + sample funding sources |
| `FUNDING_FINDER_FUN.html` | Multi-step form UI; submits to `/api/match` |
| `requirements.txt` | Flask, gunicorn |
| `Dockerfile` | Production image; gunicorn on `PORT` |
| `railway.json` | Railway build/deploy hints |
| `Procfile` | For Heroku-style hosts |

Database path: `data/funding_finder.db` (or `DATABASE_PATH` env). Created automatically from `schema.sql` on first run.
