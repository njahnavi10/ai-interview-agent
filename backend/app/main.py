from fastapi import FastAPI
from app.models import InterviewRequest

app = FastAPI(
    title="AI Interview Agent",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "AI Interview Agent is running 🚀"
    }


@app.post("/api/interview")
def interview(request: InterviewRequest):

    # First request starts the interview
    if request.candidate:
        return {
            "reply": "Welcome! Let's begin your AI interview.",
            "done": False
        }

    # Subsequent requests
    return {
        "reply": "Thanks for your answer. Here's your next question...",
        "done": False
    }