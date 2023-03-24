from chatbot import  find_whether_user_query_is_valid, find_what_user_expects, debug_attribute,resmed_chatbot,find_whether_user_query_is_valid
from constants import MESSAGE_LOG, GENERAL_QUERY, SYMPTOM_QUERY

message_log = MESSAGE_LOG

# For General Query
def test_general():
    user_input = "5 basic things about insomnia"
    product_response = find_what_user_expects(user_input)
    debug_attribute("product_response",product_response)
    assert product_response[3:].strip() in GENERAL_QUERY

# For Symptom Query
def test_symptom():
    user_input = "I have fever and cold"
    product_response = find_what_user_expects(user_input)
    debug_attribute("product_response",product_response)
    assert product_response[3:].strip() in SYMPTOM_QUERY

def test_sleep_apnea():
    user_input = "what is sleep apnea"
    response = find_whether_user_query_is_valid(user_input)
    debug_attribute("test_sleep_apnea",response)
    assert response[:-1].strip() != "I am a Resmed chatbot, I can't help with that"


def test_insomnia():
    user_input = "what is sleep apnea"
    response,_ = resmed_chatbot(user_input,message_log,False)
    debug_attribute("test_insomnia",response)
    assert "Insomnia is a sleep disorder" in response
    