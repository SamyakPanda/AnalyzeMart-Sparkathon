import psycopg2
import csv

def get_connection():
    """Establishes and returns a connection to the PostgreSQL database."""
    return psycopg2.connect(
        dbname="walmart",
        user="postgres",
        password="ishan*1234",
        host="localhost"
    )

def create_inventory_table():
    """Creates the inventory table if it does not exist."""
    conn = get_connection()
    cursor = conn.cursor()
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS inventory (
        product_id INT,
        product_name VARCHAR(255),
        quantity INT,
        store_id INT,
        PRIMARY KEY (product_id, store_id)
    );
    '''
    try:
        cursor.execute(create_table_query)
        conn.commit()
        print("Table 'inventory' created successfully or already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

def upload_inventory_csv(file_path):
    """Uploads data from a CSV file to the inventory table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)  # Read the header row
            
            # Check if the CSV headers match the table columns
            if headers != ['product_id', 'product_name', 'quantity', 'store_id']:
                raise ValueError("CSV headers do not match table columns.")
            
            for row in reader:
                print(f"Inserting row: {row}")  # Debug statement
                cursor.execute(
                    '''
                    INSERT INTO inventory (product_id, product_name, quantity, store_id)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (product_id, store_id) DO UPDATE
                    SET product_name = EXCLUDED.product_name,
                        quantity = EXCLUDED.quantity
                    ''',
                    row
                )
        conn.commit()
        print(f"Data from {file_path} uploaded successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()  # Rollback in case of error
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_inventory_table()
    upload_inventory_csv('inventory.csv')
