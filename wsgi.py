import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

try:
    from app import app
    print("App imported successfully")
except Exception as e:
    print(f"Error importing main app: {e}")
    try:
        from app_simple import app
        print("Simple app imported as fallback")
    except Exception as e2:
        print(f"Error importing simple app: {e2}")
        from flask import Flask
        app = Flask(__name__)
        
        @app.route("/")
        def index():
            return {"message": "Wiki Veloz - System running", "status": "ok"}
        
        @app.route("/debug")
        def debug():
            return {"status": "running", "message": "Debug endpoint"}
        
        print("Minimal app created")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
