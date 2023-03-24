from chatbot import  find_whether_user_query_is_valid, find_what_user_expects, debug_attribute,resmed_chatbot
from constants import MESSAGE_LOG

message_log = MESSAGE_LOG

def test_python():
    user_input = "what is python"
    user_response = find_whether_user_query_is_valid(user_input)
    debug_attribute("user_response",user_response)
    expected_response = "I am a ResMed chatbot, I can't help with that"
    assert user_response[:-1].strip().casefold() == expected_response.casefold()
    

def test_advantages_python():
    user_input = "Advantages of python"
    user_response = find_what_user_expects(user_input)
    debug_attribute("user_response",user_response)
    assert user_response == "AI:General query" or "AI:Program query"


