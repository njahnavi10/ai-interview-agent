from fastapi import FastAPI
# from app.models import InterviewRequest
from app.services.data_loader import load_candidates,load_curriculum
from app.services.candidate_analyzer import analyze_candidate
from app.services.planner import create_interview_plan
from app.services.session_manager import (
    create_session,
    get_session
)
from app.services.question_generator import generate_question
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

@app.get("/test-curriculum")
def test_curriculum():
    data = load_curriculum()

    return {
        "type": type(data).__name__,
        "preview": data
    }

@app.get("/test-candidate/{candidate_id}")
def test_candidate(candidate_id: str):
    data = load_candidates()

    for candidate in data["candidates"]:
        if candidate["member"]["id"] == candidate_id:
            return analyze_candidate(candidate)

    return {
        "error": "Candidate not found"
    }

@app.get("/test-plan/{candidate_id}")
def test_plan(candidate_id: str):
    data = load_candidates()

    for candidate in data["candidates"]:
        if candidate["member"]["id"] == candidate_id:
            analysis = analyze_candidate(candidate)
            return create_interview_plan(analysis)

    return {
        "error": "Candidate not found"
    }

@app.get("/test-session/{session_id}")
def test_session(session_id: str):

    session = get_session(session_id)

    if session is None:
        return {
            "exists": False
        }

    return {
        "exists": True,
        "current_question": session["current_question"],
        "done": session["done"]
    }

@app.post("/test-session/{session_id}")
def create_test_session(session_id: str):

    session = create_session(
        session_id=session_id,
        candidate={"name": "Sarah Johnson"},
        analysis={"test": True},
        plan={"topics": []}
    )

    return {
        "session_created": True,
        "session_id": session_id
    }

@app.post("/api/interview")
def interview(request: InterviewRequest):

    # ------------------------------------------------
    # 1. NEW INTERVIEW
    # ------------------------------------------------

    if request.candidate:

        candidate = request.candidate

        analysis = analyze_candidate(candidate)

        plan = create_interview_plan(
            analysis,
            num_questions=8
        )

        session = create_session(
            session_id=request.sessionId,
            candidate=candidate,
            analysis=analysis,
            plan=plan
        )

        first_topic = plan["topics"][0]

        question = generate_question(first_topic)

        session["questions"].append(question)

        return {
            "sessionId": request.sessionId,
            "reply": question,
            "done": False
        }

    # ------------------------------------------------
    # 2. CONTINUE EXISTING INTERVIEW
    # ------------------------------------------------

    session = get_session(request.sessionId)

    if session is None:
        return {
            "error": "Session not found"
        }

    # Save candidate's answer
    if request.message:
        session["answers"].append(request.message)

    # Move to next question
    session["current_question"] += 1

    question_number = session["current_question"]

    # ------------------------------------------------
    # 3. END INTERVIEW AFTER 8 QUESTIONS
    # ------------------------------------------------

    if question_number >= len(session["plan"]["topics"]):

        session["done"] = True

        return {
            "sessionId": request.sessionId,
            "reply": "Thank you. The interview is complete.",
            "done": True
        }

    # ------------------------------------------------
    # 4. ASK NEXT QUESTION
    # ------------------------------------------------

    next_topic = session["plan"]["topics"][question_number]

    question = generate_question(next_topic)

    session["questions"].append(question)

    return {
        "sessionId": request.sessionId,
        "reply": question,
        "done": False
    }