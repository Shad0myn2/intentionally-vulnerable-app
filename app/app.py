from flask import Flask, request, render_template_string

app = Flask(__name__)

# Vulnerable code: Hardcoded password check
@app.route('/', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        user = request.form.get('username')
        pwd = request.form.get('password')

        # Vul-1 Insecure password check (vulnerable to brute force, no hashing) 
        if user == 'admin' and pwd == 'admin':
            return "Welcome, admin!"
        else:
            error = "Invalid credentials."

        # Vul-2 Vulnerable to injection because of no validation on the input
        if '<script>' in user:
            error += " Potential XSS attack detected in username!"

    return render_template_string("""
        <h2>Login Page</h2>
        <form method="POST">
            Username: <input type="text" name="username" /><br/>
            Password: <input type="password" name="password" /><br/>
            <input type="submit" value="Login" />
        </form>
        <p style="color:red;">{{error}}</p>
    """, error=error)

if __name__ == '__main__':
    app.run(debug=True)
## Test Run