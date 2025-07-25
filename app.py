"""
Wiki Veloz - Main Application Entry Point
Clean and modular Flask application
"""

import os

from app import create_app

# Create the Flask application instance
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    debug = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    app.run(debug=debug, host="0.0.0.0", port=port)
