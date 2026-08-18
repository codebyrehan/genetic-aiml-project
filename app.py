from io import BytesIO

from flask import Flask, jsonify, render_template, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from src.clustering import summary as cluster_summary
from src.ecological_risk import assess_ecological_risk
from src.regulatory_engine import regulatory_assessment
from src.risk_engine import analyze

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "Genova Genetic Risk Intelligence"})


@app.post("/api/analyze")
def analyze_risk():
    try:
        payload = request.get_json(silent=True) or {}
        required = {"mismatches", "pam_correct", "in_exon", "conservation_score", "gc_content"}
        missing = required - payload.keys()
        if missing:
            return jsonify({"error": f"Missing fields: {', '.join(sorted(missing))}"}), 400
        return jsonify(analyze(payload))
    except (TypeError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        app.logger.exception("Risk analysis failed")
        return jsonify({"error": "Analysis service temporarily unavailable."}), 500


@app.get("/api/patterns")
def patterns():
    try:
        return jsonify(cluster_summary())
    except Exception:
        app.logger.exception("Pattern analysis failed")
        return jsonify({"error": "Pattern service temporarily unavailable."}), 500


@app.post("/api/ecological-risk")
def ecological_risk():
    try:
        payload = request.get_json(silent=True) or {}
        required = {"gene_drive", "off_target_sites", "population_impact", "uncertainty"}
        missing = required - payload.keys()
        if missing:
            return jsonify({"error": f"Missing fields: {', '.join(sorted(missing))}"}), 400
        return jsonify(assess_ecological_risk(
            gene_drive=bool(payload["gene_drive"]),
            off_target_sites=int(payload["off_target_sites"]),
            population_impact=float(payload["population_impact"]),
            uncertainty=float(payload["uncertainty"]),
        ))
    except (TypeError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        app.logger.exception("Ecological risk assessment failed")
        return jsonify({"error": "Ecological assessment temporarily unavailable."}), 500


@app.post("/api/regulatory-assessment")
def regulatory():
    try:
        payload = request.get_json(silent=True) or {}
        required = {"genetic_score", "ecological_score", "ethical_flags"}
        missing = required - payload.keys()
        if missing:
            return jsonify({"error": f"Missing fields: {', '.join(sorted(missing))}"}), 400
        return jsonify(regulatory_assessment(
            genetic_score=float(payload["genetic_score"]),
            ecological_score=float(payload["ecological_score"]),
            ethical_flags=int(payload["ethical_flags"]),
        ))
    except (TypeError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        app.logger.exception("Regulatory assessment failed")
        return jsonify({"error": "Regulatory assessment temporarily unavailable."}), 500


@app.post("/api/report")
def report():
    """Generate a compact educational assessment report from a completed analysis."""
    payload = request.get_json(silent=True) or {}
    if not payload.get("risk"):
        return jsonify({"error": "Complete a risk analysis before generating a report."}), 400

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 55
    pdf.setTitle("Genova Genetic Risk Intelligence Assessment")
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(48, y, "GENOVA — Genetic Risk Intelligence")
    y -= 28
    pdf.setFont("Helvetica", 10)
    pdf.drawString(48, y, "Educational PBL assessment · synthetic data · human oversight required")
    y -= 35
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(48, y, "Assessment Summary")
    y -= 22
    pdf.setFont("Helvetica", 10)
    risk = payload["risk"]
    lines = [
        f"Risk score: {risk.get('risk_score', 'N/A')}%",
        f"Risk label: {risk.get('label', 'N/A')}",
        f"Model: {risk.get('model', 'N/A')}",
        f"Confidence: {risk.get('confidence', 'N/A')}%",
    ]
    for line in lines:
        pdf.drawString(60, y, line)
        y -= 17

    for title, data in (("Ecological Assessment", payload.get("ecological")), ("Regulatory Assessment", payload.get("regulatory"))):
        y -= 10
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(48, y, title)
        y -= 20
        pdf.setFont("Helvetica", 10)
        if data:
            for key, value in data.items():
                text = f"{key.replace('_', ' ').title()}: {value}"
                pdf.drawString(60, y, text[:105])
                y -= 16
                if y < 70:
                    pdf.showPage()
                    y = height - 55
                    pdf.setFont("Helvetica", 10)
        else:
            pdf.drawString(60, y, "Not run")
            y -= 16

    y -= 10
    pdf.setFont("Helvetica-Oblique", 8)
    pdf.drawString(48, y, "This report is an educational prototype output, not medical, legal, clinical, or regulatory advice.")
    pdf.save()
    buffer.seek(0)
    return send_file(buffer, mimetype="application/pdf", as_attachment=True, download_name="genova-assessment.pdf")


if __name__ == "__main__":
    app.run(debug=True)
