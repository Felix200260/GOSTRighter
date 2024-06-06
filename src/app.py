from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('src', 'static', 'pdf')  # Путь к папке для загрузки файлов
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
app.secret_key = 'your_secret_key'  # Добавьте секретный ключ для работы с flash-сообщениями

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    file_url = session.pop('file_url', None)
    return render_template('index.html', file_url=file_url)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('index'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(file_path)
            flash('File successfully uploaded and processed', 'success')
            session['file_uploaded'] = True
            session['file_url'] = url_for('static', filename=f'pdf/{filename}')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'An error occurred while saving the file: {e}', 'danger')
            return redirect(url_for('index'))
    else:
        flash('Invalid file type. Only PDF files are allowed.', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
