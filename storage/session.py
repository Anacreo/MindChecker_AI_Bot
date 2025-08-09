_sessions = {}

def update_session(user_id, questionnaire, current_question):
    _sessions[user_id] = {
        "active_questionnaire": questionnaire,
        "current_question": current_question
    }

def get_session(user_id):
    return _sessions.get(user_id, {"active_questionnaire": None, "current_question": 0})
