from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Connect to CockroachDB
conn = psycopg2.connect(
    dbname="webapp",
    user="root",
    host="localhost",
    port=26257
)
cursor = conn.cursor()

# Create table (Run this only once)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name STRING,
        email STRING
    )
""")
conn.commit()

# Route to get users
@app.route("/users", methods=["GET"])
def get_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return jsonify(users)

# Route to add a user
@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (data["name"], data["email"]))
    conn.commit()
    return jsonify({"message": "User added!"})

# Run the app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)



