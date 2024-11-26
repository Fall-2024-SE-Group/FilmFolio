import sys
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Ensure the app can find the `src` package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src import app, db, routes  # Import initialized components and routes
from src import socket

# Run the app
if __name__ == "__main__":
    # Use `socket.run` for SocketIO compatibility
    socket.run(app, debug=True, port=8000, allow_unsafe_werkzeug=True)
