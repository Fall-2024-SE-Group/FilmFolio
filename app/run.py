"""
This module initializes the database for the application.
"""


import os
import sys
from src import app, socket  # Import initialized components and routes

# Ensure the app can find the `src` package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# Run the app
if __name__ == "__main__":
    # Use `socket.run` for SocketIO compatibility
    socket.run(app, debug=True, port=8000, allow_unsafe_werkzeug=True)
