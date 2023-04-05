import re

import openai

from debug_utils import debug_attribute,debug_steps
from colors import pr_cyan
from constants import davinci
from resmed.constants import SLEEP_ASSESSMENT_INFO,UNABLE_TO_FIND_PRODUCTS_IN_DB
from resmed.products import product, cheap_products, general_product

def show_products(output):
    prod_response = '\n'
    if(len(output)>0):
        items = output[0]
        output = output if len(output)==1 else output[0:2]
        debug_attribute("DB Output",output)
        if(len(items)==3):
            for prod, url,price in output:
                products = prod + " - " + url + " - $" + str(price)
                prod_response += products + "\n"
    return prod_response

def get_general_product(row,user_input,level):
    output, response_token_product = general_product(row,user_input,level)

    if len(output) == 0:
        bot_response = UNABLE_TO_FIND_PRODUCTS_IN_DB
    else:
        bot_response = show_products(output)
    return bot_response,response_token_product


def get_products(row,user_input,query_to_db):
    prod_response=""
    if "cheap" in user_input or "cheapest" in user_input:
        output,response_token_product = cheap_products(row,user_input,level=3)
        prod_response += show_products(output)
    else:
        response,response_token_product = get_general_product(row,query_to_db,level=3)
        prod_response += response
    return prod_response,response_token_product

def identify_symptom(row,user_input,level): 
    PROMPT,TOKENS,TEMPERATURE,MODEL,STOP = """Snoring, sleep apnea, and insomnia are all different sleep disorders with distinct symptoms and causes. Here are some differences that may help you differentiate between the three:
    Snoring:Characterized by loud, rhythmic breathing sounds during sleep,Usually harmless, although it can still disrupt your sleep or your partner's sleep Typically caused by a partial obstruction in the airway, often due to relaxed muscles in the throat or nasal congestion,Usually associated with pauses in breathing or gasping sensations during sleep,Change in the level of attention, concentration, or memory.
    Sleep apnea:Characterized by pauses in breathing or shallow breaths during sleep,Often accompanied by loud snoring and gasping or choking sensations during sleep,Can lead to excessive daytime sleepiness,Being Overweight(adds fat around the neck and airway),Having inflamed tonsils and adenoids,Having blocked nose due to allergy or cold,Structural problem with shape of the nose, neck or jaw,Frequently urinating at night,Waking up with night sweats,High blood pressure,Mood swings,Impotence and reduced sex drive.
    Insomnia:A sleep disorder characterized by difficulty falling asleep,staying asleep,or waking up too early in the morning,Often associated with anxiety, stress, or other psychological factors, as well as medical conditions or medications,Can lead to excessive daytime sleepiness, fatigue, irritability, difficulty concentrating, and other health problems,Making more mistakes or having accidents,Feel tired or sleepy during the day.
    Extract intent from user input.
    Intent can be Sleep Apnea, Insomnia, Snoring, Not a sleep disorder, Question
    Q: Sore throat on awakening A: Snoring Q: Excessive daytime sleepiness A: Snoring Q: I have fever A: Not a sleep disorder Q: Mood Swings A: Sleep Apnea Q: Difficulty staying asleep A: Insomnia Q: I have insomnia A: Not a sleep disorder Q: Find symptom sleep apnea A: Not a sleep disorder  Q: what should I do when not getting sleep in middle of the night A: Question Q: Find symptom {user_input}? A: """,100,0,davinci,["Q: ", "A: "]
    # Multi shot learning
    response = openai.Completion.create(
    model=MODEL,
    prompt=PROMPT,
    max_tokens=TOKENS,
    temperature=TEMPERATURE,
    stop=STOP
    )
    debug_steps(row,f"{level} - {identify_symptom.__name__} - {response}, Additional information: Model-{MODEL},Tokens-{TOKENS}, TEMPERATURE-{TEMPERATURE},STOP-{STOP},PROMPT-{PROMPT}",level)
    
    response_text = response.choices[0].text.strip()
    response_token_symptom = response.usage['total_tokens']
    return response_text, response_token_symptom


