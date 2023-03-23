from utils import  find_whether_user_query_is_valid, find_what_user_expects, debug_attribute,resmed_chatbot
from constants import MESSAGE_LOG

message_log = MESSAGE_LOG
  
def test_snoring():
    user_input = "can you suggest some snoring products"
    product_response = find_what_user_expects(user_input)
    debug_attribute("product_response",product_response)
    assert product_response == "AI:Product query"
    
def test_sleep_apnea():
    user_input = "what is sleep apnea"
    response = find_whether_user_query_is_valid(user_input)
    debug_attribute("test_sleep_apnea",response)
    assert response[:-1].strip() != "I am a Resmed chatbot, I can't help with that"


def test_insomnia():
    user_input = "what is insomnia"
    response,_ = resmed_chatbot(user_input,message_log,False)
    debug_attribute("test_insomnia",response)
    assert "Insomnia is a sleep disorder" in response
    