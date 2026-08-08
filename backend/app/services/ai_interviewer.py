import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=API_KEY)


def generate_ai_question(topic, candidate, previous_answers, curriculum_day):
    prompt = f"""
You are a professional technical interviewer conducting an
enterprise AI engineering interview.

CANDIDATE
Name: {candidate["member"]["name"]}
Role: {candidate["member"]["jobRole"]}
Experience: {candidate["member"]["yearsExperience"]} years

CURRICULUM TOPIC
Day: {curriculum_day["day"]}
Title: {curriculum_day["title"]}
Type: {curriculum_day["type"]}

Tools:
{curriculum_day["tools"]}

Learning objectives:
{curriculum_day["objectives"]}

PREVIOUS ANSWERS
{previous_answers}

Your task is to ask ONE realistic technical interview question.

Rules:
- Assess the candidate against the curriculum objectives.
- Match the candidate's experience level.
- Prefer practical engineering scenarios over definitions.
- If previous answers exist, build naturally on them.
- Do not ask multiple questions.
- Do not provide the answer.
- Do not mention that you are an AI.
- Keep the question concise.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text.strip()