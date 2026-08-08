import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_curriculum():
    with open(DATA_DIR / "curriculum.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_candidates():
    with open(DATA_DIR / "candidates.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_curriculum_day(day_number):
    curriculum = load_curriculum()

    for day in curriculum["days"]:
        if day["day"] == day_number:
            return day

    return None