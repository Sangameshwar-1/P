from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from jinja2 import Environment, FileSystemLoader
import psycopg2
from psycopg2 import pool
import os
import logging

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://naniiiiii.netlify.app"],  # Allow only your frontend domain
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Jinja2 template configuration
templates = Environment(loader=FileSystemLoader("templates"))

# Secure database connection using environment variables
DATABASE_URL = "postgresql://sale:X7eXTvOY6RtWchx2oCo4LA@mystic-ninja-4440.jxf.gcp-us-west2.cockroachlabs.cloud:26257/sangam?sslmode=verify-full&sslrootcert=https://cockroachlabs.cloud/clusters/e7f49c39-2968-4108-82ee-e452f0306e05/cert"
if not DATABASE_URL:
    raise Exception("DATABASE_URL environment variable not set!")

# Create a database connection pool (1 to 10 connections)
try:
    db_pool = pool.SimpleConnectionPool(1, 10, DATABASE_URL)
except psycopg2.Error as e:
    raise Exception(f"Error creating database connection pool: {e}")

# Function to get a database connection
def get_db_connection():
    try:
        return db_pool.getconn()
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

# Function to release a database connection back to the pool
def release_db_connection(conn):
    db_pool.putconn(conn)

# Exception handler for general errors
@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: Exception):
    logging.error(f"Error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": f"Internal Server Error: {exc}"}
    )

# Endpoint to check database connection
@app.get("/check-connection")
async def check_connection():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    cursor.close()
    release_db_connection(conn)
    return {"message": "Database connection successful!"}

# Home route (Fetch users)
@app.get("/", response_class=HTMLResponse)
async def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users;')
    users = cursor.fetchall()
    cursor.close()
    release_db_connection(conn)

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
    release_db_connection(conn)

    return {"message": "User added successfully!", "name": name, "email": email}

# View users command
@app.get("/view-users", response_class=JSONResponse)
async def view_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM users;')
        users = cursor.fetchall()
    except psycopg2.Error as e:
        logging.error(f"Database error: {e}")
        users = []
    finally:
        cursor.close()
        release_db_connection(conn)
    
    return JSONResponse(content={"users": users})

# Run the app using: uvicorn main:app --reload
