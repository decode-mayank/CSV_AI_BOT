# Resmed Chatbot
# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

### Changed
- Optimized chatbot code
- Include completion payload and response information in debug csv
- For product search, Include breadcrumb, product in tags 
- Added logs for the product response

### Added 
- Added an option to write logs in csv

### Added 
- pip install pytest ( To test our pytest code)

### Changed
- In resmed embeddings, we use completion column to find symptom - It should be always in lowercase - eg: sleep apnea, snoring, insomnia
- In resmed products, we use category column to match symptom - It should be always in lowercase - eg: sleep apnea, snoring, insomnia

### Removed
- Dropped colorama use default color ANSI

### Added 
- pip install sqlparse (Used to parse sql statement returned by chatgpt)
- pip install openai --upgrade (Upgraded openai)
- pip install discord (To connect to discord)

### Added 
- [BITCOTAI-42] - Added new column "source" in DB
- cur.execute('ALTER TABLE chatbot_datas ADD COLUMN "source" text;')

### Changed
- [BITCOTAI-43] - Updated prompt with resmed domain to stop to suggest product outside of ResMed

### Changed
- When we answer query with help of embedding then use EmbeddedBot: as prefix otherwise Bot:

### Changed
- [BITCOTAI-44] - Embed entire knowledge hub records

### Added
- [BITCOTAI-43] - Don't answer to the outside context queries(outside ResMed products)

### Added
- [BITCOTAI-35] - Created UI for resmed chatbot using gradio
- pip install gradio

