from urllib import request

from fastapi import FastAPI
from requests import session

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
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Interview Agent",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def home():
    return {
        "message": "AI Interview Agent is running 🚀"
    }




@app.get("/test")
def test():
    data = load_candidates()
    candidates = data["candidates"]

    return {
        "total_candidates": len(candidates),
        "first_candidate": candidates[0]["member"]["name"]
    }


@app.get("/api/candidates")
def get_candidates():
    data = load_candidates()

    return {
        "candidates": data["candidates"]
    }

@app.get("/test-curriculum")
def test_curriculum():
    data = load_curriculum()

    return {
        "type": type(data).__name__,
        "preview": data
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

        # Adaptive interview state
        session["evaluations"] = []
        session["followups_for_current"] = 0
        session["total_interactions"] = 0

        first_topic = plan["topics"][0]

        curriculum_day = get_curriculum_day(
            first_topic["day"]
        )

        if curriculum_day is None:
            return {
                "error": f"Curriculum day {first_topic['day']} not found"
            }

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

    # Adaptive fields
    session.setdefault("evaluations", [])
    session.setdefault("followups_for_current", 0)
    session.setdefault("total_interactions", 0)
    session.setdefault("transcript", [])

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

    # Count this answer
    session["total_interactions"] += 1

    # ============================================================
    # 5. EVALUATE ANSWER
    # ============================================================

    evaluation = evaluate_answer(
        question=current_question,
        answer=answer,
        candidate=session["candidate"],
        curriculum_day=curriculum_day
    )

    session["evaluations"].append(evaluation)

    # ============================================================
    # 6. SAVE TRANSCRIPT
    # ============================================================

    session["transcript"].append({
        "topic_day": current_topic["day"],
        "topic_title": current_topic["title"],
        "question": current_question,
        "answer": answer,
        "evaluation": evaluation,
        "is_followup": session["followups_for_current"] > 0
    })

    # ============================================================
    # 7. HARD LIMIT: 8 TOTAL ANSWERS
    # ============================================================

    if session["total_interactions"] >= 8:

        feedback = generate_final_feedback(
            candidate=session["candidate"],
            questions=[
                item["question"]
                for item in session["transcript"]
            ],
            answers=[
                item["answer"]
                for item in session["transcript"]
            ],
            evaluations=[
                item["evaluation"]
                for item in session["transcript"]
            ]
        )

        session["feedback"] = feedback
        session["done"] = True

        return {
            "sessionId": request.sessionId,
            "reply": "Thank you. The interview is complete.",
            "done": True,
            "feedback": feedback
        }

    # ============================================================
    # 8. ADAPTIVE FOLLOW-UP
    # ============================================================

    if (
        evaluation.get("follow_up_needed", False)
        and session["followups_for_current"] < 1
    ):

        session["followups_for_current"] += 1

        follow_up_question = generate_follow_up_question(
            topic=current_topic,
            candidate=session["candidate"],
            previous_answers=session["answers"],
            curriculum_day=curriculum_day,
            follow_up_focus=evaluation.get(
                "follow_up_focus",
                ""
            )
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
    # 9. MOVE TO NEXT CURRICULUM TOPIC
    # ============================================================

    session["current_question"] += 1

    session["followups_for_current"] = 0

    question_number = session["current_question"]

    # ============================================================
    # 10. SAFETY CHECK
    # ============================================================

    if question_number >= len(
        session["plan"]["topics"]
    ):

        feedback = generate_final_feedback(
            candidate=session["candidate"],
            questions=[
                item["question"]
                for item in session["transcript"]
            ],
            answers=[
                item["answer"]
                for item in session["transcript"]
            ],
            evaluations=[
                item["evaluation"]
                for item in session["transcript"]
            ]
        )

        session["feedback"] = feedback
        session["done"] = True

        return {
            "sessionId": request.sessionId,
            "reply": "Thank you. The interview is complete.",
            "done": True,
            "feedback": feedback
        }

    # ============================================================
    # 11. GENERATE NEXT TOPIC QUESTION
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