from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)
DATABASE_URL="postgresql://sale:QeDD3bw2Vr6FptLFE5QsTQ@mystic-ninja-4440.jxf.gcp-us-west2.cockroachlabs.cloud:26257/sangam?sslmode=verify-full"

# # Get the connection string from the environment variable (DATABASE_URL)
# DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to CockroachDB
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Home route
@app.route('/')
def index():
    # Connect to the database and fetch users
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users;')
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('index.html', users=users)

# Add new user
@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect('/')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
