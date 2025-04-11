from flask import Flask, request, render_template, redirect, url_for
import sqlite3

# Initialize Flask app
app = Flask(__name__)

# Function to initialize the database (if needed)
def init_db():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
    cursor.execute("INSERT INTO users (username, password) VALUES ('user', 'user123')")
    conn.commit()
    conn.close()

# Vulnerable login function (SQL Injection risk)
def unsafe_login(username, password):
    # Vulnerable SQL query (SQL Injection risk)
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return user

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = unsafe_login(username, password)
    
    if user:
        return redirect(url_for('dashboard', username=username))
    else:
        return 'Invalid credentials, try again.'

@app.route('/dashboard')
def dashboard():
    return 'Welcome to the dashboard!'

if __name__ == '__main__':
    # Initialize the database if not already done
    init_db()
    # Run the Flask app
    app.run(debug=True)
