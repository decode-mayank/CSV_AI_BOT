from Resmed.file import NEW_INSTRUCTIONS

MESSAGE_LOG = [
      {"role":"system","content": NEW_INSTRUCTIONS},
] 


# Product Suggestion: CPAP Mask.
# Intent: How to use CPAP, Entity: CPAP,

GENERAL_QUERY = "General"
SYMPTOM_QUERY = "Symptom"
PRODUCT_QUERY = "Product"
PROGRAM_QUERY = "Program"
GENERAL_PRODUCT_QUERY = "GeneralProduct"

# TextCompletionModels
davinci="text-davinci-003"
babbage="text-babbage-001"


# ChatCompletionModels
turbo="gpt-3.5-turbo"
      
# EmbeddingModels
ada="text-embedding-ada-002"


LOG = "log"
INITIAL_PROMPT = "initial_prompt"
INITIAL_RESPONSE = "initial_response"
COST = "cost"

fields_dict = {1:2,2:3,3:4,4:5,INITIAL_PROMPT:6,INITIAL_RESPONSE:7,COST:8,LOG:9}

SEPARATORS = f"{'*' * 12}\n"