import psycopg2
from psycopg2 import OperationalError

def get_connection():
    try:
        conn = psycopg2.connect(
            dbname="Walmart",
            user="postgres",
            password="ishan*1234",
            host="localhost"
        )
        print("Database connection successful!")
        return conn
        # conn.close()
    except OperationalError as e:
        print(f"The error '{e}' occurred")

# if __name__ == "__main__":
#     get_connection()

