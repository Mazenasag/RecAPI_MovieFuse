import sys
import os

# Add the current directory and src folder to sys.path
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Import your application from the existing application.py
from application import app as application

# This allows running with: python app.py (for testing)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    application.run(host="0.0.0.0", port=port, debug=True)