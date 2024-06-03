from flask import Flask, request, redirect, url_for, render_template, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Bu, oturumları güvenli hale getirmek için gereklidir.

# Basit bir kullanıcı veri tabanı
users = {
    'admin': 'password123',
    'user1': 'mypassword'
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Kimlik doğrulama ve tanımlama
        if username not in users:
            flash('Identification failed: User not found.')
            return redirect(url_for('login'))
        elif users[username] != password:
            flash('Authentication failed: Incorrect password.')
            return redirect(url_for('login'))
        else:
            session['username'] = username
            flash('Login successful!')
            return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
