from app import app
from flask import render_template, request, redirect, url_for, flash, session

# Mock user data
users = {
    "admin": {"password123": "password123", "role": "admin"}
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

@app.route('/zaafiyet1', methods=['GET', 'POST']) ###CANISHERO SQL INJ. 
def zaafiyet1():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form['username']
        
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}'"
        print("Executing query:", query)  # Bu sadece gösterim amaçlıdır; prodüksiyonda kaldırılmalıdır
        c.execute(query)
        users = c.fetchall()
        
        conn.close()
        
        if users:
            return f"Found users: {users}"
        else:
            return "No users found!"
    
    return render_template('zaafiyet1.html')



@app.route('/zaafiyet2')
def zaafiyet2():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('zaafiyet2.html')


# Yetkilendirme için basit bir rol kontrolü
def is_admin(username):
    return users[username]["role"] == "admin"

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        if is_admin(session['username']):
            return "Hoş geldiniz, {}! Yönetici paneline erişiminiz var.".format(session['username'])
        else:
            return "Hoş geldiniz, {}! Bu, bir kullanıcı panelidir.".format(session['username'])
    return redirect(url_for('login'))  

@app.route('/fetch', methods=['POST'])
def fetch_data():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    url = request.form['url']
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return render_template_string("<pre>{{ data }}</pre>", data=response.text)
        else:
            return "Failed to fetch data"
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)


