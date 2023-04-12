# Bitcot AI Cookbook

## Prerequisites:
####  1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/)

   * Note : 
     - Atleast Python >= 3.7.1 version is required to work with open ai
       - Reference - https://github.com/openai/openai-python#requirements

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
    
#### 7. Open .env and Update OPENAI_API_KEY


## Example 1 - Chatbot using gpt 3.5 turbo
 * On Linux/Mac: 

  ``` bash
    $ python examples/chatbot-using-gpt3.5-turbo/main.py
  ```

  * On Windows:
    If you get python command not found then run with py command

## Example 2 - Chatbot for bitcot website
 * On Linux/Mac: 

  ``` bash
    $ python examples/chatbot-for-bitcot-website/bot.py
  ```

  * On Windows:
    If you get python command not found then run with py command

## Example 3 - Chatbot framework
   Please check the readme at examples/chatbot-framework/README.md
 
### To navigate to cookbook

   [cookbook](docs/cookbook)

   To navigate to common documentation [documentation](docs/documentation.md)