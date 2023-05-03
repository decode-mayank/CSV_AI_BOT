# Bitcot AI Cookbook
# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

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
