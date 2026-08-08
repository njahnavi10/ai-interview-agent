import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=API_KEY)


def generate_final_feedback(
    candidate,
    questions,
    answers,
    evaluations
):
    interview_data = []

    for i in range(len(questions)):
        interview_data.append({
            "question": questions[i],
            "answer": answers[i] if i < len(answers) else "",
            "evaluation": (
                evaluations[i]
                if i < len(evaluations)
                else {}
            )
        })

    prompt = f"""
You are a senior technical interviewer providing final feedback
after an enterprise AI engineering interview.

CANDIDATE
Name: {candidate["member"]["name"]}
Role: {candidate["member"]["jobRole"]}
Experience: {candidate["member"]["yearsExperience"]} years

INTERVIEW DATA
{json.dumps(interview_data, indent=2)}

Analyze the complete interview and return ONLY valid JSON.

Use exactly this structure:

{{
  "overall_score": 0,
  "technical_strengths": [],
  "knowledge_gaps": [],
  "topics_to_revisit": [],
  "communication_assessment": "",
  "recommendation": "",
  "summary": ""
}}

Rules:

- overall_score must be between 0 and 10.
- Base the score on the evaluations provided.
- Do not invent strengths or weaknesses.
- technical_strengths should contain specific demonstrated strengths.
- knowledge_gaps should contain specific areas where the candidate
  showed incomplete or weak understanding.
- topics_to_revisit should identify curriculum topics that need
  additional study.
- communication_assessment should describe clarity, structure,
  technical precision, and completeness of the candidate's answers.
- recommendation should be actionable and suitable for the candidate.
- summary should provide a concise overall assessment.
- Return ONLY JSON.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "", 1)
        text = text.replace("```", "")
        text = text.strip()

    return json.loads(text)