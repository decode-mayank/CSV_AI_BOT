# Bitcot AI Cookbook
# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

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
