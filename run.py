from production_data_app import app, socketio 
import subprocess
import sys
import os

pid = 32768

def check_pid(pid):        
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

if not check_pid(pid):
    """ Call subprocess. """
    p = subprocess.Popen([sys.executable, "/mnt/c/Users/automatizacion/Desktop/Git Projects/Production-Data-App/data_acquisition/opcServer.py"])
    pid = p.pid

if __name__ == "__main__":
    socketio.run(app)
