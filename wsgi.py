import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({
        "message": "Wiki Veloz - System running", 
        "status": "ok",
        "timestamp": "2024-01-23T18:00:00Z"
    })

@app.route("/debug")
def debug():
    return jsonify({
        "status": "running", 
        "message": "Debug endpoint",
        "port": os.environ.get("PORT", "10000")
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
