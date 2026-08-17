from flask import Flask, jsonify, render_template, request
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


if __name__ == "__main__":
    app.run(debug=True)
