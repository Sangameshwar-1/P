from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from jinja2 import Environment, FileSystemLoader
import psycopg2
import os

# Initialize FastAPI app
app = FastAPI()

# Database connection
DATABASE_URL = "postgresql://sale:QeDD3bw2Vr6FptLFE5QsTQ@mystic-ninja-4440.jxf.gcp-us-west2.cockroachlabs.cloud:26257/sangam?sslmode=verify-full"

# Jinja2 template configuration
templates = Environment(loader=FileSystemLoader("templates"))

# Function to get database connection
def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

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

    return RedirectResponse(url="/", status_code=303)

# Run the app using: uvicorn main:app --reload
