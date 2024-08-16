import React, { useState, useEffect } from 'react';
import './DemandForecast.css';

const similarProductsMap ={'Samsung Galaxy S21': ['iPhone 12', 'Vivo V21', 'OnePlus 9'], 'iPhone 12': ['Samsung Galaxy S21', 'Vivo V21', 'OnePlus 9'], 'Vivo V21': ['Samsung Galaxy S21', 'iPhone 12', 'OnePlus 9'], 'OnePlus 9': ['Samsung Galaxy S21', 'iPhone 12', 'Vivo V21'], 'Dell XPS 13': ['MacBook Air', 'HP Spectre x360', 'Lenovo ThinkPad X1'], 'MacBook Air': ['Dell XPS 13', 'HP Spectre x360', 'Lenovo ThinkPad X1'], 'HP Spectre x360': ['Dell XPS 13', 'MacBook Air', 'Lenovo ThinkPad X1'], 'Lenovo ThinkPad X1': ['Dell XPS 13', 'MacBook Air', 'HP Spectre x360'], 'Canon EOS R5': ['Nikon Z6', 'Sony Alpha a7 III', 'Fujifilm X-T4'], 'Nikon Z6': ['Canon EOS R5', 'Sony Alpha a7 III', 'Fujifilm X-T4'], 'Sony Alpha a7 III': ['Canon EOS R5', 'Nikon Z6', 'Fujifilm X-T4'], 'Fujifilm X-T4': ['Canon EOS R5', 'Nikon Z6', 'Sony Alpha a7 III'], "Levi's Jeans": ['Nike T-shirt', 'Adidas Jacket', 'Puma Shorts'], 'Nike T-shirt': ["Levi's Jeans", 'Adidas Jacket', 'Puma Shorts'], 'Adidas Jacket': ["Levi's Jeans", 'Nike T-shirt', 'Puma Shorts'], 'Puma Shorts': ["Levi's Jeans", 'Nike T-shirt', 'Adidas Jacket'], 'Zara Dress': ['H&M Blouse', 'Forever 21 Skirt', 'Uniqlo Sweater'], 'H&M Blouse': ['Zara Dress', 'Forever 21 Skirt', 'Uniqlo Sweater'], 'Forever 21 Skirt': ['Zara Dress', 'H&M Blouse', 'Uniqlo Sweater'], 'Uniqlo Sweater': ['Zara Dress', 'H&M Blouse', 'Forever 21 Skirt'], "Carter's Pajamas": ['Gap Kids T-shirt', 'Old Navy Shorts', "OshKosh B'gosh Overalls"], 'Gap Kids T-shirt': ["Carter's Pajamas", 'Old Navy Shorts', "OshKosh B'gosh Overalls"], 'Old Navy Shorts': ["Carter's Pajamas", 'Gap Kids T-shirt', "OshKosh B'gosh Overalls"], "OshKosh B'gosh Overalls": ["Carter's Pajamas", 'Gap Kids T-shirt', 'Old Navy Shorts'], 'KitchenAid Mixer': ['Instant Pot', 'Ninja Blender', 'Cuisinart Food Processor'], 'Instant Pot': ['KitchenAid Mixer', 'Ninja Blender', 'Cuisinart Food Processor'], 'Ninja Blender': ['KitchenAid Mixer', 'Instant Pot', 'Cuisinart Food Processor'], 'Cuisinart Food Processor': ['KitchenAid Mixer', 'Instant Pot', 'Ninja Blender'], 'Dyson Vacuum': ['Roomba Robot Vacuum', 'Bissell Steam Mop', 'Shark Upright Vacuum'], 'Roomba Robot Vacuum': ['Dyson Vacuum', 'Bissell Steam Mop', 'Shark Upright Vacuum'], 'Bissell Steam Mop': ['Dyson Vacuum', 'Roomba Robot Vacuum', 'Shark Upright Vacuum'], 'Shark Upright Vacuum': ['Dyson Vacuum', 'Roomba Robot Vacuum', 'Bissell Steam Mop'], 'Samsung Refrigerator': ['LG Washing Machine', 'Whirlpool Dryer', 'Bosch Dishwasher'], 'LG Washing Machine': ['Samsung Refrigerator', 'Whirlpool Dryer', 'Bosch Dishwasher'], 'Whirlpool Dryer': ['Samsung Refrigerator', 'LG Washing Machine', 'Bosch Dishwasher'], 'Bosch Dishwasher': ['Samsung Refrigerator', 'LG Washing Machine', 'Whirlpool Dryer'], 'The Great Gatsby': ['1984', 'To Kill a Mockingbird', 'Harry Potter'], '1984': ['The Great Gatsby', 'To Kill a Mockingbird', 'Harry Potter'], 'To Kill a Mockingbird': ['The Great Gatsby', '1984', 'Harry Potter'], 'Harry Potter': ['The Great Gatsby', '1984', 'To Kill a Mockingbird'], 'Taylor Swift - Evermore': ['The Beatles - Abbey Road', 'Adele - 25', 'Beyonce - Lemonade'], 'The Beatles - Abbey Road': ['Taylor Swift - Evermore', 'Adele - 25', 'Beyonce - Lemonade'], 'Adele - 25': ['Taylor Swift - Evermore', 'The Beatles - Abbey Road', 'Beyonce - Lemonade'], 'Beyonce - Lemonade': ['Taylor Swift - Evermore', 'The Beatles - Abbey Road', 'Adele - 25'], 'The Godfather DVD': ['Inception Blu-ray', 'Frozen DVD', 'Avengers: Endgame Blu-ray'], 'Inception Blu-ray': ['The Godfather DVD', 'Frozen DVD', 'Avengers: Endgame Blu-ray'], 'Frozen DVD': ['The Godfather DVD', 'Inception Blu-ray', 'Avengers: Endgame Blu-ray'], 'Avengers: Endgame Blu-ray': ['The Godfather DVD', 'Inception Blu-ray', 'Frozen DVD'], 'Neutrogena Face Wash': ['Olay Moisturizer', 'Cetaphil Cleanser', 'The Ordinary Serum'], 'Olay Moisturizer': ['Neutrogena Face Wash', 'Cetaphil Cleanser', 'The Ordinary Serum'], 'Cetaphil Cleanser': ['Neutrogena Face Wash', 'Olay Moisturizer', 'The Ordinary Serum'], 'The Ordinary Serum': ['Neutrogena Face Wash', 'Olay Moisturizer', 'Cetaphil Cleanser'], 'Pantene Shampoo': ["L'Oreal Conditioner", 'Dove Hair Mask', 'Tresemme Hair Spray'], "L'Oreal Conditioner": ['Pantene Shampoo', 'Dove Hair Mask', 'Tresemme Hair Spray'], 'Dove Hair Mask': ['Pantene Shampoo', "L'Oreal Conditioner", 'Tresemme Hair Spray'], 'Tresemme Hair Spray': ['Pantene Shampoo', "L'Oreal Conditioner", 'Dove Hair Mask'], 'Vitamin C Tablets': ['Omega-3 Fish Oil', 'Multivitamin Gummies', 'Calcium Supplements'], 'Omega-3 Fish Oil': ['Vitamin C Tablets', 'Multivitamin Gummies', 'Calcium Supplements'], 'Multivitamin Gummies': ['Vitamin C Tablets', 'Omega-3 Fish Oil', 'Calcium Supplements'], 'Calcium Supplements': ['Vitamin C Tablets', 'Omega-3 Fish Oil', 'Multivitamin Gummies'], 'Yoga Mat': ['Dumbbells', 'Treadmill', 'Resistance Bands'], 'Dumbbells': ['Yoga Mat', 'Treadmill', 'Resistance Bands'], 'Treadmill': ['Yoga Mat', 'Dumbbells', 'Resistance Bands'], 'Resistance Bands': ['Yoga Mat', 'Dumbbells', 'Treadmill'], 'Coleman Tent': ['The North Face Backpack', 'Yeti Cooler', 'Garmin GPS'], 'The North Face Backpack': ['Coleman Tent', 'Yeti Cooler', 'Garmin GPS'], 'Yeti Cooler': ['Coleman Tent', 'The North Face Backpack', 'Garmin GPS'], 'Garmin GPS': ['WeatherTech Floor Mats', 'Pioneer Car Stereo', 'Thule Roof Rack'], 'Nike Running Shoes': ['Under Armour Sports Bra', 'Adidas Soccer Jersey', 'Puma Track Pants'], 'Under Armour Sports Bra': ['Nike Running Shoes', 'Adidas Soccer Jersey', 'Puma Track Pants'], 'Adidas Soccer Jersey': ['Nike Running Shoes', 'Under Armour Sports Bra', 'Puma Track Pants'], 'Puma Track Pants': ['Nike Running Shoes', 'Under Armour Sports Bra', 'Adidas Soccer Jersey'], 'LEGO Mindstorms': ['Melissa & Doug Puzzles', 'Fisher-Price Learning Table', 'VTech KidiZoom'], 'Melissa & Doug Puzzles': ['LEGO Mindstorms', 'Fisher-Price Learning Table', 'VTech KidiZoom'], 'Fisher-Price Learning Table': ['LEGO Mindstorms', 'Melissa & Doug Puzzles', 'VTech KidiZoom'], 'VTech KidiZoom': ['LEGO Mindstorms', 'Melissa & Doug Puzzles', 'Fisher-Price Learning Table'], 'Monopoly': ['Settlers of Catan', 'Scrabble', 'Risk'], 'Settlers of Catan': ['Monopoly', 'Scrabble', 'Risk'], 'Scrabble': ['Monopoly', 'Settlers of Catan', 'Risk'], 'Risk': ['Monopoly', 'Settlers of Catan', 'Scrabble'], 'Marvel Legends Spider-Man': ['Star Wars Darth Vader', 'Transformers Optimus Prime', 'GI Joe Duke'], 'Star Wars Darth Vader': ['Marvel Legends Spider-Man', 'Transformers Optimus Prime', 'GI Joe Duke'], 'Transformers Optimus Prime': ['Marvel Legends Spider-Man', 'Star Wars Darth Vader', 'GI Joe Duke'], 'GI Joe Duke': ['Marvel Legends Spider-Man', 'Star Wars Darth Vader', 'Transformers Optimus Prime'], 'Ikea Sofa': ['Wayfair Coffee Table', 'Ashley Recliner', 'La-Z-Boy Armchair'], 'Wayfair Coffee Table': ['Ikea Sofa', 'Ashley Recliner', 'La-Z-Boy Armchair'], 'Ashley Recliner': ['Ikea Sofa', 'Wayfair Coffee Table', 'La-Z-Boy Armchair'], 'La-Z-Boy Armchair': ['Ikea Sofa', 'Wayfair Coffee Table', 'Ashley Recliner'], 'Tempur-Pedic Mattress': ['Pottery Barn Bed Frame', 'West Elm Nightstand', 'Crate & Barrel Dresser'], 'Pottery Barn Bed Frame': ['Tempur-Pedic Mattress', 'West Elm Nightstand', 'Crate & Barrel Dresser'], 'West Elm Nightstand': ['Tempur-Pedic Mattress', 'Pottery Barn Bed Frame', 'Crate & Barrel Dresser'], 'Crate & Barrel Dresser': ['Tempur-Pedic Mattress', 'Pottery Barn Bed Frame', 'West Elm Nightstand'], 'Urban Outfitters Wall Art': ['Anthropologie Throw Pillow', 'Target Vase', 'Pier 1 Candle'], 'Anthropologie Throw Pillow': ['Urban Outfitters Wall Art', 'Target Vase', 'Pier 1 Candle'], 'Target Vase': ['Urban Outfitters Wall Art', 'Anthropologie Throw Pillow', 'Pier 1 Candle'], 'Pier 1 Candle': ['Urban Outfitters Wall Art', 'Anthropologie Throw Pillow', 'Target Vase'], 'Bosch Spark Plugs': ['Michelin Tires', 'Denso Oxygen Sensor', 'ACDelco Battery'], 'Michelin Tires': ['Bosch Spark Plugs', 'Denso Oxygen Sensor', 'ACDelco Battery'], 'Denso Oxygen Sensor': ['Bosch Spark Plugs', 'Michelin Tires', 'ACDelco Battery'], 'ACDelco Battery': ['Bosch Spark Plugs', 'Michelin Tires', 'Denso Oxygen Sensor'], 'WeatherTech Floor Mats': ['Garmin GPS', 'Pioneer Car Stereo', 'Thule Roof Rack'], 'Pioneer Car Stereo': ['WeatherTech Floor Mats', 'Garmin GPS', 'Thule Roof Rack'], 'Thule Roof Rack': ['WeatherTech Floor Mats', 'Garmin GPS', 'Pioneer Car Stereo'], 'K&N Air Filter': ['Bridgestone Tires', 'NGK Spark Plugs', 'Yoshimura Exhaust'], 'Bridgestone Tires': ['K&N Air Filter', 'NGK Spark Plugs', 'Yoshimura Exhaust'], 'NGK Spark Plugs': ['K&N Air Filter', 'Bridgestone Tires', 'Yoshimura Exhaust'], 'Yoshimura Exhaust': ['K&N Air Filter', 'Bridgestone Tires', 'NGK Spark Plugs'], 'Bananas': ['Apples', 'Carrots', 'Broccoli'], 'Apples': ['Bananas', 'Carrots', 'Broccoli'], 'Carrots': ['Bananas', 'Apples', 'Broccoli'], 'Broccoli': ['Bananas', 'Apples', 'Carrots'], "Kellogg's Corn Flakes": ['Oreo Cookies', 'Lays Potato Chips', 'Barilla Pasta'], 'Oreo Cookies': ["Kellogg's Corn Flakes", 'Lays Potato Chips', 'Barilla Pasta'], 'Lays Potato Chips': ["Kellogg's Corn Flakes", 'Oreo Cookies', 'Barilla Pasta'], 'Barilla Pasta': ["Kellogg's Corn Flakes", 'Oreo Cookies', 'Lays Potato Chips'], 'Coca-Cola': ['Pepsi', 'Starbucks Coffee', 'Lipton Tea'], 'Pepsi': ['Coca-Cola', 'Starbucks Coffee', 'Lipton Tea'], 'Starbucks Coffee': ['Coca-Cola', 'Pepsi', 'Lipton Tea'], 'Lipton Tea': ['Coca-Cola', 'Pepsi', 'Starbucks Coffee']};

