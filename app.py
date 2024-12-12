from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for sessions

# Sample data for registered users
users_db = {
    "test@example.com": {"name": "John Doe", "password": "password123"}
}

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Check if email already exists
        if email in users_db:
            return render_template('register.html', error="User already registered. Please login.")
        
        # Simulate saving the user to the "database"
        users_db[email] = {"name": name, "password": password}
        return render_template('register.html', success="Successfully registered! Now login.")
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if user exists and password is correct
        if email in users_db and users_db[email]['password'] == password:
            # Store user data in session
            session['user'] = {'name': users_db[email]['name'], 'email': email}
            return redirect(url_for('landing'))
        else:
            return render_template('login.html', error="Invalid credentials, please try again.")
    
    return render_template('login.html')

@app.route('/landing')
def landing():
    # Check if user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Pass user data to the landing page template
    user = session['user']
    return render_template('landing.html', user=user)

@app.route('/logout')
def logout():
    # Remove user from session and redirect to login
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
