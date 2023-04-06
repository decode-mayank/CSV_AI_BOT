from chatbot import debug_attribute,chatbot
from constants import MESSAGE_LOG

message_log = MESSAGE_LOG
  
def test_product_query():
    user_input = "do you have any adapter?"
    product_response = chatbot(user_input, message_log, False)
    debug_attribute("product_response",product_response)
    assert "\n\n" in product_response[0]

    