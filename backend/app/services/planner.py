def create_interview_plan(candidate_analysis, num_questions=8):
    skipped = candidate_analysis.get("skipped_topics", [])
    struggled = candidate_analysis.get("struggled_topics", [])
    completed = candidate_analysis.get("completed_topics", [])

    plan = []

    # Priority 1: skipped topics
    for topic in skipped:
        plan.append({
            "day": topic["day"],
            "title": topic["title"],
            "reason": "Candidate skipped this topic",
            "priority": "high"
        })

    # Priority 2: topics that required multiple attempts
    for topic in struggled:
        if not any(item["day"] == topic["day"] for item in plan):
            plan.append({
                "day": topic["day"],
                "title": topic["title"],
                "reason": f"Candidate required {topic['attempts']} attempts",
                "priority": "high"
            })

    # Priority 3: completed topics
    for topic in completed:
        if not any(item["day"] == topic["day"] for item in plan):
            plan.append({
                "day": topic["day"],
                "title": topic["title"],
                "reason": "Candidate completed this topic",
                "priority": "normal"
            })

    return {
        "total_questions": num_questions,
        "topics": plan[:num_questions]
    }