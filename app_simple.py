from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return "Wiki Veloz - Funcionando!"

@app.route("/debug")
def debug():
    return jsonify({
        "status": "running",
        "message": "Wiki Veloz está funcionando!"
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
