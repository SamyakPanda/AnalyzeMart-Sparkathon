import psycopg2
import csv

def get_connection():
    return psycopg2.connect(
        dbname="walmart",
        user="postgres",
        password="ishan*1234",
        host="localhost"
    )

def create_supply_demand_table():
    conn = get_connection()
    cursor = conn.cursor()
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS product_supply_demand (
        id SERIAL PRIMARY KEY,
        product_category VARCHAR(255),
        sub_category VARCHAR(255),
        product_name VARCHAR(255),
        price_of_commodity FLOAT,
        firm_goals VARCHAR(50),
        price_of_inputs FLOAT,
        technology VARCHAR(50),
        government_policy VARCHAR(50),
        expectations VARCHAR(50),
        prices_of_other_commodities FLOAT,
        number_of_firms INT,
        natural_factors VARCHAR(50),
        supply_demand VARCHAR(50)
    );
    '''
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()

def upload_product_supply_demand_csv(file_path):
    conn = get_connection()
    cursor = conn.cursor()

    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            cursor.execute(
                '''
                INSERT INTO product_supply_demand (
                    product_category, sub_category, product_name, price_of_commodity, 
                    firm_goals, price_of_inputs, technology, government_policy, 
                    expectations, prices_of_other_commodities, number_of_firms, 
                    natural_factors, supply_demand
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''',
                row
            )
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_supply_demand_table()
    upload_product_supply_demand_csv('product_supply_demand.csv')
