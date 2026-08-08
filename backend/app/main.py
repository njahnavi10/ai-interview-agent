from fastapi import FastAPI

from app.models import InterviewRequest

from app.services.data_loader import (
    load_curriculum,
    load_candidates,
    get_curriculum_day
)

from app.services.candidate_analyzer import analyze_candidate
from app.services.planner import create_interview_plan

from app.services.session_manager import (
    create_session,
    get_session
)

from app.services.ai_interviewer import (
    generate_ai_question,
    generate_follow_up_question
)

from app.services.answer_evaluator import evaluate_answer
from app.services.feedback_generator import generate_final_feedback

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

    # ============================================================
    # 1. START NEW INTERVIEW
    # ============================================================

    if request.candidate:

        candidate = request.candidate

        # Analyze candidate
        analysis = analyze_candidate(candidate)

        # Create personalized interview plan
        plan = create_interview_plan(
            analysis,
            num_questions=8
        )

        # Create session
        session = create_session(
            session_id=request.sessionId,
            candidate=candidate,
            analysis=analysis,
            plan=plan
        )

        # Extra adaptive-interview state
        session["evaluations"] = []
        session["followups_for_current"] = 0

        # First topic
        first_topic = plan["topics"][0]

        curriculum_day = get_curriculum_day(
            first_topic["day"]
        )

        if curriculum_day is None:
            return {
                "error": f"Curriculum day {first_topic['day']} not found"
            }

        # Generate AI question
        question = generate_ai_question(
            topic=first_topic,
            candidate=candidate,
            previous_answers=[],
            curriculum_day=curriculum_day
        )

        session["questions"].append(question)

        return {
            "sessionId": request.sessionId,
            "reply": question,
            "done": False
        }

    # ============================================================
    # 2. GET EXISTING SESSION
    # ============================================================

    session = get_session(request.sessionId)

    if session is None:
        return {
            "error": "Session not found"
        }

    if session["done"]:
        return {
            "sessionId": request.sessionId,
            "reply": "This interview has already been completed.",
            "done": True
        }

    # Make sure adaptive fields exist
    session.setdefault("evaluations", [])
    session.setdefault("followups_for_current", 0)

    # ============================================================
    # 3. GET CURRENT QUESTION
    # ============================================================

    current_question_index = session["current_question"]

    current_topic = session["plan"]["topics"][
        current_question_index
    ]

    curriculum_day = get_curriculum_day(
        current_topic["day"]
    )

    if curriculum_day is None:
        return {
            "error": f"Curriculum day {current_topic['day']} not found"
        }

    current_question = session["questions"][-1]

    # ============================================================
    # 4. SAVE CANDIDATE ANSWER
    # ============================================================

    answer = request.message

    if not answer:
        return {
            "error": "A message is required for an existing interview."
        }

    session["answers"].append(answer)

    # ============================================================
    # 5. EVALUATE ANSWER WITH GEMINI
    # ============================================================

    evaluation = evaluate_answer(
        question=current_question,
        answer=answer,
        candidate=session["candidate"],
        curriculum_day=curriculum_day
    )

    session["evaluations"].append(evaluation)

    # ============================================================
    # 6. ADAPTIVE FOLLOW-UP
    # ============================================================

    # Maximum ONE follow-up for each curriculum topic.
    if (
        evaluation["follow_up_needed"]
        and session["followups_for_current"] < 1
    ):

        session["followups_for_current"] += 1

        follow_up_question = generate_follow_up_question(
            topic=current_topic,
            candidate=session["candidate"],
            previous_answers=session["answers"],
            curriculum_day=curriculum_day,
            follow_up_focus=evaluation["follow_up_focus"]
        )

        session["questions"].append(
            follow_up_question
        )

        return {
            "sessionId": request.sessionId,
            "reply": follow_up_question,
            "done": False
        }

    # ============================================================
    # 7. MOVE TO NEXT CURRICULUM TOPIC
    # ============================================================

    session["current_question"] += 1

    # Reset follow-up counter for new topic
    session["followups_for_current"] = 0

    question_number = session["current_question"]

    # ============================================================
    # 8. CHECK WHETHER INTERVIEW IS COMPLETE
    # ============================================================

    if question_number >= len(session["plan"]["topics"]):

        session["done"] = True

        return {
            "sessionId": request.sessionId,
            "reply": "Thank you. The interview is complete.",
            "done": True
        }

    # ============================================================
    # 9. GENERATE NEXT TOPIC QUESTION
    # ============================================================

    next_topic = session["plan"]["topics"][
        question_number
    ]

    next_curriculum_day = get_curriculum_day(
        next_topic["day"]
    )

    if next_curriculum_day is None:
        return {
            "error": f"Curriculum day {next_topic['day']} not found"
        }

    question = generate_ai_question(
        topic=next_topic,
        candidate=session["candidate"],
        previous_answers=session["answers"],
        curriculum_day=next_curriculum_day
    )

    session["questions"].append(question)

    return {
        "sessionId": request.sessionId,
        "reply": question,
        "done": False
    }

@app.get("/test-ai")
def test_ai():

    topic = {
        "title": "Prompt Engineering Fundamentals"
    }

    candidate = {
        "member": {
            "name": "Sarah Johnson",
            "jobRole": "Senior Data Engineer",
            "yearsExperience": 9
        }
    }

    curriculum_day = get_curriculum_day(12)

    question = generate_ai_question(
    topic=topic,
    candidate=candidate,
    previous_answers=[],
    curriculum_day=curriculum_day
)

    return {
        "question": question
    }

@app.post("/test-evaluator")
def test_evaluator():

    candidate = {
        "member": {
            "name": "Sarah Johnson",
            "jobRole": "Senior Data Engineer",
            "yearsExperience": 9
        }
    }

    curriculum_day = get_curriculum_day(29)

    question = """
    How would you architect the observability layer using structured
    logging and Prometheus to track component-level latency,
    tool execution failures, and token costs?
    """

    answer = """
    I would use structured logs to capture tool failures and request
    information. Prometheus would collect metrics such as latency
    and error rates. I would avoid putting user_id and session_id
    directly into Prometheus labels because they create high
    cardinality.
    """

    evaluation = evaluate_answer(
        question=question,
        answer=answer,
        candidate=candidate,
        curriculum_day=curriculum_day
    )

    return evaluation

@app.post("/test-feedback")
def test_feedback():

    candidate = {
        "member": {
            "name": "Sarah Johnson",
            "jobRole": "Senior Data Engineer",
            "yearsExperience": 9
        }
    }

    questions = [
        "How would you design a hybrid retrieval engine?",
        "How would you handle high-cardinality Prometheus metrics?"
    ]

    answers = [
        "I would route structured queries to SQL and semantic queries to vector search.",
        "I would avoid using user_id and session_id as Prometheus labels."
    ]

    evaluations = [
        {
            "score": 7,
            "level": "GOOD",
            "strengths": [
                "Understands SQL and vector retrieval"
            ],
            "gaps": [
                "Needs more detail on result ranking"
            ],
            "misconceptions": [],
            "follow_up_needed": False,
            "follow_up_focus": ""
        },
        {
            "score": 4,
            "level": "DEVELOPING",
            "strengths": [
                "Understands high-cardinality risk"
            ],
            "gaps": [
                "Limited knowledge of Prometheus metric types"
            ],
            "misconceptions": [],
            "follow_up_needed": True,
            "follow_up_focus": "Prometheus counters and histograms"
        }
    ]

    feedback = generate_final_feedback(
        candidate=candidate,
        questions=questions,
        answers=answers,
        evaluations=evaluations
    )

    return feedback