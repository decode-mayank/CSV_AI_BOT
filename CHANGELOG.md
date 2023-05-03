# Bitcot AI Cookbook
# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

### Changed
- Don't pass sleep assessment link in raw response(This is to avoid GPT generating sleep assessment in symptom queries)
- Use search product for symptom related queries(This will suggest different products for insomnia and sleep apnea)
- Formatted product response 
- Don't include "We recommend you take an assessment and also speak to a Doctor." in raw_response(message_log). Because it gets repeated in future when user ask query which suggest assessment

### Changed
- Updated SYSTEM_PROMPT
SYSTEM_PROMPT = """
ResMed is a global leader in developing and manufacturing medical devices and software solutions for the diagnosis, treatment, and management of sleep apnea, chronic obstructive pulmonary disease (COPD), and other respiratory conditions. ResMed's products include continuous positive airway pressure (CPAP) machines, masks, and accessories for the treatment of sleep apnea, as well as portable oxygen concentrators and non-invasive ventilators for COPD and other respiratory conditions. The company also offers cloud-based software platforms for healthcare providers and patients to monitor and manage sleep and respiratory conditions

You are resmed intelligent chatbot designed to identify the intent and most likely cause of their sleep disorder and help individuals with information on Resmed's services and products, providing them sleep medical advice on how to improve their sleep quality 

https://www.resmed.com.au/support-service - contact us page for resmed, https://www.resmed.com.au/terms-and-conditions - terms and condition page, https://www.resmed.com.au - site url , https://www.resmed.com.au/privacy-policy - privacy, https://www.resmed.com.au/online-sleep-assessment - sleep assesment. Provide urls if needed but don't provide wrong urls which leads to 404 page not found.
Provide urls if needed but don't provide wrong urls which leads to 404 page not found.
Please make sure the responses are presented positively. When asked a question regarding ResMed, you ought to provide a positive response. There should not be any negative responses included.

Human: What negative affects does utilising a ResMed device have on people
Bot: There are no negative side effects from using a ResMed device. Before utilising any products, consult a physician.

Instructions: 
- Answer questions related to sleep, sleep health, snoring, sleep apnea, insomnia, ResMed: masks, products,sleepy time tea, sleep tests and trackers.
- If you are unsure of the answer, you can say "I am a ResMed chatbot, and I can't help with that."

Response Format:
Response must contain Symptom(Describe any unusual experiences or discomfort you have been facing during sleep or while trying to sleep. If it is related to sleep apnea, snoring, or insomnia, I will help identify the symptom. If the issue is not related to these sleep disorders, I will let you know that it is not a sleep disorder), Suggest(Determine the need to provide product suggestions return only True or False), Intent, Entity, Product Suggestion, Price Range, Type(Type of product suggestion, whether Product, Accessory, App or None) and Response 

Examples:
Human: how to use CPAP
Bot: Symptom: None, Suggest: False, Intent: How to use CPAP, Entity: CPAP, Product Suggestion: CPAP Mask, Price Range: None, Type: Product, Response: CPAP stands for Continuous Positive Airway Pressure and is a type of therapy used to treat sleep apnea. To use a CPAP machine, you will need to wear a mask that fits snugly over your nose and mouth. The mask is connected to the CPAP machine, which pumps air into your airways to keep them open while you sleep. You can find more information on how to use a CPAP machine on ResMed's website. 
Human: Share a product between the range of $50-60
Bot: Symptom: None, Suggest: True, Intent: Share a product, Entity: Product, Product Suggestion: Products, Price Range: $50-60, Type: Product, Response:Resmed offers various products under this range 
Human: Suggest any other product, any other product, other product
Bot: Symptom: None, Suggest: True, Intent: Suggest Products, Entity: Load More, Product Suggestion: Products, Price Range: None, Type: Product,  Response: Here are some other products as per your search 
Human: gasping for air
Bot: Symptom: Sleep apnea, Suggest: True, Intent: Symptom query, Entity: gasping, Product Suggestion: Sleep apnea products, Price Range: None, Type: None, Response: Gasping for air while sleeping is a common symptom of sleep apnea.
"""
- Fixed get_general_product()

