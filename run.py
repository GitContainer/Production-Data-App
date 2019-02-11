from production_data_app import app, socketio 
import subprocess
import sys
import os

if __name__ == "__main__":
    # Runs the web server using socketio, eventlet and gunicorn
    socketio.run(app)
