import string
from flask import Flask, jsonify, request
from .routes import main
from flask_cors import CORS
from .db import get_connection
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import warnings
import csv
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../order_history.csv')

# Create a pivot table to summarize orders by Customer ID and Product Name
customer_product_matrix = df.pivot_table(index='Customer ID', columns='Product Name', values='Price Sold At', aggfunc='sum', fill_value=0)

# Perform SVD
svd = TruncatedSVD(n_components=20, random_state=42)
U = svd.fit_transform(customer_product_matrix)
sigma = svd.singular_values_
VT = svd.components_

# Reconstruct the customer-product matrix
reconstructed_matrix = np.dot(np.dot(U, np.diag(sigma)), VT)
reconstructed_df = pd.DataFrame(reconstructed_matrix, index=customer_product_matrix.index, columns=customer_product_matrix.columns)

# Function to get top 10 recommendations for a given customer
def get_top_10_recommendations(customer_id):
    if customer_id not in reconstructed_df.index:
        return []
    customer_ratings = reconstructed_df.loc[customer_id]
    top_10_items = customer_ratings.sort_values(ascending=False).head(10).index.tolist()
    return top_10_items

# Function to get top 3 recommendations per category for a given customer
def get_top_3_per_category(customer_id):
    if customer_id not in reconstructed_df.index:
        return {}
    customer_ratings = reconstructed_df.loc[customer_id]
    top_3_per_category = {}
    for category in df['Industry'].unique():
        category_items = df[df['Industry'] == category]['Product Name'].unique()
        category_ratings = customer_ratings[category_items]
        top_3_items = category_ratings.sort_values(ascending=False).head(3).index.tolist()
        top_3_per_category[category] = top_3_items
    return top_3_per_category

# Function to identify the category a customer is most interested in
def most_interested_category(customer_id):
    if customer_id not in reconstructed_df.index:
        return None
    customer_ratings = reconstructed_df.loc[customer_id]
    category_interest = {}
    for category in df['Industry'].unique():
        category_items = df[df['Industry'] == category]['Product Name'].unique()
        category_ratings = customer_ratings[category_items].sum()
        category_interest[category] = category_ratings
    most_interested = max(category_interest, key=category_interest.get)
    return most_interested

# Function to determine the price range a customer mostly prefers
def preferred_price_range(customer_id):
    if customer_id not in reconstructed_df.index:
        return None
    customer_ratings = reconstructed_df.loc[customer_id]
    top_rated_items = customer_ratings.sort_values(ascending=False).head(10).index
    top_rated_prices = df[df['Product Name'].isin(top_rated_items)]['Price Sold At']
    avg_price = top_rated_prices.mean()
    return avg_price



def get_store_coordinates():
    coordinates = {}
    with open('../store_coordinates.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            coordinates[row['store_id']] = {
                'latitude': float(row['latitude']),
                'longitude': float(row['longitude'])
            }
    return coordinates

# Example data for warehouses, stores, and product details
warehouses = ['Warehouse 1', 'Warehouse 2', 'Warehouse 3']
stores = ['Store 1', 'Store 2', 'Store 3', 'Store 4']
warehouse_capacities = [5000, 4000, 3000]  # Capacity of each warehouse
store_demands = [1000, 1200, 800, 1500]    # Demand of each store

# Cost matrix (transport cost from each warehouse to each store)
# Rows represent warehouses, columns represent stores
transport_costs = np.array([
    [2, 3, 4, 5],   # Costs from Warehouse 1 to each store
    [3, 2, 5, 4],   # Costs from Warehouse 2 to each store
    [4, 5, 3, 2]    # Costs from Warehouse 3 to each store
])

