from chatbot import find_what_user_expects, debug_attribute,resmed_chatbot
from constants import MESSAGE_LOG

message_log = MESSAGE_LOG
  
def test_product_query():
    user_input = "do you have any adapter?"
    product_response = resmed_chatbot(user_input, message_log, False)
    debug_attribute("product_response",product_response)
    assert "\n\n" in product_response[0]

    