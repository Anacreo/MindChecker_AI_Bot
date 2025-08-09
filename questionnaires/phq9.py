import json

with open("questionnaires/phq9.json", "r") as f:
    PHQ9 = json.load(f)

def get_question(q_num):
    return PHQ9[q_num - 1]["text"]

def get_options(q_num):
    return [[opt] for opt in PHQ9[q_num - 1]["options"]]
