from production_data_app import app, socketio

import subprocess
import sys

pid = subprocess.Popen([sys.executable, "/mnt/d/Projects/Production-Data-App/data_acquisition/test.py"]) # call subprocess
# pid = subprocess.Popen([sys.executable, "/mnt/c/Users/automatizacion/Desktop/Git Projects/Production-Data-App/data_acquisition/opcServer.py"])

if __name__ == "__main__":
    socketio.run(app)
