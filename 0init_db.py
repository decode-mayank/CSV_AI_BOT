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
    probability FLOAT NOT NULL DEFAULT 0,
    response_accepted BOOLEAN NOT NULL DEFAULT FALSE,
    response_time SMALLINT NOT NULL,
    time_stamp TIMESTAMP NOT NULL
  );""")
except psycopg2.errors.DuplicateTable:
  print(f"Table chatbot_datas already exist - If you want to drop this table then run DROP TABLE IF EXISTS chatbot_datas;")
  conn.rollback()

try:
  cur.execute('ALTER TABLE chatbot_datas ADD COLUMN "source" text;')
  print("Added source column in database")
except psycopg2.errors.DuplicateColumn:
  print("Source column already exists")


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


