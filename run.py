from production_data_app import app, socketio

import subprocess
import sys

pid = subprocess.Popen([sys.executable, "opcServer.py"]) # call subprocess

if __name__ == "__main__":
    socketio.run(app)
