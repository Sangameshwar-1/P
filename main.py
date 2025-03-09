from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
import logging

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://naniiiiii.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# GroqCloud API configuration
GROQ_API_KEY = "ogsk_psa2HblyLOUfwHiZT7jSWGdyb3FYyRAWF4c7zcK9khCE5vRLcfTQ"  # Store API key in environment variables
GROQ_URL = "https://api.groq.com/v1/chat/completions"

if not GROQ_API_KEY:
    raise Exception("GROQ_API_KEY environment variable not set!")

# Endpoint to call GroqCloud AI
@app.post("/ask")
async def ask_groq(prompt: str = Form(...)):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",  # Example model, update as needed
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=data)
        response_json = response.json()

        if response.status_code == 200:
            return JSONResponse(content={"response": response_json["choices"][0]["message"]["content"]})
        else:
            raise HTTPException(status_code=response.status_code, detail=response_json)

    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Run the app using: uvicorn main:app --reload
