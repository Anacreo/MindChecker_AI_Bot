import spacy

nlp = spacy.load("en_core_web_sm")

# Define keyword clusters for each PHQ-9 score
score_keywords = {
    0: ["not at all", "never", "none", "nope"],
    1: ["several days", "sometimes", "occasionally", "not much", "barely", "a little"],
    2: ["more than half", "often", "frequently"],
    3: ["nearly every day", "always", "daily", "constantly"]
}

def interpret_response(text):
    doc = nlp(text.lower())
    for score, keywords in score_keywords.items():
        for keyword in keywords:
            if keyword in doc.text:
                return score

    # Fallback: use sentiment or ask for clarification
    sentiment = doc._.polarity if hasattr(doc._, "polarity") else None
    return None
