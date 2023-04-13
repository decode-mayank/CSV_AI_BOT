from chatbot import find_what_user_expects, debug_attribute
from constants import MESSAGE_LOG, GENERAL_QUERY, SYMPTOM_QUERY, PROGRAM_QUERY

message_log = MESSAGE_LOG

# For General Query


def test_general():
    breakpoint()
    user_input = "Do I need a referral for a Medicare-rebated sleep test?"
    product_response = find_what_user_expects(None, user_input, None)
    print(product_response[0])
    debug_attribute("product_response", product_response)
    assert product_response[0].strip() in GENERAL_QUERY


def test_symptom():
    user_input = "I have fever and cold"
    product_response = find_what_user_expects(None, user_input, None)
    print(product_response[0])
    debug_attribute("product_response", product_response)
    assert product_response[0].strip() in SYMPTOM_QUERY


def test_program():
    breakpoint()
    user_input = "factorial program"
    product_response = find_what_user_expects(None, user_input, None)
    print(product_response[0])
    debug_attribute("product_response", product_response)
    assert product_response[0].strip() in PROGRAM_QUERY


# For Symptom Query
# def test_symptom():
#     user_input = "I have fever and cold"
#     product_response = find_what_user_expects(user_input, level=True)
#     debug_attribute("product_response",product_response)
#     assert product_response[3:].strip() in SYMPTOM_QUERY

# def test_sleep_apnea():
#     user_input = "what is sleep apnea"
#     response = find_whether_user_query_is_valid(user_input)
#     debug_attribute("test_sleep_apnea",response)
#     assert response[:-1].strip() != "I am a Resmed chatbot, I can't help with that"


# def test_insomnia():
#     breakpoint()
#     user_input = "what is sleep apnea"
#     response,_ = resmed_chatbot(user_input,message_log,False)
#     debug_attribute("test_insomnia",response)
#     assert "Sleep apnea is a sleep disorder" in response
