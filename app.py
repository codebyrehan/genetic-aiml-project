from flask import Flask, jsonify, render_template, request
from src.risk_engine import analyze

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api/health")
def health():
    return jsonify({"status":"ok","service":"Genova Genetic Risk Intelligence"})

@app.post("/api/analyze")
def analyze_risk():
    try:
        payload=request.get_json(silent=True) or {}
        required={"mismatches","pam_correct","in_exon","conservation_score","gc_content"}
        missing=required-payload.keys()
        if missing:
            return jsonify({"error":f"Missing fields: {', '.join(sorted(missing))}"}),400
        return jsonify(analyze(payload))
    except (TypeError,ValueError) as exc:
        return jsonify({"error":str(exc)}),400
    except Exception:
        app.logger.exception("Risk analysis failed")
        return jsonify({"error":"Analysis service temporarily unavailable."}),500

if __name__=="__main__":
    app.run(debug=True)
