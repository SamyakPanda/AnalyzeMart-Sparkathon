import csv
from backend.app.db import get_connection
def generate_store_coordinates():
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        query = "SELECT DISTINCT store_id FROM orders"
        cursor.execute(query)
        stores = cursor.fetchall()
        
        with open('store_coordinates.csv', 'w', newline='') as csvfile:
            fieldnames = ['store_id', 'latitude', 'longitude']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for store in stores:
                writer.writerow({'store_id': store[0], 'latitude': '', 'longitude': ''})
                
        print("store_coordinates.csv has been generated. Please fill in the latitude and longitude for each store.")
    
    except Exception as e:
        print(f"Error generating store coordinates file: {e}")
    
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    generate_store_coordinates()
