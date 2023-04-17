from dotenv import load_dotenv
from psycopg2.errors import DuplicateTable
from utils import get_db_connection

load_dotenv()

conn, cur = get_db_connection()


def create_response_table():
    try:
        cur.execute("""CREATE TABLE chatbot_datas (
      id SERIAL PRIMARY KEY,
      user_input TEXT,
      bot_response TEXT,
      initial_prompt TEXT,
      initial_response TEXT,
      level1 TEXT,
      level2 TEXT,
      level3 TEXT,
      level4 TEXT,
      response_accepted BOOLEAN NOT NULL DEFAULT FALSE,
      response_time SMALLINT NOT NULL,
      discord_id VARCHAR(50) NOT NULL DEFAULT '',
      cost DECIMAL(5,3) NOT NULL,
      time_stamp TIMESTAMP NOT NULL,
      created_at TIMESTAMP DEFAULT NOW(),
      updated_at TIMESTAMP DEFAULT NOW()
    );""")

    except DuplicateTable:
        print(f"Table chatbot_datas already exist - If you want to drop this table then run DROP TABLE IF EXISTS chatbot_datas;")


if __name__ == '__main__':

    # Open a cursor to perform database operations
    cur = conn.cursor()
    create_response_table()
    conn.commit()
    cur.close()
    conn.close()
