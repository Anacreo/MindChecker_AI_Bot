import os
import time
import logging
import openai

# Load OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# PHQ-9 frequency categories
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
    Logs input, output, and confidence.
    """
    messages = [{"role": "system", "content": PROMPT_TEMPLATE}] + conversation
    logging.info("🔍 Calling LLM with conversation:")
    for msg in conversation:
        logging.info(f"{msg['role'].upper()}: {msg['content']}")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7
        )
        content = response.choices[0].message.content.strip()
        logging.info(f"📨 LLM raw response: {content}")

        result = eval(content)
        logging.info(f"✅ Parsed result: {result}")

        return result
    except Exception as e:
        logging.error(f"❌ LLM call failed: {e}")
        return {"confidence": 0.0}

def classify_response(user_input: str, max_turns: int = 5, confidence_threshold: float = 0.9):
    """
    Uses OpenAI to classify PHQ-9 response with clarification loop.
    Logs confidence and decision path.
    """
    logging.info(f"🧠 Starting classification for input: '{user_input}'")
    conversation = [{"role": "user", "content": f"User input: \"{user_input}\""}]

    for turn in range(max_turns):
        logging.info(f"🔄 Turn {turn + 1}: querying LLM...")
        result = query_llm(conversation)

        confidence = result.get("confidence", 0.0)
        logging.info(f"📊 Confidence score: {confidence}")

        if confidence >= confidence_threshold and "classification" in result:
            label_id = result["classification"]
            logging.info(f"🎯 Confident classification: {LABELS[label_id]} ({label_id})")
            return {
                "status": "classified",
                "classification": LABELS[label_id],
                "score": label_id,
                "confidence": round(confidence, 3)
            }

        if "clarifying_question" in result:
            logging.info(f"🗣️ Clarification needed: {result['clarifying_question']}")
            return {
                "status": "clarification_needed",
                "message": result["clarifying_question"],
                "turn": turn + 1
            }

        logging.warning("⚠️ No classification or clarification returned. Continuing...")
        time.sleep(0.5)

    logging.error("🚫 Max turns reached without confident classification.")
    return {
        "status": "uncertain",
        "message": "Unable to confidently classify response after multiple turns."
    }
