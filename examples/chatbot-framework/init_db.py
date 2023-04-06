from dotenv import load_dotenv
from psycopg2.errors import DuplicateTable,DuplicateColumn
from utils import get_db_connection

load_dotenv()

conn,cur = get_db_connection()


def create_response_table():
  try:
    cur.execute("""CREATE TABLE chatbot_datas (
      prompt VARCHAR(500),
      completion VARCHAR(5000),
      probability FLOAT NOT NULL DEFAULT 0,
      response_accepted BOOLEAN NOT NULL DEFAULT FALSE,
      response_time SMALLINT NOT NULL,
      time_stamp TIMESTAMP NOT NULL
    );""")

  except DuplicateTable:
    print(f"Table chatbot_datas already exist - If you want to drop this table then run DROP TABLE IF EXISTS chatbot_datas;")


def alter_response_table():
  try:
    cur.execute('ALTER TABLE chatbot_datas ADD COLUMN "source" text;')
    cur.execute('ALTER TABLE chatbot_datas ALTER COLUMN source TYPE VARCHAR(5000);')
    print("Added source column in database")
  except (DuplicateColumn):
    print("Source column already exists")
  
# Below line of code is to add new column to existing table
# cur.execute('ALTER TABLE chatbot_datas ADD COLUMN "response_accepted" BOOLEAN NOT NULL DEFAULT FALSE;')


if __name__ == '__main__':

  # Open a cursor to perform database operations
  cur = conn.cursor()
  create_response_table()
  alter_response_table()
  conn.commit()
  cur.close()
  conn.close()