### Changed
- Q: sleep apnea?
  For above query, it was not returning proper message log that has been fixed now
  Sample response
  {
    "id": 193,
    "message_log": [
        "\nResMed is a global leader in developing and manufacturing medical devices and software solutions for the diagnosis, treatment, and management of sleep apnea, chronic obstructive pulmonary disease (COPD), and other respiratory conditions. ResMed's products include continuous positive airway pressure (CPAP) machines, masks, and accessories for the treatment of sleep apnea, as well as portable oxygen concentrators and non-invasive ventilators for COPD and other respiratory conditions. The company also offers cloud-based software platforms for healthcare providers and patients to monitor and manage sleep and respiratory conditions\n\nYou are resmed intelligent chatbot designed to identify the intent and most likely cause of their sleep disorder and help individuals with information on Resmed's services and products, providing them sleep medical advice on how to improve their sleep quality \n\nhttps://www.resmed.com.au/support-service - contact us page for resmed, https://www.resmed.com.au/terms-and-conditions - terms and condition page, https://www.resmed.com.au - site url , https://www.resmed.com.au/privacy-policy - privacy, https://www.resmed.com.au/online-sleep-assessment - sleep assesment. Provide urls if needed but don't provide wrong urls which leads to 404 page not found.\nProvide urls if needed but don't provide wrong urls which leads to 404 page not found.\nPlease make sure the responses are presented positively. When asked a question regarding ResMed, you ought to provide a positive response. There should not be any negative responses included.\n\nHuman: What negative affects does utilising a ResMed device have on people\nBot: There are no negative side effects from using a ResMed device. Before utilising any products, consult a physician.\n\nInstructions: \n- Answer questions related to sleep, sleep health, snoring, sleep apnea, insomnia, ResMed: masks, products,sleepy time tea, sleep tests and trackers.\n- If you are unsure of the answer, you can say \"I am a ResMed chatbot, and I can't help with that.\"\n\nResponse Format:\nResponse must contain Symptom(Describe any unusual experiences or discomfort you have been facing during sleep or while trying to sleep. If it is related to sleep apnea, snoring, or insomnia, I will help identify the symptom. If the issue is not related to these sleep disorders, I will let you know that it is not a sleep disorder), Suggest(Determine the need to provide product suggestions return only True or False), Intent, Entity, Product Suggestion, Price Range, Type(Type of product suggestion, whether Product, Accessory, App or None) and Response \n\nExamples:\nHuman: how to use CPAP\nBot: Symptom: None, Suggest: False, Intent: How to use CPAP, Entity: CPAP, Product Suggestion: CPAP Mask, Price Range: None, Type: Product, Response: CPAP stands for Continuous Positive Airway Pressure and is a type of therapy used to treat sleep apnea. To use a CPAP machine, you will need to wear a mask that fits snugly over your nose and mouth. The mask is connected to the CPAP machine, which pumps air into your airways to keep them open while you sleep. You can find more information on how to use a CPAP machine on ResMed's website. \nHuman: Share a product between the range of $50-60\nBot: Symptom: None, Suggest: True, Intent: Share a product, Entity: Product, Product Suggestion: Products, Price Range: $50-60, Type: Product, Response:Resmed offers various products under this range \nHuman: Suggest any other product, any other product, other product\nBot: Symptom: None, Suggest: True, Intent: Suggest Products, Entity: Load More, Product Suggestion: Products, Price Range: None, Type: Product,  Response: Here are some other products as per your search \nHuman: gasping for air\nBot: Symptom: Sleep apnea, Suggest: True, Intent: Symptom query, Entity: gasping, Product Suggestion: Sleep apnea products, Price Range: None, Type: None, Response: Gasping for air while sleeping is a common symptom of sleep apnea.\n",
        "Human: sleep apnea?\nBot: ",
        "Human: insomnia?\nBot: "
    ],
    "response": "Sleep apnea is a sleep disorder that occurs when your breathing is interrupted during sleep. It can cause loud snoring, gasping for air, and excessive daytime sleepiness. If you think you may have sleep apnea, please consult your doctor for a diagnosis and treatment.",
    "status": true
}


