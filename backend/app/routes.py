from flask import Blueprint, jsonify
from .db import get_connection

main = Blueprint('main', __name__)

@main.route('/api/analytics', methods=['GET'])
def get_analytics():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Top Products Sold
        cursor.execute("SELECT product_name, COUNT(*) AS count FROM orders GROUP BY product_name ORDER BY count DESC LIMIT 5")
        top_products = cursor.fetchall()

        # Top Industries Sold
        cursor.execute("""
            SELECT industry, COUNT(*) AS count
            FROM orders
            GROUP BY industry
            ORDER BY count DESC
            LIMIT 5
        """)
        top_industries = cursor.fetchall()

        # Top Subgroups in Each Industry
        cursor.execute("""
            SELECT industry, subgroup, COUNT(*) AS count
            FROM orders
            GROUP BY industry, subgroup
            ORDER BY industry, count DESC
        """)
        top_subgroups = cursor.fetchall()

        # Sales in Each Store
        cursor.execute("""
            SELECT store_id, COUNT(*) AS count
            FROM orders
            GROUP BY store_id
        """)
        sales_per_store = cursor.fetchall()

    except Exception as e:
        print("Error fetching analytics data:", e)
        return jsonify({"error": "Error fetching analytics data"}), 500

    finally:
        cursor.close()
        conn.close()

    # Process and format the data
    top_subgroup_data = {}
    for industry, subgroup, count in top_subgroups:
        if industry not in top_subgroup_data:
            top_subgroup_data[industry] = []
        top_subgroup_data[industry].append({"name": subgroup, "count": count})

    data = {
        "topProducts": [{"name": row[0], "count": row[1]} for row in top_products],
        "topIndustries": [{"name": row[0], "count": row[1]} for row in top_industries],
        "topSubgroups": [{"industry": industry, "subgroups": subgroups} for industry, subgroups in top_subgroup_data.items()],
        "salesPerStore": {str(row[0]): row[1] for row in sales_per_store}
    }

    return jsonify(data)

@main.route('/home', methods=['GET'])
def hello():
    return jsonify(message="Hello from Flask!")

@main.route('/api/orders', methods=['GET'])
def get_orders():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "hello": "world",
            "order_id": row[0],
            "customer_id": row[1],
            "product_name": row[2],
            "price_sold_at": row[3],
            "industry": row[4],
            "subgroup": row[5],
            # "order_time": row[6],
            "order_date": row[7],
            "store_id": row[8]
        })
        # print(data)
    return jsonify(data)
