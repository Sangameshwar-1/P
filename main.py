from fastapi import FastAPI, HTTPException
import google.generativeai as genai
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import asyncio

# Initialize FastAPI app
app = FastAPI()

# Configure Gemini AI API Key
GEMINI_API_KEY = "AIzaSyCi-GoXnRJVeb6Di-d-6wT1NWcKH-Khj7M"
genai.configure(api_key=GEMINI_API_KEY)

# CORS middleware to allow requests from specific origin
origins = [
    "https://naniiiiii.netlify.app",  # Add your frontend URL here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow the listed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Define a request model for the incoming question
class QuestionRequest(BaseModel):
    question: str

# Define the response model (could be modified to include more data)
class AnswerResponse(BaseModel):
    response: str

# Ask anything to Gemini AI
@app.post("/ask")
async def ask_gemini(request: QuestionRequest):
    """Takes a user's prompt and returns AI-generated response."""
    try:
        # You may need to use async methods if generativeai supports it
        model = genai.GenerativeModel("gemini-pro")
        response = await asyncio.to_thread(model.generate_content, request.question)  # Run blocking code in a thread

        return {"response": response.text}

    except Exception as e:
        # Return a more descriptive error
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")
