from utils import resmed_chatbot, call_chat_completion_api, find_whether_user_query_is_valid, RESPONSE_FOR_INVALID_QUERY, find_what_user_expects
import pytest
from unittest import TestCase
import json
from utils import resmed_chatbot



def test_resmed_chatbot():
    #breakpoint()
    user_input = "can you suggest some snoring products"
    find_what_user_expects(user_input)
    print(find_what_user_expects(user_input))
    if find_what_user_expects(user_input) == "AI:General query":
        print(find_what_user_expects(user_input))
        response = find_whether_user_query_is_valid(user_input)
        assert response[:-1] != "I am a Resmed chatbot, I can't help with that"

def test_resmed_chatbot():
    user_input = "what is sleep apnea"
    response = find_whether_user_query_is_valid(user_input)
    print(response[:-1])
    print(len(response))
    assert response[:-1].strip() != "I am a Resmed chatbot, I can't help with that"
