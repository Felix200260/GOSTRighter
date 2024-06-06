from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('src', 'static', 'pdf')
app.config['WORD_UPLOAD_FOLDER'] = os.path.join('src', 'static', 'word')
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
app.config['ALLOWED_WORD_EXTENSIONS'] = {'doc', 'docx'}
app.secret_key = 'your_secret_key'

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/')
def index():
    return render_template('index.html', file_url=session.get('file_url'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('index'))
    if file and allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS']):
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

@app.route('/next_stage')
def next_stage():
    word_file_url = session.pop('word_file_url', None)
    return render_template('second_stage.html', file_url=word_file_url)

@app.route('/upload_word', methods=['POST'])
def upload_word_file():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('next_stage'))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('next_stage'))
    if file and allowed_file(file.filename, app.config['ALLOWED_WORD_EXTENSIONS']):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['WORD_UPLOAD_FOLDER'], filename)
        try:
            os.makedirs(app.config['WORD_UPLOAD_FOLDER'], exist_ok=True)
            file.save(file_path)
            flash('Word file successfully uploaded and processed', 'success')
            session['word_file_uploaded'] = True
            session['word_file_url'] = url_for('static', filename=f'word/{filename}')
            return redirect(url_for('next_stage'))
        except Exception as e:
            flash(f'An error occurred while saving the file: {e}', 'danger')
            return redirect(url_for('next_stage'))
    else:
        flash('Invalid file type. Only Word files (.doc, .docx) are allowed.', 'danger')
        return redirect(url_for('next_stage'))

if __name__ == '__main__':
    app.run(debug=True)
