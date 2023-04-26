import csv
import os

import psycopg2
from dotenv import load_dotenv


load_dotenv()

conn = psycopg2.connect(host=os.getenv("DATABASE_HOST"),
                        database=os.getenv('DATABASE_NAME'),
                        user=os.getenv('DATABASE_USER'),
                        password=os.getenv('DATABASE_PASSWORD'))
cur = conn.cursor()


def add_csv_to_db():
    with open('products.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row.
        for row in reader:
            cur.execute(
                "INSERT INTO product VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s) ON CONFLICT (sku) DO UPDATE SET category = EXCLUDED.category, product = EXCLUDED.product, description = EXCLUDED.description, price = EXCLUDED.price, breadcrumb = EXCLUDED.breadcrumb, product_url = EXCLUDED.product_url, money_back = EXCLUDED.money_back, rating = EXCLUDED.rating, total_reviews = EXCLUDED.total_reviews,tags = EXCLUDED.tags",
                row
            )


if __name__ == '__main__':

    # Open a cursor to perform database operations
    cur = conn.cursor()
    add_csv_to_db()
    conn.commit()
    cur.close()
    conn.close()
