import json

with open("questionnaires/phq9.json", "r") as f:
    PHQ9 = json.load(f)

def get_question(q_num):
    return PHQ9[q_num - 1]["text"]

def get_options(q_num):
    return [[opt] for opt in PHQ9[q_num - 1]["options"]]

def evaluate_phq9_responses(responses):
    """
    Takes a list of integers representing PHQ-9 responses (0–3 per question).
    Returns total score and severity interpretation.
    """
    if len(responses) != 9:
        raise ValueError("PHQ-9 requires exactly 9 responses.")

    total_score = sum(responses)

    if total_score <= 4:
        severity = "Minimal or none"
    elif total_score <= 9:
        severity = "Mild"
    elif total_score <= 14:
        severity = "Moderate"
    elif total_score <= 19:
        severity = "Moderately severe"
    else:
        severity = "Severe"

    suicide_risk = responses[8] >= 1  # Question 9 is about suicidal ideation

    return {
        "total_score": total_score,
        "severity": severity,
        "suicide_risk": suicide_risk
    }
