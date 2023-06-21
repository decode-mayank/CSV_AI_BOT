# Bitcot AI
A cutting-edge, artificial intelligence project dedicated to innovating and building AI accelerators for BitCot

## Prerequisites :

#### 1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/)

- Note :
  - Atleast Python >= 3.7.1 version is required to work with open ai
    - Reference - https://github.com/openai/openai-python#requirements

## Setup

#### 1. Generate a new SSH key:
 - open terminal in local machine
 - Paste the following command, replacing "your_email@example.com" with your GitHub email address:
   ```
       ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
 - Press Enter when prompted to specify the file to save the key (accept the default path).
 - At the prompt, type a secure passphrase. For more information, see "Working with SSH key passphrases."
 - Enter a passphrase and confirm it by typing it again.
 - Copy the SSH public key to your clipboard
   ```
      cat ~/.ssh/id_ed25519.pub
   ```
   
#### 2. Add SSH key to GitHub:
 - Click "Settings" in the repository menu
 - Click "New SSH key" or "Add SSH key".
 - Click "Add SSH key" to save.



#### 3. Clone this Repository

```bash
  git clone https://bitbucket.org/bitcot/bitcot.ai.git
```
- with SSH Key to clone
```bash
  git clone git@github.com:bitcot/bitcot.ai.git
``` 

#### 4. Navigate into the Project Directory

```bash
   cd bitcot.ai
```

#### 5. Install and configure virtualenv - Run below command

```bash
    pip install virtualenv
```

- For Linux/Mac

  a) Create virtual env:

  ```bash
   python3 -m venv venv
  ```

  b) Activate the environment:

  ```bash
   bash source venv/bin/activate
  ```

- For Windows

  a) Create Virtual env:

  ```bash
   py -m venv venv
  ```

  b) Activate the environment:

  ```bash
   .\env\Scripts\activate
  ```

#### 6. To install the requirements

```bash
  pip install -r requirements.txt
```

#### 7. Make a copy of the example environment variables file

- On Linux/Mac:

```bash
  $ cp .env.example .env
```

- On Windows:

```powershell
  $ copy .env.example .env
```

#### 8. Follow below steps to get secret key from openai, open .env then assign that key to OPENAI_API_KEY

    Login to https://openai.com/ and get API key from https://beta.openai.com/account/api-keys

#### 9. Open .env and Update OPENAI_API_KEY


### Skip virtual environment and Format python code

- To format the code - Use below command
  ```bash
  $ find . -path './venv' -prune -o -name '*.py' -print | tqdm --unit='file' --total=$(find . -name '*.py' -not -path './venv/*' | wc -l) | xargs -I{} autopep8 --in-place {}
  ```

## Example 1 - Chatbot using gpt 3.5 turbo

- On Linux/Mac:

```bash
  $ python examples/chatbot-using-gpt3.5-turbo/main.py
```

- On Windows:
  If you get python command not found then run with py command

## Example 2 - Chatbot for bitcot website

- On Linux/Mac:

```bash
  $ python examples/chatbot-for-bitcot-website/bot.py
```

- On Windows:
  If you get python command not found then run with py command


## Example 3 - Chatbot Flask API
  1. Change directory to flask_ai
     cd flask_ai
  2. Run flask server
     python app.py
     For more information please check README.md in this path - flask_ai/README.md
  3. Run discord 
     ```bash
      $ python discord_bot.py
    ```
    
    Note: discord requires flask to be running
