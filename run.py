from production_data_app import app, socketio 
import subprocess
import sys
import os

# Creates another process that will execute the OPC server
p = subprocess.Popen([sys.executable, "/mnt/c/Users/automatizacion/Desktop/Git Projects/Production-Data-App/data_acquisition/opcServer.py"])

if __name__ == "__main__":
    # Runs the web server using socketio, eventlet and gunicorn
    socketio.run(app)
