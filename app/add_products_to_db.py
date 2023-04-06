import csv

from dotenv import load_dotenv
from psycopg2.errors import DuplicateTable

from utils import get_db_connection

load_dotenv()

conn,cur = get_db_connection()

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
      total_reviews INTEGER,
      tags VARCHAR(500)
    );""")
  
  except DuplicateTable:
    print(f"Table product already exist - If you want to drop this table then run DROP TABLE IF EXISTS product;")

def add_csv_to_db():
  with open('app_products.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) # Skip the header row.
    for row in reader:
        cur.execute(
        "INSERT INTO product VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s) ON CONFLICT (sku) DO UPDATE SET category = EXCLUDED.category, product = EXCLUDED.product, description = EXCLUDED.description, price = EXCLUDED.price, breadcrumb = EXCLUDED.breadcrumb, product_url = EXCLUDED.product_url, money_back = EXCLUDED.money_back, rating = EXCLUDED.rating, total_reviews = EXCLUDED.total_reviews,tags = EXCLUDED.tags",
        row
    )
  

if __name__ == '__main__':

  # Open a cursor to perform database operations
  cur = conn.cursor()
  create_product_table()
  add_csv_to_db()
  conn.commit()
  cur.close()
  conn.close()
