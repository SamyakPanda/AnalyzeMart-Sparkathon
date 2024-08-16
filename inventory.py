import csv
import random

# List of products with unique IDs
products = [
    {"product_id": i + 1, "product_name": name} for i, name in enumerate([
        "1984", "ACDelco Battery", "Adele - 25", "Adidas Jacket", "Adidas Soccer Jersey",
        "Anthropologie Throw Pillow", "Apples", "Ashley Recliner", "Avengers: Endgame Blu-ray",
        "Bananas", "Barilla Pasta", "Beyonce - Lemonade", "Bissell Steam Mop", "Bosch Dishwasher",
        "Bosch Spark Plugs", "Bridgestone Tires", "Broccoli", "Calcium Supplements", "Canon EOS R5",
        "Carrots", "Carter's Pajamas", "Cetaphil Cleanser", "Coca-Cola", "Coleman Tent", 
        "Crate & Barrel Dresser", "Cuisinart Food Processor", "Dell XPS 13", "Denso Oxygen Sensor", 
        "Dove Hair Mask", "Dumbbells", "Dyson Vacuum", "Fisher-Price Learning Table", 
        "Forever 21 Skirt", "Frozen DVD", "Fujifilm X-T4", "GI Joe Duke", "Gap Kids T-shirt", 
        "Garmin GPS", "H&M Blouse", "HP Spectre x360", "Harry Potter", "Ikea Sofa", "Inception Blu-ray", 
        "Instant Pot", "K&N Air Filter", "Kellogg's Corn Flakes", "KitchenAid Mixer", "L'Oreal Conditioner", 
        "LEGO Mindstorms", "LG Washing Machine", "La-Z-Boy Armchair", "Lays Potato Chips", "Lenovo ThinkPad X1", 
        "Levi's Jeans", "Lipton Tea", "MacBook Air", "Marvel Legends Spider-Man", "Melissa & Doug Puzzles", 
        "Michelin Tires", "Monopoly", "Multivitamin Gummies", "NGK Spark Plugs", "Neutrogena Face Wash", 
        "Nike Running Shoes", "Nike T-shirt", "Nikon Z6", "Ninja Blender", "Olay Moisturizer", 
        "Old Navy Shorts", "Omega-3 Fish Oil", "OnePlus 9", "Oreo Cookies", "OshKosh B'gosh Overalls", 
        "Pantene Shampoo", "Pepsi", "Pier 1 Candle", "Pioneer Car Stereo", "Pottery Barn Bed Frame", 
        "Puma Shorts", "Puma Track Pants", "Resistance Bands", "Risk", "Roomba Robot Vacuum", 
        "Samsung Galaxy S21", "Samsung Refrigerator", "Scrabble", "Settlers of Catan", "Shark Upright Vacuum", 
        "Sony Alpha a7 III", "Star Wars Darth Vader", "Starbucks Coffee", "Target Vase", 
        "Taylor Swift - Evermore", "Tempur-Pedic Mattress", "The Beatles - Abbey Road", 
        "The Godfather DVD", "The Great Gatsby", "The North Face Backpack", "The Ordinary Serum", 
        "Thule Roof Rack", "To Kill a Mockingbird", "Transformers Optimus Prime", "Treadmill", 
        "Tresemme Hair Spray", "Under Armour Sports Bra", "Uniqlo Sweater", "Urban Outfitters Wall Art", 
        "VTech KidiZoom", "Vitamin C Tablets", "Vivo V21", "Wayfair Coffee Table", 
        "WeatherTech Floor Mats", "West Elm Nightstand", "Whirlpool Dryer", "Yeti Cooler", 
        "Yoga Mat", "Yoshimura Exhaust", "Zara Dress", "iPhone 12"
    ])
]

# Store numbers from 1 to 18
stores = [i for i in range(1, 19)]

# Function to generate random inventory count between 40 and 60
def generate_inventory():
    return random.randint(10, 20)

# CSV file path
csv_file_path = 'inventory.csv'

# Writing the CSV file
with open(csv_file_path, mode='w', newline='') as csv_file:
    fieldnames = ['product_id', 'product_name', 'quantity', 'store_id']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for product in products:
        for store_id in stores:
            row = {
                'product_id': product['product_id'],
                'product_name': product['product_name'],
                'quantity': generate_inventory(),
                'store_id': store_id
            }
            writer.writerow(row)

print(f"Inventory CSV file has been created at {csv_file_path}")
