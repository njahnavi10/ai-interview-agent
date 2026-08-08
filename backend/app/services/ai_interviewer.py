import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=API_KEY)


def generate_ai_question(topic, candidate, previous_answers):
    prompt = f"""
You are a professional technical interviewer.

Candidate:
Name: {candidate["member"]["name"]}
Role: {candidate["member"]["jobRole"]}
Experience: {candidate["member"]["yearsExperience"]} years

Current interview topic:
{topic["title"]}

Previous candidate answers:
{previous_answers}

Generate ONE technical interview question about the current topic.

Rules:
- Ask a realistic interview question.
- Do not ask multiple questions at once.
- Match the candidate's experience level.
- If previous answers exist, build naturally on them.
- Do not mention that you are an AI.
- Do not provide the answer.
- Keep the question concise.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text.strip()