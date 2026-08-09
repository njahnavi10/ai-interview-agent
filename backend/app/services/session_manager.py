sessions = {}


def create_session(session_id, candidate, analysis, plan):
    sessions[session_id] = {
        "candidate": candidate,
        "analysis": analysis,
        "plan": plan,
        "current_question": 0,
        "questions": [],
        "answers": [],
        "evaluations": [],
        "transcript": [],
        "followups_for_current": 0,
        "done": False,
        "feedback": None
    }

    return sessions[session_id]


def get_session(session_id):
    return sessions.get(session_id)


def update_session(session_id, **updates):
    session = sessions.get(session_id)

    if session is None:
        return None

    session.update(updates)
    return session


def session_exists(session_id):
    return session_id in sessions