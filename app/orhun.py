from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)

# Profil resimlerinin yükleneceği dizin
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ana sayfa
@app.route('/')
def index():
    return render_template('index.html')

# Profil resmi yükleme formu
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Dosyayı kontrol et
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            # Dosyayı güvenli bir şekilde yükle
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
