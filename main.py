from fastapi import FastAPI
import google.generativeai as genai
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

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
@app.post("/ask", response_model=AnswerResponse)
async def ask_gemini(request: QuestionRequest):
    """Takes a user's prompt and returns AI-generated response."""
    try:
        # Make a request to Gemini AI API
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(request.question)
        return {"response": response.text}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}