def chatbot_logic(row,user_input,response_from_gpt):
    raw_response = response_from_gpt
    response,intent,entity,product_suggestion,price_range = get_props_from_message(response_from_gpt)
    product_suggestion=product_suggestion.lower().replace("resmed","")
    debug_attribute("Response",response)
    debug_attribute("intent",intent)
    debug_attribute("entity",entity)
    debug_attribute("product_suggestion",product_suggestion)
    debug_attribute("price_range",price_range)
    bot_response = ""
    tokens = 0
    
    # elif(intent=="None" or entity=="" or product_suggestion is None):
    #     # We will reach this elif on this query - Is diabetes a disease?
    #     bot_response = RESPONSE_FOR_INVALID_QUERY
    #     raw_response = RESPONSE_FOR_INVALID_QUERY
    symptom,symptom_tokens = identify_symptom(row,user_input,level=2)
    found_symptom = symptom=="Sleep Apnea" or symptom=="Insomnia" or symptom=="Snoring"
    if found_symptom:
        debug_attribute("Identify symptom",symptom)
        tokens = symptom_tokens
        debug_steps(row,"Found symptom & suggest products",level=4)
        MSG = f"This appears to be a condition called {symptom}.It is a fairly common condition, which can be addressed. We recommend you take an assessment and also speak to a Doctor."        
        # We found out symptom of the user. So, let's override the response came from chatgpt
        bot_response= f"{MSG}\n{SLEEP_ASSESSMENT_INFO}"
        raw_response = bot_response
        
        output,prod_tokens = product(row,symptom,level=3)
        prod_response = show_products(output)
        
        # Add product response to bot_response, raw_response
        bot_response += prod_response
        raw_response = raw_response + prod_response
        tokens += prod_tokens
    else:
        # We will reach this block when we ask the question like Is diabetes a disease?
        query_to_db = ""
        # if "None" in price_range:
        query_to_db=f"{entity},{product_suggestion}"
        # else:
        #     query_to_db=f"{price_range}"
        debug_attribute("query_to_db",query_to_db)
        prod_response, response_token_product=get_products(row,user_input,query_to_db)
        print("->>>>>> Check here",prod_response)
        tokens = response_token_product
        if "$" in response:
            # What is the price of BongoRx Starter Kit
            response = ""
            raw_response=""
        bot_response = response + prod_response
        raw_response = raw_response + prod_response
        
    return bot_response,raw_response,tokens
    

def extract_data(pattern,message):
    results = re.search(pattern, message)
    return results.group(1) if results else ""

def get_props_from_message(message):
    response = message.split("Intent")[0]
    intent,entity,product_suggestion="","",""
    # Extracting the Intent
    intent = extract_data(r'Intent: (.*), Entity', message)
    # Extracting the Entity
    entity = extract_data(r'Entity: (.*), Product Suggestion', message)
    # Extracting the Product Suggestion
    product_suggestion = extract_data(r'Product Suggestion: (.*), Price Range', message)
    # Extract price range
    price_range = extract_data(r'Price Range:\s*(.*)', message)
    
    return response,intent,entity,product_suggestion,price_range

# print(get_props_from_message("""Here are some tips to help you get a good night's sleep: 
# 1. Stick to a regular sleep schedule - go to bed and wake up at the same time every day. 
# 2. Avoid caffeine, nicotine, and alcohol before bed. 
# 3. Exercise regularly, but not too close to bedtime. 
# 4. Avoid large meals and beverages late at night. 
# 5. Relax before bed by taking a warm bath or reading a book. 
# 6. Make sure your bedroom is dark, quiet, and comfortable. 
# 7. If you can't sleep, get out of bed and do something relaxing until you feel tired. 
# Intent: Healthy Sleep Tips, Entity: Healthy Sleep Tips, Product Suggestion: Resmed, Price Range: None."""))