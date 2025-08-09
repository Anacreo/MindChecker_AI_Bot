import json
from config import DATA_FILE

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def save_response(user_id, questionnaire, question_num, response):
    data = load_data()
    user = data.setdefault(user_id, {})
    q_data = user.setdefault(questionnaire, {})
    q_data[str(question_num)] = response
    save_data(data)
