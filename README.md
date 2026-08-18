# GENOVA — Genetic Risk Intelligence

> **PBL · Introduction to AIML** — *Challenges in Regulating Genetic Information in Mammals*

GENOVA is a portfolio-grade educational web application demonstrating how AI/ML can support structured exploration of genetic-risk signals, pattern discovery, ecological consequences, scenario comparison, explainability, and responsible regulatory review.

## ✨ Portfolio upgrades

- **Risk analysis:** Random Forest-based educational risk signal from synthetic genetic features.
- **Explainability:** feature-importance signals are surfaced alongside each prediction.
- **Intelligence dashboard:** genetic, ecological, and governance signals are visualized together.
- **Scenario simulator:** baseline, high off-target, gene-drive, and high-conservation scenarios can be compared interactively.
- **Pattern discovery:** reproducible K-Means clustering with interpretable pattern summaries.
- **Ecological risk:** transparent proxy combining gene-drive status, off-target activity, population impact, and uncertainty.
- **Regulatory review:** human-review recommendation combining genetic, ecological, and ethical signals.
- **Assessment reports:** completed analyses can be exported as a PDF for PBL demonstrations.
- **Methodology:** end-to-end explanation of feature engineering → prediction → clustering → governance synthesis.
- **Responsive portfolio UI:** polished desktop/mobile experience with live meters, scenario cards, and responsible-AI framing.
- **Production engineering:** Flask API, automated tests, GitHub Actions CI, and Render deployment.

## Architecture

```text
Browser
  │
  ├── Risk Analyzer ────────► POST /api/analyze ───────► Risk Engine
  ├── Ecological Review ────► POST /api/ecological-risk ► Ecological Proxy
  ├── Governance Review ────► POST /api/regulatory-assessment ► Regulatory Engine
  ├── Pattern Discovery ────► GET  /api/patterns ─────► K-Means Service
  └── Assessment Export ────► POST /api/report ───────► PDF Report
                                      │
                                      ▼
                             Responsible-AI framing
                             + Human oversight
```

## Repository structure

- `app.py` — Flask application, API routes, and PDF report generation
- `src/risk_engine.py` — supervised risk analysis
- `src/clustering.py` — reproducible K-Means pattern discovery
- `src/ecological_risk.py` — transparent ecological-risk proxy
- `src/regulatory_engine.py` — human-review regulatory signal
- `tests/test_engines.py` + `tests/test_api.py` — automated engine/API/report tests
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

This is an **educational prototype using synthetic data**. Its outputs are not medical, clinical, ecological, legal, or regulatory advice. The application does not approve or reject genetic interventions; it illustrates how AI/ML signals can be incorporated into a human-led review process.