const DemandForecast = () => {
    const [trendData, setTrendData] = useState({});
    const [supplyDemandData, setSupplyDemandData] = useState({});
    const [error, setError] = useState(null);
    const [entityType, setEntityType] = useState('product');
    const [selectedIndustry, setSelectedIndustry] = useState(null);

    const [recommendationCounts, setRecommendationCounts] = useState({
        stock: 0,
        strongStock: 0,
        discount: 0,
        stop: 0
    });

    const fetchData = async (type, industry = null) => {
        try {
            const trendUrl = industry ? `/api/industry/${industry}` : `/api/demand_trend?type=${type}`;
            const response = await fetch(trendUrl);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const trendData = await response.json();

            if (type === 'product') {
                const supplyDemandResponse = await fetch('/api/product_supply_demand');
                if (!supplyDemandResponse.ok) {
                    throw new Error('Network response was not ok');
                }
                const supplyDemandArray = await supplyDemandResponse.json();
                const supplyDemandData = supplyDemandArray.reduce((acc, { product_name, supply_demand }) => {
                    acc[product_name] = supply_demand;
                    return acc;
                }, {});
                console.log('Supply-Demand Data:', supplyDemandData);
                setSupplyDemandData(supplyDemandData);
            } else {
                setSupplyDemandData({});
            }

            setTrendData(trendData);
        } catch (error) {
            setError(error.toString());
        }
    };

    useEffect(() => {
        fetchData(entityType, selectedIndustry);
    }, [entityType, selectedIndustry]);

    useEffect(() => {
        updateCounts();
    }, [trendData, supplyDemandData]);

    const handleEntityTypeChange = (type) => {
        setEntityType(type);
        setSelectedIndustry(null);
        setTrendData({});
        setSupplyDemandData({});
        setError(null);
    };

    const handleIndustryClick = (industry) => {
        setEntityType('industry');
        setSelectedIndustry(industry);
        fetchData('industry', industry);
    };

    const renderSimilarProducts = (product) => {
        const similarProducts = similarProductsMap[product];
        if (!similarProducts) return null;
    
        return (
            <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
                {similarProducts.map((similarProduct) => (
                    <div
                        key={similarProduct}
                        style={{
                            border: '1px solid black',
                            borderRadius: '8px',
                            padding: '5px 10px',
                            textAlign: 'center',
                            fontSize: '12px',
                        }}
                    >
                        {similarProduct}: {trendData[similarProduct] ? trendData[similarProduct].charAt(0).toUpperCase() + trendData[similarProduct].slice(1) : 'No trend data'}
                    </div>
                ))}
            </div>
        );
    };
    
    const getRecommendation = (trend, supply) => {
        const recommendations = {
            'rising': {
                'High': 'Stock',
                'Stable': 'Stock',
                'Low': 'Strong Stock'
            },
            'stable': {
                'High': 'Stock',
                'Stable': 'Stock',
                'Low': 'Stock'
            },
            'declining': {
                'High': 'Discount/Unstock',
                'Stable': 'Discount/Unstock',
                'Low': 'Stop Supply'
            }
        };
    
        return recommendations[trend]?.[supply] || 'No Recommendation';
    };

    const updateCounts = () => {
        const newCounts = {
            stock: 0,
            strongStock: 0,
            discount: 0,
            stop: 0
        };

        Object.entries(supplyDemandData).forEach(([entity, supply]) => {
            const trend = trendData[entity];
            if (trend) {
                const recommendation = getRecommendation(trend, supply);
                if (recommendation === 'Stock') newCounts.stock++;
                if (recommendation === 'Strong Stock') newCounts.strongStock++;
                if (recommendation === 'Discount/Unstock') newCounts.discount++;
                if (recommendation === 'Stop Supply') newCounts.stop++;
            }
        });

        setRecommendationCounts(newCounts);
    };

    return (
        <div className="demand-forecast-container">
            <div>
                <h2 style={{fontFamily: 'sans-serif'}}>Demand Forecasting</h2>
            </div>
            <div className="entity-type-selector">
                <button 
                    onClick={() => handleEntityTypeChange('product')}
                    className={entityType === 'product' ? 'active' : ''}
                >
                    Product
                </button>
                <button 
                    onClick={() => handleEntityTypeChange('industry')}
                    className={entityType === 'industry' ? 'active' : ''}
                >
                    Industry
                </button>
                
            </div>
            <div className="industry-filter" style={{fontSize:'15px'}}>
                    Trend Data for {entityType} and recommendations
            </div>

            <div className="total-count-box">
                <img src="../static/Stock.png" />
                <span><strong>Total {entityType === 'product' ? 'Products' : 'Industries'}:</strong> 
                <div style={{fontSize:'30px', textAlign:'center'}}>{Object.keys(trendData).length}</div></span>
            </div>
            <div>
                {entityType === 'product' && (
                <div className="recommendation-summary">
                    <div className="recommendation-item">
                        <img src="../static/Stock.png" />
                        <span>
                            <strong>Recommended to Stock:</strong>
                            <div style={{ fontSize: '30px', textAlign: 'center', marginTop: '10px' }}>{recommendationCounts.stock}</div>
                        </span>
                    </div>
                    <div className="recommendation-item">
                        <img src="../static/Strong Stock.png" />
                        <span>
                            <strong>Recommended to Strong Stock:</strong>
                            <div style={{ fontSize: '30px', textAlign: 'center', marginTop: '10px'}}>{recommendationCounts.strongStock}</div>
                        </span>
                    </div>
                    <div className="recommendation-item">
                        <img src="../static/Discount/Unstock.png" alt="Discount" />
                        <span>
                            <strong>Recommended to Discount/Unstock:</strong>
                            <div style={{ fontSize: '30px', textAlign: 'center', marginTop: '10px' }}>{recommendationCounts.discount}</div>
                        </span>
                    </div>
                    <div className="recommendation-item">
                        <img src="../static/Stop Supply.png" alt="Stop" />
                        <span>
                            <strong>Recommended to Stop Supply:</strong>
                            <div style={{ fontSize: '30px', textAlign: 'center', marginTop: '10px' }}>{recommendationCounts.stop}</div>
                        </span>
                    </div>
                </div>
            )}
            </div>

            {selectedIndustry && (
                <>
                <div className="industry-filter">
                    <label htmlFor="industry-select">Select Industry: </label>
                    <select 
                        id="industry-select" 
                        onChange={(e) => handleIndustryClick(e.target.value)} 
                        value={selectedIndustry}
                    >
                        <option value="Industry1">Industry1</option>
                        <option value="Industry2">Industry2</option>
                        {/* Add other industries here */}
                    </select>
                </div>
                <div className="industry-filter">
                    Industry: {selectedIndustry}
                </div>
                </>
            )}
            {error ? (
                <div className="error">{error}</div>
            ) : (
                <table className="forecast-table">
                    <thead>
                        <tr>
                            <th>{entityType.charAt(0).toUpperCase() + entityType.slice(1)}</th>
                            <th>Trend</th>
                            {entityType === 'product' && <th>Supply</th>}
                            {entityType === 'product' && <th>Recommendation</th>}
                            {entityType === 'product' && <th>Similar Products</th>}
                        </tr>
                    </thead>
                    <tbody>
                        {Object.entries(trendData).map(([entity, trend]) => (
                            <tr 
                                key={entity} 
                                // className={`forecast-item ${trend}`} 
                                onClick={() => entityType === 'industry' && handleIndustryClick(entity)}
                            >
                                <td style={{ fontWeight: 'bold', fontSize: '1.2em' }}>
                                    {entity}
                                </td>
                                <td style={{ textAlign: 'center' }}>
                                <div className="container">
                                    <div className="trend-container">
                                        <img 
                                            src={require(`../static/${trend}.png`)}
                                            alt={`${trend} logo`}
                                            className="trend-logo"
                                        />
                                        <span className="trend-text">{trend.charAt(0).toUpperCase() + trend.slice(1)}</span>
                                    </div>
                                </div>
                            </td>

                                {entityType === 'product' && (
                                    <td style={{ textAlign: 'center' }}>
                                        <div className="container">
                                            <div className="supply-container">
                                                <img 
                                                    src={supplyDemandData[entity] 
                                                        ? require(`../static/${supplyDemandData[entity] === 'High' ? 'rising.png' 
                                                            : supplyDemandData[entity] === 'Low' ? 'declining.png' 
                                                            : 'stable.png'}`) 
                                                        : null}
                                                    className="supply-logo"
                                                />
                                                <span className="supply-text">
                                                    {supplyDemandData[entity] 
                                                        ? supplyDemandData[entity].charAt(0).toUpperCase() + supplyDemandData[entity].slice(1) 
                                                        : 'No data'}
                                                </span>
                                            </div>
                                        </div>
                                    </td>
                                
                                )}
                                {entityType === 'product' && (
                                    <td style={{ textAlign: 'center' }}>
                                        <div className="container">
                                            <div className='supply-container2'>
                                                <img 
                                                    src={
                                                        supplyDemandData[entity] 
                                                        ? require(`../static/${getRecommendation(trend, supplyDemandData[entity])}.png`) 
                                                        : null
                                                    }
                                                    className="supply-logo"
                                                />
                                                <span className="supply-text">
                                                    {getRecommendation(trend, 
                                                        supplyDemandData[entity] 
                                                        ? supplyDemandData[entity].charAt(0).toUpperCase() + supplyDemandData[entity].slice(1) 
                                                        : 'No data'
                                                    )}
                                                </span>
                                            </div>
                                        </div>
                                    </td>
                                )}

                                {entityType === 'product' && <td style={{ maxWidth:'200px'}}>{renderSimilarProducts(entity)}</td>}
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
};

export default DemandForecast;