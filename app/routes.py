from app import app
from flask import render_template, request, redirect, url_for, flash, session

# Mock user data
users = {
    "admin": "password123"
}

@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/about')
def about():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('about.html')

@app.route('/contact')
def contact():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['logged_in'] = True
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You were logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/zaafiyet1')
def zaafiyet1():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('zaafiyet1.html')

@app.route('/zaafiyet2')
def zaafiyet2():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('zaafiyet2.html')