products = [
    {'name': 'Samsung Galaxy S21', 'cost': 69999, 'holding_cost_rate': 0.1, 'ordering_cost': 200},
    {'name': 'iPhone 12', 'cost': 64900, 'holding_cost_rate': 0.1, 'ordering_cost': 180},
    {'name': 'Vivo V21', 'cost': 28999, 'holding_cost_rate': 0.1, 'ordering_cost': 150},
    {'name': 'OnePlus 9', 'cost': 49999, 'holding_cost_rate': 0.1, 'ordering_cost': 220},
    {'name': 'Dell XPS 13', 'cost': 129999, 'holding_cost_rate': 0.1, 'ordering_cost': 300},
    {'name': 'MacBook Air', 'cost': 92990, 'holding_cost_rate': 0.1, 'ordering_cost': 250},
    {'name': 'HP Spectre x360', 'cost': 114999, 'holding_cost_rate': 0.1, 'ordering_cost': 270},
    {'name': 'Lenovo ThinkPad X1', 'cost': 139990, 'holding_cost_rate': 0.1, 'ordering_cost': 320},
    {'name': 'Canon EOS R5', 'cost': 289990, 'holding_cost_rate': 0.1, 'ordering_cost': 500},
    {'name': 'Nikon Z6', 'cost': 189990, 'holding_cost_rate': 0.1, 'ordering_cost': 450},
    {'name': 'Sony Alpha a7 III', 'cost': 199990, 'holding_cost_rate': 0.1, 'ordering_cost': 480},
    {'name': 'Fujifilm X-T4', 'cost': 169990, 'holding_cost_rate': 0.1, 'ordering_cost': 470},
    {'name': 'Levi\'s Jeans', 'cost': 2999, 'holding_cost_rate': 0.1, 'ordering_cost': 50},
    {'name': 'Nike T-shirt', 'cost': 1799, 'holding_cost_rate': 0.1, 'ordering_cost': 45},
    {'name': 'Adidas Jacket', 'cost': 3499, 'holding_cost_rate': 0.1, 'ordering_cost': 60},
    {'name': 'Puma Shorts', 'cost': 1299, 'holding_cost_rate': 0.1, 'ordering_cost': 40},
    {'name': 'Zara Dress', 'cost': 4999, 'holding_cost_rate': 0.1, 'ordering_cost': 55},
    {'name': 'H&M Blouse', 'cost': 1999, 'holding_cost_rate': 0.1, 'ordering_cost': 45},
    {'name': 'Forever 21 Skirt', 'cost': 2499, 'holding_cost_rate': 0.1, 'ordering_cost': 50},
    {'name': 'Mango Coat', 'cost': 5999, 'holding_cost_rate': 0.1, 'ordering_cost': 65},
]

def calculate_eoq(demand, ordering_cost, holding_cost):
    return np.sqrt((2 * demand * ordering_cost) / holding_cost)

def calculate_safety_stock(daily_demand_std, lead_time, lead_time_std):
    return daily_demand_std * np.sqrt(lead_time + lead_time_std ** 2)

def calculate_rop(daily_demand, lead_time, safety_stock):
    return daily_demand * lead_time + safety_stock

def calculate_total_cost(demand, ordering_cost, holding_cost, transport_cost, eoq):
    num_orders = demand / eoq
    return (num_orders * ordering_cost) + (eoq / 2 * holding_cost) + transport_cost

