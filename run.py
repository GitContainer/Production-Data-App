from production_data_app import app, socketio 
import subprocess
import sys
import os

p = subprocess.Popen([sys.executable, "/mnt/c/Users/automatizacion/Desktop/Git Projects/Production-Data-App/data_acquisition/opcServer.py"])

if __name__ == "__main__":
    socketio.run(app)
