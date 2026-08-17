from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "Genova Genetic Risk Intelligence"})

if __name__ == "__main__":
    app.run(debug=True)
