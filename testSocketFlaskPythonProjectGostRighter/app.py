from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    socketio.start_background_task(target=run_script)
    return redirect(url_for('index'))

def run_script():
    process = subprocess.Popen(['python', 'main.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors='replace')
    for line in iter(process.stdout.readline, ''):
        socketio.emit('process_output', {'data': line})
        socketio.sleep(0.1)  # небольшая пауза для предотвращения переполнения
    process.stdout.close()
    process.wait()

if __name__ == '__main__':
    socketio.run(app, debug=True)
