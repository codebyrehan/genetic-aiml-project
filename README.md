# GENOVA — Genetic Risk Intelligence

> **PBL · Introduction to AIML** — *Challenges in Regulating Genetic Information in Mammals*

GENOVA is a portfolio-grade educational web application that demonstrates how AI/ML can support structured exploration of genetic-risk signals, pattern discovery, ecological considerations, and responsible regulatory review.

## What the application demonstrates

- **Risk analysis:** a Random Forest-based educational risk signal from synthetic genetic features.
- **Pattern discovery:** reproducible K-Means clustering with silhouette-score model selection.
- **Explainability:** feature-importance signals are surfaced alongside the prediction.
- **Ecological risk:** a transparent proxy combines gene-drive status, off-target activity, population impact, and uncertainty.
- **Regulatory review:** a human-review recommendation combines genetic, ecological, and ethical signals.
- **Responsible AI:** explicit limitations, privacy guidance, human oversight, and non-clinical/non-regulatory positioning.
- **Production engineering:** Flask API, responsive frontend, automated tests, GitHub Actions CI, and Render deployment.

## Architecture

```text
Browser
  │
  ├── Risk Analyzer ────────► POST /api/analyze ──► Risk Engine
  │
  └── Pattern Discovery ────► GET  /api/patterns ─► K-Means Service

Risk / ecological / regulatory modules
                 │
                 ▼
        Responsible-AI framing
```

## Repository structure

- `app.py` — Flask application and API routes
- `src/risk_engine.py` — supervised risk analysis
- `src/clustering.py` — reproducible K-Means pattern discovery
- `src/ecological_risk.py` — transparent ecological-risk proxy
- `src/regulatory_engine.py` — human-review regulatory signal
- `tests/test_engines.py` — automated tests
- `.github/workflows/ci.yml` — CI pipeline
- `docs/RESPONSIBLE_AI.md` — limitations and responsible-use guidance
- `ARCHITECTURE.md` — system design
- `ALGORITHMS.md` — algorithm notes
- `templates/` + `static/` — web experience

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

This is an **educational prototype using synthetic data**. Its outputs are not medical, clinical, ecological, legal, or regulatory advice. The application does not approve or reject genetic interventions; it is designed to illustrate how AI/ML signals can be incorporated into a human-led review process.
