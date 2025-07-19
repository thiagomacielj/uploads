import os
import json
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, jsonify, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Adicione uma chave secreta para usar flash
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
DATA_FILE = os.path.join(app.config['UPLOAD_FOLDER'], 'uploads.json')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt', 'zip', 'pdf', 'cdr', 'psd'}

# Cria pasta e JSON se não existirem
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_unique_filename(directory, filename):
    """
    Garante que o arquivo não será sobrescrito.
    """
    base, ext = os.path.splitext(filename)
    counter = 1
    unique_filename = filename
    while os.path.exists(os.path.join(directory, unique_filename)):
        unique_filename = f"{base}_{counter}{ext}"
        counter += 1
    return unique_filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    name = request.form.get('name')
    date = request.form.get('date')
    if not name or not date:
        return jsonify({'success': False, 'message': 'Nome e data são obrigatórios.'})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = get_unique_filename(app.config['UPLOAD_FOLDER'], filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        with open(DATA_FILE, 'r') as f:
            uploads = json.load(f)

        uploads.append({
            'filename': filename,
            'name': name,
            'date': date
        })

        with open(DATA_FILE, 'w') as f:
            json.dump(uploads, f, indent=4)

        return jsonify({'success': True, 'message': 'Arquivo enviado com sucesso!'})

    return jsonify({'success': False, 'message': 'Arquivo inválido ou ausente.'})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)

    with open(DATA_FILE, 'r') as f:
        uploads = json.load(f)
    uploads = [u for u in uploads if u['filename'] != filename]
    with open(DATA_FILE, 'w') as f:
        json.dump(uploads, f, indent=4)

    flash('Arquivo excluído com sucesso!', 'success')
    return redirect(url_for('visualizar_uploads'))

@app.route('/visualizar')
def visualizar_uploads():
    with open(DATA_FILE, 'r') as f:
        uploads = json.load(f)
    return render_template('visualizar.html', uploads=uploads)

if __name__ == '__main__':
    app.run(debug=True)