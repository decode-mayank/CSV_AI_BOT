from chatbot import debug_attribute,chatbot
from constants import MESSAGE_LOG
import pandas as pd

message_log = MESSAGE_LOG
df = pd.read_csv("testcases.csv")
  
<<<<<<< HEAD:test_product_queries.py
def test_product_query(user_input):
    product_response = resmed_chatbot(user_input, message_log, False)
=======
def test_product_query():
    user_input = "do you have any adapter?"
    product_response = chatbot(user_input, message_log, False)
>>>>>>> 934cdc5649f227defede41c3540cc9c70ecace43:examples/chatbot-framework/app/tests/test_product_queries.py
    debug_attribute("product_response",product_response)
    try:
        assert "\n\n" in product_response[0]
        return "Pass"
    except AssertionError:
        return "Fail"
df["output"] = df.apply(lambda row: test_product_query(row["User Input"]), axis=1)
df.to_csv("testcases.csv", index=False)