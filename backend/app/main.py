from fastapi import FastAPI
# from app.models import InterviewRequest
from app.services.data_loader import load_candidates


app = FastAPI(
    title="AI Interview Agent",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "AI Interview Agent is running 🚀"
    }


# @app.post("/api/interview")
# def interview(request: InterviewRequest):

#     # First request starts the interview
#     if request.candidate:
#         return {
#             "reply": "Welcome! Let's begin your AI interview.",
#             "done": False
#         }

#     # Subsequent requests
#     return {
#         "reply": "Thanks for your answer. Here's your next question...",
#         "done": False
#     }



@app.get("/test")
def test():
    data = load_candidates()
    candidates = data["candidates"]

    return {
        "total_candidates": len(candidates),
        "first_candidate": candidates[0]["member"]["name"]
    }