from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from jinja2 import Environment, FileSystemLoader
import psycopg2
import os

# Initialize FastAPI app
app = FastAPI()

# # Initialize Jinja2 environment
# templates = Environment(loader=FileSystemLoader("templates"))

# Database connection
DATABASE_URL = "postgresql://sale:X7eXTvOY6RtWchx2oCo4LA@mystic-ninja-4440.jxf.gcp-us-west2.cockroachlabs.cloud:26257/sangam?sslmode=verify-full"

# Function to get database connection
def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
    return conn

# Endpoint to check database connection
@app.get("/check-connection")
async def check_connection():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        return {"message": "Database connection successful!"}
    else:
        raise HTTPException(status_code=500, detail="Database connection failed!")

# Home route (Fetch users)
@app.get("/", response_class=HTMLResponse)
async def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users;')
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    template = templates.get_template("index.html")
    return HTMLResponse(content=template.render(users=users))

# Add new user (POST)
@app.post("/add")
async def add_user(name: str = Form(...), email: str = Form(...)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "User added successfully!", "name": name, "email": email}

# View users command
@app.get("/view-users", response_class=JSONResponse)
async def view_users():
    users = []
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM users;')
            users = cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
        finally:
            cursor.close()
            conn.close()
    
    return JSONResponse(content={"users": users})

# Run the app using: uvicorn main:app --reload
