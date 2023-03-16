import os
import psycopg2
from dotenv import load_dotenv
import csv
from psycopg2.errors import DuplicateTable,DuplicateColumn,InFailedSqlTransaction

load_dotenv()

conn = psycopg2.connect(
        host="localhost",
        database=os.getenv('DB'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'))

# Open a cursor to perform database operations
cur = conn.cursor()


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
    cur.execute('ALTER TABLE chatbot_datas ALTER COLUMN source TYPE VARCHAR(5000);;')
    print("Added source column in database")
  except (DuplicateColumn):
    print("Source column already exists")

def create_product_table():
  try:
    cur.execute("""CREATE TABLE product(
      category VARCHAR(500) NOT NULL,
      sku VARCHAR(500) PRIMARY KEY,
      product VARCHAR(500) NOT NULL,
      description VARCHAR(5000),
      price FLOAT,
      breadcrumb VARCHAR(500),
      product_url VARCHAR(500),
      money_back BOOLEAN,
      rating FLOAT,
      total_reviews INTEGER
    );""")
  
  except DuplicateTable:
    print(f"Table product already exist - If you want to drop this table then run DROP TABLE IF EXISTS product;")

def add_csv_to_db():
  try:
    with open('resmed_products_1.csv', 'r') as f:
      reader = csv.reader(f)
      next(reader) # Skip the header row.
      for row in reader:
          cur.execute(
          "INSERT INTO product VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (sku) DO UPDATE SET category = EXCLUDED.category, product = EXCLUDED.product, description = EXCLUDED.description, price = EXCLUDED.price, breadcrumb = EXCLUDED.breadcrumb, product_url = EXCLUDED.product_url, money_back = EXCLUDED.money_back, rating = EXCLUDED.rating, total_reviews = EXCLUDED.total_reviews",
          row
      )
  except:
    print(f"Issue while adding CSV to DB")

  
# Below line of code is to add new column to existing table
# cur.execute('ALTER TABLE chatbot_datas ADD COLUMN "response_accepted" BOOLEAN NOT NULL DEFAULT FALSE;')

'''
Connect to database in psql
psql postgres -U syed -d bitcotai


To export the table in CSV format:
copy (SELECT * FROM chatbot_datas) to '/Users/bitcot/Downloads/VSCodeProjects/chatgpt/bitcot.ai/a.csv' with csv;
'''

if __name__ == '__main__':

  # Open a cursor to perform database operations
  cur = conn.cursor()
  create_response_table()
  alter_response_table()
  create_product_table()
  add_csv_to_db()
  conn.commit()
  cur.close()
  conn.close()
