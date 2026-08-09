from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import InterviewRequest

from app.services.data_loader import (
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


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ai-interview-agent-frontend-6uuq.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def home():
    return {
        "message": "AI Interview Agent is running 🚀"
    }


# ============================================================
# GET CANDIDATES
# ============================================================

@app.get("/api/candidates")
def get_candidates():
    data = load_candidates()

    return {
        "candidates": data["candidates"]
    }


# ============================================================
# INTERVIEW
# ============================================================

@app.post("/api/interview")
def interview(request: InterviewRequest):

    # ========================================================
    # 1. START NEW INTERVIEW
    # ========================================================

    if request.candidate:

        candidate = request.candidate

        # Analyze candidate
        analysis = analyze_candidate(candidate)

        # Create personalized interview plan
        plan = create_interview_plan(
            analysis,
            num_questions=8
        )

        # Safety check
        if not plan.get("topics"):
            return {
                "error": "No interview topics available for this candidate."
            }

        # Create session
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
        session["transcript"] = []

        # First topic
        first_topic = plan["topics"][0]

        curriculum_day = get_curriculum_day(
            first_topic["day"]
        )

        if curriculum_day is None:
            return {
                "error": (
                    f"Curriculum day "
                    f"{first_topic['day']} not found"
                )
            }

        # Generate first AI question
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


    # ========================================================
    # 2. GET EXISTING SESSION
    # ========================================================

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


    # ========================================================
    # 3. INITIALIZE ADAPTIVE FIELDS
    # ========================================================

    session.setdefault("evaluations", [])
    session.setdefault("followups_for_current", 0)
    session.setdefault("total_interactions", 0)
    session.setdefault("transcript", [])


    # ========================================================
    # 4. GET CURRENT QUESTION
    # ========================================================

    current_question_index = session["current_question"]

    current_topic = session["plan"]["topics"][
        current_question_index
    ]

    curriculum_day = get_curriculum_day(
        current_topic["day"]
    )

    if curriculum_day is None:
        return {
            "error": (
                f"Curriculum day "
                f"{current_topic['day']} not found"
            )
        }

    current_question = session["questions"][-1]


    # ========================================================
    # 5. SAVE CANDIDATE ANSWER
    # ========================================================

    answer = request.message

    if not answer:
        return {
            "error": (
                "A message is required "
                "for an existing interview."
            )
        }

    session["answers"].append(answer)

    # Count candidate answer
    session["total_interactions"] += 1


    # ========================================================
    # 6. EVALUATE ANSWER
    # ========================================================

    evaluation = evaluate_answer(
        question=current_question,
        answer=answer,
        candidate=session["candidate"],
        curriculum_day=curriculum_day
    )

    session["evaluations"].append(evaluation)


    # ========================================================
    # 7. SAVE TRANSCRIPT
    # ========================================================

    session["transcript"].append({
        "topic_day": current_topic["day"],
        "topic_title": current_topic["title"],
        "question": current_question,
        "answer": answer,
        "evaluation": evaluation,
        "is_followup": (
            session["followups_for_current"] > 0
        )
    })


    # ========================================================
    # 8. HARD LIMIT: 8 TOTAL ANSWERS
    # ========================================================

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


    # ========================================================
    # 9. ADAPTIVE FOLLOW-UP
    # ========================================================

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


    # ========================================================
    # 10. MOVE TO NEXT CURRICULUM TOPIC
    # ========================================================

    session["current_question"] += 1

    session["followups_for_current"] = 0

    question_number = session["current_question"]


    # ========================================================
    # 11. SAFETY CHECK
    # ========================================================

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


    # ========================================================
    # 12. GENERATE NEXT TOPIC QUESTION
    # ========================================================

    next_topic = session["plan"]["topics"][
        question_number
    ]

    next_curriculum_day = get_curriculum_day(
        next_topic["day"]
    )

    if next_curriculum_day is None:
        return {
            "error": (
                f"Curriculum day "
                f"{next_topic['day']} not found"
            )
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