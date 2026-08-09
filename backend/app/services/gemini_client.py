import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=API_KEY)


def generate_content(prompt, max_retries=2):
    """
    Centralized Gemini API wrapper.

    Handles temporary 503 errors and rate limits without
    crashing the FastAPI application.
    """

    for attempt in range(max_retries + 1):

        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            return response.text.strip()

        except errors.ClientError as e:

            # 429 = quota/rate limit
            if e.code == 429:
                if attempt < max_retries:
                    wait_time = 10 * (attempt + 1)
                    time.sleep(wait_time)
                    continue

                raise RuntimeError(
                    "Gemini API quota exceeded. "
                    "Please try again later."
                )

            raise

        except errors.ServerError as e:

            # 503 = temporary Gemini availability issue
            if e.code == 503 and attempt < max_retries:
                wait_time = 5 * (attempt + 1)
                time.sleep(wait_time)
                continue

            raise RuntimeError(
                "Gemini service is temporarily unavailable."
            )

        except Exception as e:
            raise RuntimeError(
                f"Gemini request failed: {str(e)}"
            )