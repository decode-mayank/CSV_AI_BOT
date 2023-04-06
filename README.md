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

c) To launch chabot UI - Run output.py
python output.py


### Tests ###

1. We use pytest to run automated test
   Test file should have prefix test_

   To run test: pytest
   To run test with print messages: pytest -s

   If you face any error with pytest:
   Example: 
   '''
    Sample log
    (venv) bitcot@bitcots-MacBook-Pro bitcot.ai % pytest                  
    ===================================================== test session starts =====================================================
    platform darwin -- Python 3.10.4, pytest-7.1.2, pluggy-1.0.0
    rootdir: /Users/bitcot/Downloads/VSCodeProjects/chatgpt/bitcot.ai
    plugins: anyio-3.6.1, Faker-14.2.0, workflow-1.6.0
    collecting ... 
    collected 0 items / 1 error                                                                                                   

    =========================================================== ERRORS ============================================================
    _______________________________________________ ERROR collecting test_utils.py ________________________________________________
    ImportError while importing test module '/Users/bitcot/Downloads/VSCodeProjects/chatgpt/bitcot.ai/test_utils.py'.
    Hint: make sure your test modules/packages have valid Python names.
    Traceback:
    /Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
        return _bootstrap._gcd_import(name[level:], package, level)
    test_utils.py:1: in <module>
        from utils import  find_whether_user_query_is_valid, find_what_user_expects
    utils.py:6: in <module>
        import openai
    E   ModuleNotFoundError: No module named 'openai'
    =================================================== short test summary info ===================================================
    ERROR test_utils.py
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    ====================================================== 1 error in 0.53s =======================================================
    (venv) bitcot@bitcots-MacBook-Pro bitcot.ai % deactivate
  '''
  Solution: https://stackoverflow.com/questions/35045038/how-do-i-use-pytest-with-virtualenv#:~:text=The%20reason%20is%20that%20the,installed%20within%20your%20virtual%20environment.


#### References ####
1. Completion - https://platform.openai.com/docs/api-reference/completions 
2. Chat Completion - https://platform.openai.com/docs/api-reference/chat/create