import os 
from flask import Flask, request, redirect, url_for, render_template 
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.utils import secure_filename 
 
app = Flask(__name__) 
app.config.from_object('config.Config') 
db = SQLAlchemy(app) 
 
UPLOAD_FOLDERS = { 
    'олени': os.path.join(app.config['UPLOAD_FOLDER'], 'олени'), 
    'кабарга': os.path.join(app.config['UPLOAD_FOLDER'], 'кабарга'), 
    'косуля': os.path.join(app.config['UPLOAD_FOLDER'], 'косуля') 
} 
 
for folder in UPLOAD_FOLDERS.values(): 
    os.makedirs(folder, exist_ok=True) 
 
class FileUpload(db.Model): 
    __tablename__ = 'file_uploads' 
    id_number = db.Column(db.Integer, primary_key=True) 
    img_name = db.Column(db.String(255)) 
    tag = db.Column(db.String(255)) 
    root = db.Column(db.String(255)) 
    label = db.Column(db.String(255)) 
    comment = db.Column(db.Text) 
 
    def __repr__(self): 
        return f'<File {self.img_name}>' 
 
@app.route('/') 
def index(): 
    return render_template('index.html') 
 
@app.route('/upload', methods=['POST']) 
def upload_file(): 
    if 'file' not in request.files: 
        return redirect(request.url) 
    file = request.files['file'] 
    if file.filename == '': 
        return redirect(request.url) 
    if file: 
        filename = secure_filename(file.filename) 
        label = request.form['label'] 
        if label not in UPLOAD_FOLDERS: 
            return "Invalid label", 400 
        folder_path = UPLOAD_FOLDERS[label] 
        file_path = os.path.join(folder_path, filename) 
        file.save(file_path) 
        file_format = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'unknown' 
        new_file = FileUpload( 
            img_name=filename, 
            tag=file_format, 
            root=file_path, 
            label=label, 
            comment=request.form['comment'] 
        ) 
        db.session.add(new_file) 
        db.session.commit() 
        return redirect(url_for('history')) 
 
@app.route('/history') 
def history(): 
    uploads = FileUpload.query.all() 
    return render_template('history.html', uploads=uploads) 
 
@app.route('/history/<root>') 
def history_by_root(root): 
    uploads = FileUpload.query.filter_by(root=root).all() 
    return render_template('history.html', uploads=uploads) 
 
@app.route('/clear_history', methods=['POST']) 
def clear_history(): 
    db.session.query(FileUpload).delete() 
    db.session.commit() 
    return redirect(url_for('history')) 
 
if __name__ == '__main__': 
    db.create_all() 
    app.run(debug=True, host='0.0.0.0')