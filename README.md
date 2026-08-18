# GENOVA — Genetic Risk Intelligence

> **PBL · Introduction to AIML** — *Challenges in Regulating Genetic Information in Mammals*

GENOVA is a portfolio-grade educational web application demonstrating how AI/ML can support structured exploration of genetic-risk signals, pattern discovery, ecological consequences, scenario comparison, explainability, dataset inspection, model evaluation, and responsible regulatory review.

## ✨ Final portfolio feature set

- **Risk Analyzer:** Random Forest-based educational risk signal from a deterministic synthetic feature space.
- **Explainable AI Center:** relative feature-importance visualization plus interpretation guardrails.
- **Intelligence Dashboard:** genetic, ecological, and governance signals visualized together.
- **Scenario Laboratory:** baseline, high off-target, gene-drive, and high-conservation scenarios with comparative risk signals.
- **Ecological Risk Map:** interactive OpenStreetMap/Leaflet context using clearly labeled synthetic research zones.
- **Pattern Discovery:** reproducible K-Means clustering with interpretable pattern summaries.
- **Model Intelligence:** accuracy, precision, recall, F1 and confusion matrix on an 80/20 deterministic synthetic benchmark.
- **Research Dataset Studio:** CSV profiling, missing-value detection, supported-feature checks and numeric summaries; uploads are processed in memory and not persisted.
- **Ecological Review:** transparent proxy combining gene-drive status, off-target activity, population impact and uncertainty.
- **Regulatory Review:** human-review recommendation combining genetic, ecological and ethical signals.
- **Assessment Reports:** completed analyses can be exported as a PDF for PBL demonstrations.
- **Presentation Mode:** distraction-reduced view for viva/demo presentations.
- **Methodology + Responsible AI:** explicit limitations, synthetic-data framing and human-oversight guidance.
- **Production engineering:** Flask API, automated tests, GitHub Actions CI and Render deployment.

## Architecture

```text
Browser
  │
  ├── Risk Analyzer ─────────► POST /api/analyze ─────────► Random Forest Risk Engine
  ├── Ecological Review ─────► POST /api/ecological-risk ─► Ecological Proxy
  ├── Governance Review ─────► POST /api/regulatory-assessment ─► Regulatory Engine
  ├── Pattern Discovery ─────► GET  /api/patterns ───────► K-Means Service
  ├── Model Intelligence ────► GET  /api/model-metrics ──► Deterministic Benchmark
  ├── Dataset Studio ────────► POST /api/dataset-profile ► In-memory CSV Profiler
  └── Assessment Export ─────► POST /api/report ─────────► PDF Report
                                      │
                                      ▼
                         Responsible-AI + Human Oversight
```

## API surface

| Endpoint | Purpose |
| --- | --- |
| `GET /api/health` | service health check |
| `POST /api/analyze` | genetic risk assessment |
| `GET /api/patterns` | clustering/pattern summary |
| `POST /api/ecological-risk` | ecological proxy assessment |
| `POST /api/regulatory-assessment` | governance-oriented synthesis |
| `GET /api/model-metrics` | deterministic ML benchmark |
| `POST /api/dataset-profile` | safe in-memory CSV profiling |
| `POST /api/report` | PDF assessment export |

## Repository structure

- `app.py` — Flask application and API routes
- `src/risk_engine.py` — supervised risk analysis
- `src/model_intelligence.py` — reproducible model benchmark metrics
- `src/dataset_studio.py` — in-memory CSV profiler
- `src/clustering.py` — reproducible K-Means pattern discovery
- `src/ecological_risk.py` — transparent ecological-risk proxy
- `src/regulatory_engine.py` — human-review regulatory signal
- `tests/` — automated engine/API/report tests
- `.github/workflows/ci.yml` — CI pipeline
- `docs/RESPONSIBLE_AI.md` — limitations and responsible-use guidance
- `ARCHITECTURE.md` — system design
- `ALGORITHMS.md` — algorithm notes
- `templates/` + `static/` — responsive web experience

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

Run tests:

```bash
pytest -q
```

## Researcher

**Mohd Rehan**  
Roll No. **25SCS1003003208**  
Email: **codebyrehan@gmail.com**

## Responsible-use statement

This is an **educational prototype using synthetic data**. Its outputs are not medical, clinical, ecological, legal, or regulatory advice. The application does not approve or reject genetic interventions; it illustrates how AI/ML signals can be incorporated into a human-led review process. Geographic map points are synthetic research zones, not real release sites.
