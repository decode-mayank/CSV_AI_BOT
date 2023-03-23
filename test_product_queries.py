from utils import find_what_user_expects, debug_attribute
from constants import MESSAGE_LOG

message_log = MESSAGE_LOG
  
def test_product_query():
    user_input = "can you suggest some snoring products"
    product_response = find_what_user_expects(user_input)
    debug_attribute("product_response",product_response)
    assert product_response == "AI:Product query"

    