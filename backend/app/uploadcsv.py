import psycopg2
import csv

def get_connection():
    return psycopg2.connect(
        dbname="walmart",
        user="postgres",
        password="ishan*1234",
        host="localhost"
    )

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS orders (
        order_id SERIAL PRIMARY KEY,
        customer_id INT,
        product_name VARCHAR(255),
        price_sold_at FLOAT,
        industry VARCHAR(255),
        subgroup VARCHAR(255),
        order_time TIME,
        order_date DATE,
        store_id INT
    );
    '''
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()

def upload_csv(file_path):
    conn = get_connection()
    cursor = conn.cursor()

    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            cursor.execute(
                '''
                INSERT INTO orders (customer_id, product_name, price_sold_at, industry, subgroup, order_time, order_date, store_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ''',
                row[1:]  # Exclude the order_id from CSV
            )
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_table()
    upload_csv('order_history.csv')
