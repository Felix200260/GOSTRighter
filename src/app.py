from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
import os
import subprocess

app = Flask(__name__)
app.config['UPLOAD_FOLDER_PDF'] = os.path.join('src', 'static', 'pdf')
app.config['UPLOAD_FOLDER_WORD'] = os.path.join('src', 'static', 'word')
app.config['ALLOWED_EXTENSIONS_PDF'] = {'pdf'}
app.config['ALLOWED_EXTENSIONS_WORD'] = {'docx'}
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)

def clear_upload_folders():
    """Очистка папок загрузки."""
    folders = [app.config['UPLOAD_FOLDER_PDF'], app.config['UPLOAD_FOLDER_WORD']]
    for folder in folders:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)  # Удаление файла
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

def allowed_file(filename, allowed_extensions):
    """Проверка, что файл имеет допустимое расширение."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/')
def index():
    """Главная страница приложения."""
    pdf_file_url = session.pop('pdf_file_url', None)
    return render_template('index.html', pdf_file_url=pdf_file_url)

@app.route('/upload', methods=['POST']) 
def upload_file():
    """Загрузка PDF-файла."""
    if 'file' not in request.files:
        flash('No file part', 'danger')  # Сообщение об ошибке
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'danger')  # Сообщение об ошибке
        return redirect(url_for('index'))
    if file and allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS_PDF']):
        folder = app.config['UPLOAD_FOLDER_PDF']
        filename = secure_filename(file.filename)
        file_path = os.path.join(folder, filename)
        try:
            os.makedirs(folder, exist_ok=True)
            file.save(file_path)
            flash(f'{filename} successfully uploaded and processed', 'success')
            session['pdf_file_url'] = url_for('static', filename=f'pdf/{filename}')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'An error occurred while saving the file: {e}', 'danger')  # Сообщение об ошибке
            return redirect(url_for('index'))
    else:
        flash('Invalid file type. Only PDF files are allowed.', 'danger')  # Сообщение об ошибке
        return redirect(url_for('index'))

@app.route('/upload_word', methods=['POST'])
def upload_word_file():
    """Загрузка Word-файла."""
    if 'word_file' not in request.files:
        flash('No file part', 'danger')  # Сообщение об ошибке
        return redirect(url_for('next_stage'))
    file = request.files['word_file']
    if file.filename == '':
        flash('No selected file', 'danger')  # Сообщение об ошибке
        return redirect(url_for('next_stage'))
    if file and allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS_WORD']):
        folder = app.config['UPLOAD_FOLDER_WORD']
        filename = secure_filename(file.filename)
        file_path = os.path.join(folder, filename)
        try:
            os.makedirs(folder, exist_ok=True)
            file.save(file_path)  # Сохранение файла
            flash(f'{filename} successfully uploaded and processed', 'success')  # Сообщение об успешной загрузке
            session['word_file_url'] = url_for('static', filename=f'word/{filename}')
            return redirect(url_for('next_stage'))
        except Exception as e:
            flash(f'An error occurred while saving the file: {e}', 'danger')  # Сообщение об ошибке
            return redirect(url_for('next_stage'))
    else:
        flash('Invalid file type. Only Word files are allowed.', 'danger')  # Сообщение об ошибке
        return redirect(url_for('next_stage'))

@app.route('/next_stage')
def next_stage():
    """Переход на следующую страницу после загрузки Word-файла."""
    word_file_url = session.pop('word_file_url', None)
    return render_template('second_stage.html', word_file_url=word_file_url)

@app.route('/process', methods=['POST'])
def process_files():
    """Обработка файлов с помощью скрипта main.py."""
    pdf_file_path = os.path.join(app.config['UPLOAD_FOLDER_PDF'], os.path.basename(session.get('pdf_file_url', '')))
    word_file_path = os.path.join(app.config['UPLOAD_FOLDER_WORD'], os.path.basename(session.get('word_file_url', '')))
    
    try:
        with subprocess.Popen(
            ['python', 'src/main.py', pdf_file_path, word_file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            text=True
        ) as process:
            output = ""
            for line in process.stdout:
                output += line
                socketio.emit('process_output', {'data': line})
                print(line, end='')  # Вывод каждой строки в реальном времени в консоль
            for line in process.stderr:
                output += line
                socketio.emit('process_output', {'data': line})
                print(line, end='')  # Вывод ошибок в реальном времени в консоль
            
        if process.returncode != 0:
            flash(f'An error occurred during processing: {output}', 'danger')
            return redirect(url_for('next_stage'))
        
        flash('Processing completed', 'success')  # Сообщение об успешной обработке
        session['process_output'] = output
        return redirect(url_for('process_output'))
    except Exception as e:
        flash(f'An error occurred during processing: {e}', 'danger')  # Сообщение об ошибке
        return redirect(url_for('next_stage'))

@app.route('/process_output')
def process_output():
    """Вывод результата обработки."""
    process_output = session.pop('process_output', '')
    return render_template('process_output.html', process_output=process_output)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER_PDF'], exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER_WORD'], exist_ok=True)
    clear_upload_folders()
    socketio.run(app, debug=True)
