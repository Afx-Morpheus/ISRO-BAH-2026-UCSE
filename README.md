# Urban Cooling Strategy Engine (UCSE)

An interactive, local-first prototype for exploring satellite-inspired urban heat intelligence and budget-constrained urban cooling investment strategies.

> **Demo data notice:** The included Chennai zones and metrics are synthetic demonstration values. This build does not yet ingest live ISRO/Google Earth Engine imagery or authoritative census/municipal datasets. Outputs are illustrative indices, not validated temperature, energy, carbon or population forecasts.

## Features
- Chennai demo heat and vulnerability map (Leaflet + OpenStreetMap tiles).
- Zone indicators: illustrative LST, NDVI, built-up share, population and vulnerability.
- Physics-informed intervention explanations.
- Budget, Balanced and Cooling objective profiles.
- Budget-constrained portfolio ranking across urban forestry, cool roofs, solar canopies, green roofs, reflective pavements, permeable surfaces and blue-green infrastructure.
- Three-scenario comparison.
- Exportable plain-text planning report.
- FastAPI backend with health, zone, optimization, scenario and report endpoints.

## Run on Windows
1. Install Python 3.10 or newer from https://www.python.org/downloads/ (enable **Add Python to PATH**).
2. Extract this ZIP.
3. Double-click `START_UCSE.bat`.
4. Open http://127.0.0.1:8000 in your browser.

The first run creates a virtual environment and installs dependencies. Internet is needed for dependency installation and the online map tiles/fonts. The app's API and optimizer run locally.

## Run manually
```bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000. API docs are at http://127.0.0.1:8000/docs.

## Test the optimizer
```bash
pytest -q
```

## Project structure
```text
UCSE_Project/
├── app/
│   ├── main.py              # FastAPI routes
│   └── optimizer.py         # transparent portfolio ranking logic
├── data/
│   └── zones.json           # synthetic Chennai demo zones
├── docs/
│   └── model_assumptions.md # assumptions, limitations, validation roadmap
├── static/
│   ├── index.html           # dashboard
│   ├── style.css
│   └── app.js
├── tests/
│   └── test_optimizer.py
├── requirements.txt
├── START_UCSE.bat
└── README.md
```

## API endpoints
- `GET /api/health`
- `GET /api/zones`
- `POST /api/optimize` with `{ "budget_crore": 150, "mode": "balanced" }`
- `POST /api/scenarios` with `{ "budget_crore": 150 }`
- `POST /api/report` with `{ "budget_crore": 150, "mode": "balanced" }`

## Next steps for a research-grade implementation
Connect approved Earth-observation data; build reproducible LST/NDVI/LULC processing; add real population and infrastructure layers; source local intervention costs; calibrate cooling/energy/carbon response; replace the baseline greedy selector with a validated multi-objective optimizer; and quantify uncertainty. See `docs/model_assumptions.md`.