def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route('/api/product_supply_demand')
    def get_product_supply_demand():
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            query = """
            SELECT product_name, supply_demand
            FROM product_supply_demand;
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            product_data = []
            
            for row in rows:
                product_name = row[0]
                supply_demand = row[1]
                product_data.append({
                    "product_name": product_name,
                    "supply_demand": supply_demand
                })
        
        except Exception as e:
            print(f"Error fetching product supply-demand data: {e}")
            return jsonify({"error": f"Error fetching product supply-demand data: {e}"}), 500
        
        finally:
            cursor.close()
            conn.close()

        return jsonify(product_data)
    
    @app.route('/api/recommendations/<customer_id>',)
    def get_recommendations(customer_id):
        try:
            # Get the recommendations and preferences
            top_10_recommendations = get_top_10_recommendations(int(customer_id))
            top_3_per_category = get_top_3_per_category(int(customer_id))
            most_interested = most_interested_category(int(customer_id))
            preferred_price = preferred_price_range(int(customer_id))

            # Perform t-SNE for dimensionality reduction
            tsne = TSNE(n_components=2, random_state=42)
            tsne_results = tsne.fit_transform(U)

            # Perform KMeans clustering to identify clusters
            kmeans = KMeans(n_clusters=5, random_state=42)
            cluster_labels = kmeans.fit_predict(U)
            
            # Disable interactive mode
            plt.ioff()
            
            # Generate the t-SNE plot
            tsne_df = pd.DataFrame(tsne_results, columns=['tsne_1', 'tsne_2'])
            tsne_df['Customer ID'] = customer_product_matrix.index
            tsne_df['Cluster'] = cluster_labels
            
            plt.figure(figsize=(10, 7))
            sns.scatterplot(x='tsne_1', y='tsne_2', hue='Cluster', palette='tab10', data=tsne_df)
            for i, txt in enumerate(tsne_df['Customer ID']):
                plt.annotate(txt, (tsne_df['tsne_1'][i], tsne_df['tsne_2'][i]), fontsize=8)
            plt.title('Customer Clusters with Labels')
            plt.xlabel('t-SNE Dimension 1')
            plt.ylabel('t-SNE Dimension 2')
            
            # Save the plot to a BytesIO object and encode it as base64
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
            
            response = {
                "top_10_recommendations": top_10_recommendations,
                "top_3_per_category": top_3_per_category,
                "most_interested_category": most_interested,
                "preferred_price_range": preferred_price,
                "plot_image": img_base64  # Include the image in the response
            }
            
            # Close the plot to free up resources
            plt.close()
            
            return jsonify(response)
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/product_details')
    def get_product_details():
        try:
            results = []
            for product in products:
                product_results = {
                    'product_name': product['name'],
                    'stores': []
                }

                for store_idx, store_demand in enumerate(store_demands):
                    warehouse_assignments = np.zeros(len(warehouses))
                    min_transport_cost = np.inf
                    optimal_warehouse = -1
                    
                    for warehouse_idx, warehouse_capacity in enumerate(warehouse_capacities):
                        if store_demand <= warehouse_capacity:
                            cost = transport_costs[warehouse_idx][store_idx] * store_demand
                            if cost < min_transport_cost:
                                min_transport_cost = cost
                                optimal_warehouse = warehouse_idx
                    
                    if optimal_warehouse == -1:
                        product_results['stores'].append({
                            'store_name': stores[store_idx],
                            'error': 'No warehouse can meet the demand'
                        })
                        continue

                    holding_cost = product['holding_cost_rate'] * product['cost']
                    eoq = float(calculate_eoq(store_demand, product['ordering_cost'], holding_cost))
                    daily_demand = store_demand / 365
                    safety_stock = float(calculate_safety_stock(10, 10, 2))  # Adjusted as needed
                    rop = float(calculate_rop(daily_demand, 10, safety_stock))  # Adjusted as needed
                    ail = float(eoq / 2 + safety_stock)
                    transport_cost = float(min_transport_cost)
                    total_cost = float(calculate_total_cost(store_demand, product['ordering_cost'], holding_cost, transport_cost, eoq))

                    product_results['stores'].append({
                        'store_name': stores[store_idx],
                        'warehouse_name': warehouses[optimal_warehouse],
                        'eoq': eoq,
                        'rop': rop,
                        'safety_stock': safety_stock,
                        'ail': ail,
                        'total_cost': total_cost,
                        'transport_cost': transport_cost
                    })

                results.append(product_results)

            return jsonify(results)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/store_locations')
    def get_store_locations():
        conn = get_connection()
        cursor = conn.cursor()
    
        try:
            query = """
            SELECT store_id, SUM(price_sold_at) as total_sales
            FROM orders
            GROUP BY store_id;
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            coordinates={"1":{"latitude":16.469883441295156,"longitude":77.81749090065996},"10":{"latitude":33.065836604778504,"longitude":75.31260833295073},"11":{"latitude":32.992149567364834,"longitude":75.70811611023484},"12":{"latitude":18.35669168899395,"longitude":83.44249042156814},"13":{"latitude":22.960494712069785,"longitude":88.14463844039008},"14":{"latitude":29.00052775368981,"longitude":77.24620191078407},"15":{"latitude":27.763349260559043,"longitude":78.52061585981058},"16":{"latitude":29.345864627833674,"longitude":77.20225660219694},"17":{"latitude":13.71225267738587,"longitude":77.55381907089391},"18":{"latitude":21.577841222676973,"longitude":77.90538153959088},"2":{"latitude":17.81362898043096,"longitude":78.43272522087966},"3":{"latitude":28.19025504928872,"longitude":77.8614362092471},"4":{"latitude":14.181398970878098,"longitude":79.31163139262209},"5":{"latitude":20.51149215794065,"longitude":75.1807723854327},"6":{"latitude":23.6063530664472,"longitude":77.20225658044028},"7":{"latitude":29.077369638158732,"longitude":77.20225658044028},"8":{"latitude":31.16776222563392,"longitude":75.70811608847816},"9":{"latitude":31.580479492523224,"longitude":75.8399520359962}}
            
            store_data = []
            coordinates = get_store_coordinates()
            
            for row in rows:
                store_id = str(row[0])
                total_sales = row[1]
                if store_id in coordinates:
                    store_data.append({
                        "store_id": store_id,
                        "latitude": coordinates[store_id]['latitude'],
                        "longitude": coordinates[store_id]['longitude'],
                        "total_sales": total_sales
                    })
        
        except Exception as e:
            print(f"Error fetching store locations: {e}")
            return jsonify({"error": f"Error fetching store locations: {e}"}), 500
        
        finally:
            cursor.close()
            conn.close()

        return jsonify(store_data)
    
    @app.route('/api/store_sales/<int:store_id>')
    def get_store_sales(store_id):
        conn = get_connection()
        cursor = conn.cursor()

        # Fetch inventory data
        cursor.execute('''
            SELECT product_name, quantity
            FROM inventory
            WHERE store_id = %s
        ''', (store_id,))
        inventory_data = cursor.fetchall()

        # Fetch sales data
        cursor.execute('''
            SELECT product_name, COUNT(*) AS quantity_sold
            FROM orders
            WHERE store_id = %s
            GROUP BY product_name
        ''', (store_id,))
        orders_data = cursor.fetchall()

        cursor.close()
        conn.close()

        # Format the data for JSON output
        data = {
            'inventory': [],
            'sales': []
        }

        for product_name, quantity in inventory_data:
            data['inventory'].append({
                'product': product_name,
                'quantity_present': quantity
            })

        for product_name, quantity_sold in orders_data:
            data['sales'].append({
                'product': product_name,
                'quantity_sold': quantity_sold
            })

        return jsonify(data)

    # Assuming you have the necessary imports and Flask app setup
    @app.route('/api/industry_demand/<int:store_id>')
    def get_industry_demand(store_id):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            query = """
            SELECT industry, DATE(order_date) AS order_date, COUNT(*) AS count
            FROM orders
            WHERE store_id = %s AND order_date >= CURRENT_DATE - INTERVAL '2 months'
            GROUP BY industry, DATE(order_date);
            """
            cursor.execute(query, (store_id,))
            rows = cursor.fetchall()

            df = pd.DataFrame(rows, columns=['industry', 'order_date', 'count'])
            df['order_date'] = pd.to_datetime(df['order_date'])

            trend_data = {}

            for industry in df['industry'].unique():
                industry_df = df[df['industry'] == industry].set_index('order_date')
                industry_df = industry_df.resample('D').sum().fillna(0)

                model = ARIMA(industry_df['count'], order=(1, 1, 1))
                model_fit = model.fit()
                forecast = model_fit.forecast(steps=7)

                last_actual = industry_df['count'].iloc[-7:].mean()
                next_forecast = forecast.mean()

                if next_forecast > last_actual:
                    trend = 'rising'
                elif next_forecast < last_actual:
                    trend = 'declining'
                else:
                    trend = 'stable'

                trend_data[industry] = trend

        except Exception as e:
            print("Error fetching industry demand data:", e)
            return jsonify({"error": "Error fetching industry demand data"}), 500

        finally:
            cursor.close()
            conn.close()

        return jsonify(trend_data)


    @app.route('/api/industry/<string:industry_name>')
    def get_industry_data(industry_name):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            query = f"""
            SELECT product_name, subgroup, DATE(order_date) AS order_date, COUNT(*) AS count
            FROM orders
            WHERE industry = %s AND order_date >= CURRENT_DATE - INTERVAL '2 months'
            GROUP BY product_name, subgroup, DATE(order_date);
            """
            cursor.execute(query, (industry_name,))
            rows = cursor.fetchall()

            df = pd.DataFrame(rows, columns=['product_name', 'subgroup', 'order_date', 'count'])
            df['order_date'] = pd.to_datetime(df['order_date'])

            trend_data = {}

            for subgroup in df['subgroup'].unique():
                subgroup_df = df[df['subgroup'] == subgroup].set_index('order_date')
                subgroup_df = subgroup_df.resample('D').sum().fillna(0)

                model = ARIMA(subgroup_df['count'], order=(1, 1, 1))
                model_fit = model.fit()
                forecast = model_fit.forecast(steps=7)

                last_actual = subgroup_df['count'].iloc[-7:].mean()
                next_forecast = forecast.mean()

                if next_forecast > last_actual:
                    trend = 'rising'
                elif next_forecast < last_actual:
                    trend = 'declining'
                else:
                    trend = 'stable'

                trend_data[subgroup] = trend

        except Exception as e:
            print("Error fetching industry data:", e)
            return jsonify({"error": "Error fetching industry data"}), 500

        finally:
            cursor.close()
            conn.close()

        return jsonify(trend_data)

    @app.route('/api/demand_trend')
    def get_demand_trend():
        conn = get_connection()
        cursor = conn.cursor()

        # Determine if we are using industry or product
        entity_type = request.args.get('type', 'product')  # Default to product if no type is provided
        entity_column = 'industry' if entity_type == 'industry' else 'product_name'

        try:
            query = f"""
            SELECT {entity_column}, DATE(order_date) AS order_date, COUNT(*) AS count
            FROM orders
            WHERE order_date >= CURRENT_DATE - INTERVAL '2 months'
            GROUP BY {entity_column}, DATE(order_date);
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            # Convert to DataFrame for easier manipulation
            df = pd.DataFrame(rows, columns=[entity_column, 'order_date', 'count'])
            df['order_date'] = pd.to_datetime(df['order_date'])

            trend_data = {}

            # Determine trend for each entity using ARIMA model
            for entity in df[entity_column].unique():
                entity_df = df[df[entity_column] == entity].set_index('order_date')
                entity_df = entity_df.resample('D').sum().fillna(0)  # Resample daily, fill missing days with 0

                # Use warnings filter to handle ARIMA warnings
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore')
                    model = ARIMA(entity_df['count'], order=(1, 1, 1))
                    model_fit = model.fit()
                    forecast = model_fit.forecast(steps=7)  # Forecast for the next 7 days

                last_actual = entity_df['count'].iloc[-7:].mean()
                next_forecast = forecast.mean()

                if next_forecast > last_actual:
                    trend = 'rising'
                elif next_forecast < last_actual:
                    trend = 'declining'
                else:
                    trend = 'stable'

                trend_data[entity] = trend

        except Exception as e:
            print("Error fetching demand trend data:", e)
            return jsonify({"error": "Error fetching demand trend data"}), 500

        finally:
            cursor.close()
            conn.close()

        return jsonify(trend_data)

    # app.register_blueprint(main)
    @app.route('/api/analytics')
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

    @app.route('/home', methods=['GET'])
    def hello():
        return jsonify(message="Hello from Flask!")

    @app.route('/api/orders', methods=['GET'])
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

    return app
