# Resmed-Chatbot-for-knowledge-hub

## Prerequisites:
####  1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/)

   * Note : 
     - Atleast Python >= 3.7.1 version is required to work with open ai
       - Reference - https://github.com/openai/openai-python#requirements

#### 2. Install postgresql ####
    * Reference - https://www.postgresql.org/download/
  

## Setup

#### 1. Clone this Repository ####

  ``` bash
    git clone https://bitbucket.org/bitcot/bitcot.ai.git
  ```
    
#### 2. Navigate into the Project Directory ####

  ``` bash
     cd bitcot.ai
  ```

#### 3. Install and configure virtualenv - Run below command ####

  ``` bash
      pip install virtualenv
  ```

   * For Linux/Mac
   
     a) Create virtual env:
       ``` bash
        python3 -m venv venv
       ```

     b) Activate the environment:
       ``` bash
        bash source venv/bin/activate
       ```

   * For Windows

     a) Create Virtual env:
       ``` bash
        py -m venv venv 
       ```

     b) Activate the environment:
       ``` bash
        .\env\Scripts\activate 
       ```

#### 4. To install the requirements ####
  ``` bash
    pip install -r requirements.txt
  ```

#### 5. Make a copy of the example environment variables file ####

  * On Linux/Mac: 

  ``` bash
    $ cp .env.example .env
  ```

  * On Windows:

  ``` powershell
    $ copy .env.example .env
  ```

#### 6. Follow below steps to get secret key from openai, open .env then assign that key to OPENAI_API_KEY 
    
    Login to https://openai.com/ and get API key from https://beta.openai.com/account/api-keys
    
#### 7. Create database ####
    * On Linux/Ubuntu: 
    ``` bash
      $ sudo -u postgres psql -c "CREATE DATABASE bitcotai"
    ```

    * On Mac: 
    ``` bash
      $ psql postgres -c "CREATE DATABASE bitcotai"
    ```

#### 8. Run 0init_db.py - This will create table in bitcotai database ####
        python 0init_db.py

#### 9. Scrape knowledge hub site ####
    scrapy runspider 1scrape_knowledge_hub.py -O knowledge_hub.csv

#### 10. Scrape resmed products ####
    scrapy runspider 2scrape_resmed_products.py -O resmed_products.csv

#### 11. Change CSV to spreadsheet and create each sheet for type ####  
 
#### 12. Generate embedding file ####  
python 3get_all_embeddings.py

#### 13. Run the chatbot ####
a) To run chatbot as script - Run main file 
python main.py

b) To run chatbot as API - Run api file
uvicorn api:app
Default port is 8000

To use other ports
uvicorn api:app --port 8001
