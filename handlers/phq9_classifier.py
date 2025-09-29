import os
import openai
import time

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Final PHQ-9 categories
LABELS = {
    0: "Not at all",
    1: "Several days",
    2: "More than half the days",
    3: "Nearly every day"
}

# Prompt template for LLM
PROMPT_TEMPLATE = """
You are a mental health assistant helping classify PHQ-9 responses. Your goal is to map freeform user input to one of four categories:

- Not at all (0)
- Several days (1)
- More than half the days (2)
- Nearly every day (3)

If the input is vague or ambiguous, ask a conversational follow-up question to clarify frequency — without repeating the category labels. Continue until you are confident in your classification.

Respond in JSON format:
{
  "clarifying_question": "...",  // optional
  "classification": 0-3,         // optional
  "confidence": float            // required
}
"""

def query_llm(conversation: list) -> dict:
    """
    Sends conversation history to OpenAI and returns parsed JSON response.
    """
    messages = [{"role": "system", "content": PROMPT_TEMPLATE}] + conversation

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7
    )

    content = response.choices[0].message.content.strip()
    try:
        return eval(content)
    except Exception:
        return {"confidence": 0.0}

def classify_phq9_response(user_input: str, max_turns: int = 5, confidence_threshold: float = 0.9):
    """
    Uses OpenAI to classify PHQ-9 response with clarification loop.
    """
    conversation = [{"role": "user", "content": f"User input: \"{user_input}\""}]

    for turn in range(max_turns):
        result = query_llm(conversation)

        if result.get("confidence", 0) >= confidence_threshold and "classification" in result:
            label_id = result["classification"]
            return {
                "status": "classified",
                "classification": LABELS[label_id],
                "score": label_id,
                "confidence": round(result["confidence"], 3)
            }

        if "clarifying_question" in result:
            return {
                "status": "clarification_needed",
                "message": result["clarifying_question"],
                "turn": turn + 1
            }

        time.sleep(0.5)  # Optional pacing

    return {
        "status": "uncertain",
        "message": "Unable to confidently classify response after multiple turns."
    }
