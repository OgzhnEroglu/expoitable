from flask import Flask, render_template, request, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_session import Session
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Veritabanı bağlantısı oluşturma
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Veritabanı oluşturma ve örnek kullanıcı ekleme
def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, username TEXT, message TEXT)')
    conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('admin', 'password'))
    conn.commit()
    conn.close()

class LoginForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    captcha = StringField('CAPTCHA', validators=[DataRequired()])
    submit = SubmitField('Giriş Yap')

class MessageForm(FlaskForm):
    message = TextAreaField('Mesaj', validators=[DataRequired()])
    submit = SubmitField('Gönder')

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        captcha = form.captcha.data

        # CAPTCHA bypass: CAPTCHA doğrulaması yapılmadan geçiliyor
        if captcha == 'bypass':
            conn = get_db_connection()
            user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
            conn.close()
            if user:
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                return "Geçersiz kullanıcı adı veya şifre."
        else:
            return "Geçersiz CAPTCHA."
    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    form = MessageForm()
    if form.validate_on_submit():
        message = form.message.data
        username = session['username']

        conn = get_db_connection()
        conn.execute('INSERT INTO messages (username, message) VALUES (?, ?)', (username, message))
        conn.commit()
        conn.close()

        return "Mesaj gönderildi: " + message
    return render_template('dashboard.html', form=form)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
 