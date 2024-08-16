import pandas as pd
import numpy as np

# List of factors
factors = [
    "Price of the Commodity",
    "Firm Goals",
    "Price of Inputs or Factors",
    "Technology",
    "Government Policy",
    "Expectations",
    "Prices of other Commodities",
    "Number of Firms",
    "Natural Factors"
]

# Product template with prices
products = {
    "Electronics": {
        "Mobile Phones": {
            "Samsung Galaxy S21": 69999,
            "iPhone 12": 64900,
            "Vivo V21": 28999,
            "OnePlus 9": 49999
        },
        "Laptops": {
            "Dell XPS 13": 129999,
            "MacBook Air": 92990,
            "HP Spectre x360": 114999,
            "Lenovo ThinkPad X1": 139990
        },
        "Cameras": {
            "Canon EOS R5": 289990,
            "Nikon Z6": 189990,
            "Sony Alpha a7 III": 199990,
            "Fujifilm X-T4": 169990
        }
    },
    "Clothing and Apparel": {
        "Men's Clothing": {
            "Levi's Jeans": 2999,
            "Nike T-shirt": 1799,
            "Adidas Jacket": 3499,
            "Puma Shorts": 1299
        },
        "Women's Clothing": {
            "Zara Dress": 4999,
            "H&M Blouse": 1999,
            "Forever 21 Skirt": 2499,
            "Uniqlo Sweater": 2999
        },
        "Children's Clothing": {
            "Carter's Pajamas": 1499,
            "Gap Kids T-shirt": 899,
            "Old Navy Shorts": 1199,
            "OshKosh B'gosh Overalls": 1799
        }
    },
    "Home and Kitchen Appliances": {
        "Kitchen Gadgets": {
            "KitchenAid Mixer": 21999,
            "Instant Pot": 11999,
            "Ninja Blender": 13999,
            "Cuisinart Food Processor": 16999
        },
        "Cleaning Appliances": {
            "Dyson Vacuum": 34999,
            "Roomba Robot Vacuum": 29999,
            "Bissell Steam Mop": 13999,
            "Shark Upright Vacuum": 24999
        },
        "Large Appliances": {
            "Samsung Refrigerator": 54990,
            "LG Washing Machine": 31990,
            "Whirlpool Dryer": 24990,
            "Bosch Dishwasher": 34990
        }
    },
    "Books and Media": {
        "Fiction Books": {
            "The Great Gatsby": 399,
            "1984": 299,
            "To Kill a Mockingbird": 349,
            "Harry Potter": 599
        },
        "Music CDs": {
            "Taylor Swift - Evermore": 799,
            "The Beatles - Abbey Road": 899,
            "Adele - 25": 799,
            "Beyonce - Lemonade": 899
        },
        "Movies": {
            "The Godfather DVD": 499,
            "Inception Blu-ray": 699,
            "Frozen DVD": 499,
            "Avengers: Endgame Blu-ray": 799
        }
    },
    "Health and Beauty Products": {
        "Skincare Products": {
            "Neutrogena Face Wash": 499,
            "Olay Moisturizer": 699,
            "Cetaphil Cleanser": 799,
            "The Ordinary Serum": 1099
        },
        "Hair Care Products": {
            "Pantene Shampoo": 399,
            "L'Oreal Conditioner": 399,
            "Dove Hair Mask": 499,
            "Tresemme Hair Spray": 299
        },
        "Vitamins": {
            "Vitamin C Tablets": 399,
            "Omega-3 Fish Oil": 899,
            "Multivitamin Gummies": 699,
            "Calcium Supplements": 499
        }
    },
    "Sporting Goods and Outdoor Equipment": {
        "Fitness Equipment": {
            "Yoga Mat": 1499,
            "Dumbbells": 2999,
            "Treadmill": 49999,
            "Resistance Bands": 799
        },
        "Outdoor Gear": {
            "Coleman Tent": 12999,
            "The North Face Backpack": 8999,
            "Yeti Cooler": 14999,
            "Garmin GPS": 21999
        },
        "Sports Apparel": {
            "Nike Running Shoes": 6999,
            "Under Armour Sports Bra": 1299,
            "Adidas Soccer Jersey": 2499,
            "Puma Track Pants": 1799
        }
    },
    "Toys and Games": {
        "Educational Toys": {
            "LEGO Mindstorms": 35999,
            "Melissa & Doug Puzzles": 1499,
            "Fisher-Price Learning Table": 3499,
            "VTech KidiZoom": 2999
        },
        "Board Games": {
            "Monopoly": 1499,
            "Settlers of Catan": 1999,
            "Scrabble": 1199,
            "Risk": 1499
        },
        "Action Figures": {
            "Marvel Legends Spider-Man": 1499,
            "Star Wars Darth Vader": 1799,
            "Transformers Optimus Prime": 2199,
            "GI Joe Duke": 1299
        }
    },
    "Furniture and Home Décor": {
        "Living Room Furniture": {
            "Ikea Sofa": 25999,
            "Wayfair Coffee Table": 8999,
            "Ashley Recliner": 16999,
            "La-Z-Boy Armchair": 18999
        },
        "Bedroom Furniture": {
            "Tempur-Pedic Mattress": 49990,
            "Pottery Barn Bed Frame": 34999,
            "West Elm Nightstand": 9999,
            "Crate & Barrel Dresser": 20999
        },
        "Home Decor": {
            "Urban Outfitters Wall Art": 2499,
            "Anthropologie Throw Pillow": 1599,
            "Target Vase": 799,
            "Pier 1 Candle": 599
        }
    },
    "Automotive Parts and Accessories": {
        "Car Parts": {
            "Bosch Spark Plugs": 499,
            "Michelin Tires": 6999,
            "Denso Oxygen Sensor": 2999,
            "ACDelco Battery": 4999
        },
        "Car Accessories": {
            "WeatherTech Floor Mats": 9999,
            "Garmin GPS": 21999,
            "Pioneer Car Stereo": 12999,
            "Thule Roof Rack": 15999
        },
        "Motorcycle Parts": {
            "K&N Air Filter": 2999,
            "Bridgestone Tires": 7999,
            "NGK Spark Plugs": 799,
            "Yoshimura Exhaust": 21999
        }
    },
    "Groceries and Food Items": {
        "Fresh Produce": {
            "Bananas": 50,
            "Apples": 100,
            "Carrots": 60,
            "Broccoli": 80
        },
        "Packaged Foods": {
            "Kellogg's Corn Flakes": 299,
            "Oreo Cookies": 159,
            "Lays Potato Chips": 99,
            "Barilla Pasta": 199
        },
        "Beverages": {
            "Coca-Cola": 40,
            "Pepsi": 35,
            "Starbucks Coffee": 250,
            "Lipton Tea": 100
        }
    }
}

