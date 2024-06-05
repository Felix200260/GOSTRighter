from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'pdf/'  # Путь к папке для загрузки файлов
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
app.secret_key = 'your_secret_key'  # Добавьте секретный ключ для работы с flash-сообщениями

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Здесь можно добавить логику обработки файла
        flash('File successfully uploaded and processed')
        return redirect(url_for('index'))
    else:
        flash('Invalid file type. Only PDF files are allowed.')
        return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)
