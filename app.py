from flask import Flask, render_template
from flask_socketio import SocketIO
import pyautogui
import threading

pyautogui.FAILSAFE = False

global tl, tr
tl = ''
tr = ''

app = Flask(__name__)
socketio = SocketIO(app)
def jjjj():
    pyautogui.mouseDown()
def kkkk():
    global tl
    tl = threading.Timer(0.1, jjjj)
    tl.start()
    pyautogui.click()
def rrrr():
    pyautogui.click(button='right')
# Rota para servir a página HTML
@app.route('/')
def index():
    return render_template('index.html')

# Lidar com a recepção dos dados do giroscópio
@socketio.on('gyroscopeData')
def handle_gyroscope_data(data):
    global tl, tr
    if(data['left']):
        if(tl==''):
            tl = threading.Timer(0.01, kkkk)
            tl.start()
    else:
        if(not tl==''):
            tl.cancel()
            pyautogui.mouseUp()
            tl = ''
    if(data['right']):
        if(tr==''):
            tr = threading.Timer(0.01, rrrr)
            tr.start()
    else:
        if(not tr==''):
            tr.cancel()
            tr = ''
    
    pyautogui.moveRel(data['gamma']*-1*1,data['alpha']*-1*1)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)