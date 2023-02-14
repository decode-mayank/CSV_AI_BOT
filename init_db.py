import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
        host="localhost",
        database=os.getenv('DB'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'))

# Open a cursor to perform database operations
cur = conn.cursor()

try:
  cur.execute("""CREATE TABLE chatbot_datas (
    prompt VARCHAR(500),
    completion VARCHAR(1000),
    response_accepted BOOLEAN NOT NULL DEFAULT FALSE
  );""")
except psycopg2.errors.DuplicateTable:
  print(f"Table chatbot_datas already exist - If you want to drop this table then run DROP TABLE IF EXISTS chatbot_datas;")

# Below line of code is to add new column to existing table
# cur.execute('ALTER TABLE chatbot_datas ADD COLUMN "response_accepted" BOOLEAN NOT NULL DEFAULT FALSE;')

'''
Connect to database in psql
psql postgres -U syed -d bitcotai


To export the table in CSV format:
copy (SELECT * FROM chatbot_datas) to '/Users/bitcot/Downloads/VSCodeProjects/chatgpt/bitcot.ai/a.csv' with csv;
'''

conn.commit()
cur.close()
conn.close()


