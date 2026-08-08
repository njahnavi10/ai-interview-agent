def analyze_candidate(candidate):
    member = candidate["member"]
    missions = candidate.get("missions", [])
    signals = candidate.get("signals", {})

    completed = []
    skipped = []
    struggled = []

    for mission in missions:
        if mission.get("skipped"):
            skipped.append({
                "day": mission["day"],
                "title": mission["title"]
            })
            continue

        if mission.get("passed"):
            completed.append({
                "day": mission["day"],
                "title": mission["title"],
                "attempts": mission.get("attempts", 1)
            })

            if mission.get("attempts", 1) > 1:
                struggled.append({
                    "day": mission["day"],
                    "title": mission["title"],
                    "attempts": mission["attempts"]
                })

    return {
        "candidate": {
            "id": member["id"],
            "name": member["name"],
            "jobRole": member["jobRole"],
            "yearsExperience": member["yearsExperience"],
            "education": member["education"],
            "status": member["status"]
        },
        "completed_topics": completed,
        "skipped_topics": skipped,
        "struggled_topics": struggled,
        "learning_signals": signals
    }