from utils import find_what_user_expects, debug_attribute, resmed_chatbot
from constants import MESSAGE_LOG
import pandas as pd

message_log = MESSAGE_LOG
df = pd.read_csv("testcases.csv")
  
def test_product_query(user_input):
    product_response = resmed_chatbot(user_input, message_log, False)
    debug_attribute("product_response",product_response)
    try:
        assert "\n\n" in product_response[0]
        return "Pass"
    except AssertionError:
        return "Fail"
df["output"] = df.apply(lambda row: test_product_query(row["User Input"]), axis=1)
df.to_csv("testcases.csv", index=False)