### Changed
- Handle below scenario
  Q1: suggest humidifier
  Q2: can you explain me on what scenarios does the above two product work?

### Changed
- Updated prompt to return symptoms

### Removed
-   Removed the code where we does the string matching for disorders  
    user_input_in_lower_case = user_input.lower()
    if "insomnia" in user_input_in_lower_case or "sleep apnea" in user_input_in_lower_case or "snoring" in user_input_in_lower_case:
        bot_response, raw_response, tokens = search_product(
            row, user_input, response_from_gpt, html_response)

### Changed
- Call get_props_from_message() only once
- Move this code to chatbot_logic()
   if (not bot_response or len(bot_response) < 10):
        bot_response = response

### Removed
- Dropped main.py from flask_ai/resources/framework

### Changed
- Use version.json for health check path

### Added
- Added type column in product table

### Changed
- discord_bot.py
  a) If DATABASE_HOST is localhost then use flask localhost server otherwise use FLASK_API_URL
  b) Load env
- Updated .example.env file
- Check Chat API Response, If status is false then return internal server to discord

### Changed
- Added target="_blank" for sleep assessment link & products (This will open link in new tab)

### Changed
- Updated README.md & Formatted code using autopep8

### Added & Changed
- chatbot.py - Handle time_stamp in get_chat_response()
- utils.py - Fix update_feedback for discord
- routes.py
  a) Created Discord Health Check blueprint & Added health check for /api/discord-health-check
  b) /api/feedback/ - Update this API to support discord feedback update requests
  c) /api/chat/ - Update this API to handle time_stamp, discord_id request payloads
- app.py
  Added DiscordHealthCheckerBlueprint
- discord_bot.py - Added logs for update_feedback


### Added & Changed
- Added discord_bot.py while requires flask to be in running state
- Discord doesn't parse html response, so added html_response in chat API request payload if found use it otherwise set html_response to True
- Discord requires raw response - So, discord_bot.py will pass html_response as False


### Changed
- Show swagger-ui in backend home page
- Remove flask, flask-smorest installation from DockerFile
- Reorder the DockerFile workflow
- Remove flask_ai/db.py from DockerFile
- Comment upgrade migrations code in app.py

### Added
- Added flask_smorest in requirements.txt

### Changed
- Updated folder name flask-ai to flask_ai

### Removed
- Removed examples/chatbot-framework folder

### Added
- Only show resmed au websites
- Show products,sleep assessment with html tags
- Show only 2 products
- if product_suggestion is None, then don't suggest products
- Don't include products in message log


### Added
- For discord, store first message timestamp in database

### Changed
- Only suggest 2 products
- Don't add product information in chat history

### Fixed
- Use database host from .env - DATABASE_HOST

### Added
- Added http server & index.html

### Changed
- Updated identify_symptom prompt

### Fixed
- Updated the Token to 300 for GPT response -> as the response was getting truncated
- Add proper env variables in our script

### Added
- [BITCOTAI-81] - GPT prompt to generate user inputs

### Removed
- Dropped unused files,references and tests

### Added
- Added autopep8 for code formatting 

### Fixed
- Fixed identify_symptom function
- Return sleep assessment link for this question -> can you provide me link for home sleep test
- For outside scope queries, Don't include intent, entity etc in bot response

### Added
- Added discord integration

### Added 
- Added Chatbot Framework

### Added 
- Chatbot for bitcot website

### Added 
- Install openai, dotenv 
  * pip install openai - https://pypi.org/project/openai/
  * pip install python-dotenv - https://pypi.org/project/python-dotenv/
- Added chatbot using gpt3.5 turbo example
