import os
import logging
from openai import OpenAI

# Optional: enable logging
logger = logging.getLogger(__name__)

# Load API key from Render environment variable
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

def classify_response(user_input):
    system_prompt = """
You are a mental health assistant helping users complete the PHQ-9 questionnaire.

Given a user's freeform response, classify it into one of:
- Not at all (0)
- Several days (1)
- More than half the days (2)
- Nearly every day (3)

Respond ONLY with the selected option and score.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.exception(f"PHQ-9 classification failed for input: {user_input}")
        return "⚠️ Unable to classify response. Please try again."
