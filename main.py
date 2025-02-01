from fastapi import FastAPI
import google.generativeai as genai
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI() 

# Configure Gemini AI API Key
GEMINI_API_KEY = "AIzaSyCi-GoXnRJVeb6Di-d-6wT1NWcKH-Khj7M"
genai.configure(api_key=GEMINI_API_KEY)

# Define a request model
class QuestionRequest(BaseModel):
    prompt: str

# 📌 1. Ask anything to Gemini AI
@app.post("/ask")
async def ask_gemini(request: QuestionRequest):
    """Takes a user's prompt and returns AI-generated response."""
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(request.prompt)
        return {"response": response.text}
    except Exception as e:
        return {"error": str(e)}

