import json
import os
from dotenv import load_dotenv
from app.services.gemini_client import generate_content

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set")



def evaluate_answer(
    question,
    answer,
    candidate,
    curriculum_day
):
    prompt = f"""
You are evaluating a candidate during a technical AI engineering interview.

CANDIDATE
Name: {candidate["member"]["name"]}
Role: {candidate["member"]["jobRole"]}
Experience: {candidate["member"]["yearsExperience"]} years

CURRICULUM
Day: {curriculum_day["day"]}
Title: {curriculum_day["title"]}
Type: {curriculum_day["type"]}

Learning objectives:
{curriculum_day["objectives"]}

INTERVIEW QUESTION
{question}

CANDIDATE ANSWER
{answer}

Evaluate the answer against the curriculum objectives and the interview question.

You must return ONLY valid JSON.

Use this exact structure:

{{
  "score": 0,
  "level": "WEAK",
  "strengths": [],
  "gaps": [],
  "misconceptions": [],
  "follow_up_needed": false,
  "follow_up_focus": ""
}}

Rules:

- score must be an integer from 0 to 10.
- 0-3 = WEAK
- 4-6 = DEVELOPING
- 7-8 = GOOD
- 9-10 = EXCELLENT
- Identify specific strengths from the candidate's answer.
- Identify specific knowledge gaps.
- Identify misconceptions only when they actually exist.
- Do not invent weaknesses that are not supported by the answer.
- Set follow_up_needed to true when the answer has an important gap,
  misconception, or area that should be explored further.
- Set follow_up_focus to the specific concept that should be explored.
- If no follow-up is needed, use an empty string for follow_up_focus.
"""

    text = generate_content(prompt)

    # Remove markdown code fences if Gemini adds them
    if text.startswith("```"):
        text = text.replace("```json", "", 1)
        text = text.replace("```", "")
        text = text.strip()

    return json.loads(text)