# Mapping for categorical features
categorical_mapping = {
    "Firm Goals": ["High", "Medium", "Low"],
    "Technology": ["Advanced", "Moderate", "Basic"],
    "Government Policy": ["Favorable", "Neutral", "Unfavorable"],
    "Expectations": ["Positive", "Neutral", "Negative"],
    "Natural Factors": ["Optimal", "Average", "Poor"]
}

# Function to randomly assign categorical values
def get_random_categorical_value(factor):
    return np.random.choice(categorical_mapping[factor])

# Generate data for all products
all_products_features = []

for category, subcategories in products.items():
    for subcategory, items in subcategories.items():
        for item, price in items.items():
            features = {
                "Category": category,
                "Subcategory": subcategory,
                "Product": item,
                "Price of the Commodity": price,
                "Firm Goals": get_random_categorical_value("Firm Goals"),
                "Price of Inputs or Factors": np.random.randint(1, 101),
                "Technology": get_random_categorical_value("Technology"),
                "Government Policy": get_random_categorical_value("Government Policy"),
                "Expectations": get_random_categorical_value("Expectations"),
                "Prices of other Commodities": np.random.randint(price-100, price + 100),
                "Number of Firms": np.random.randint(1, 11),
                "Natural Factors": get_random_categorical_value("Natural Factors")
            }
            all_products_features.append(features)

# Create a DataFrame
df = pd.DataFrame(all_products_features)

# Save to CSV
df.to_csv('product_factors.csv', index=False)

print("CSV file 'product_factors.csv' created successfully.")
