# Business-Chatbot-with-voice-Assistant

## Setup

####  1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/)

   * Note : 
     - Atleast Python >= 3.7.1 version is required to work with open ai
       - Reference - https://github.com/openai/openai-python#requirements
   
#### 2. Clone this Repository ####

  ``` bash
    git clone https://bitbucket.org/bitcot/bitcot.ai.git
  ```
    
#### 3. Navigate into the Project Directory ####

  ``` bash
     cd bitcot.ai
  ```

#### 4. Install and configure virtualenv - Run below command ####

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

#### 5. To install the requirements ####
  ``` bash
    pip install -r requirements.txt
  ```

#### 6. Make a copy of the example environment variables file ####

  * On Linux/Mac: 

  ``` bash
    $ cp .env.example .env
  ```

  * On Windows:

  ``` powershell
    $ copy .env.example .env
  ```

#### 7. Follow below steps to get secret key from openai, open .env then assign that key to OPENAI_API_KEY 
    
    Login to https://openai.com/ and get API key from https://beta.openai.com/account/api-keys
    
#### 8. To run the Project ####
    python3 bot.py