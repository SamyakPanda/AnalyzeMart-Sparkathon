import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Predictions.css';

const Predictions = () => {
    const [productData, setProductData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [activeProductTab, setActiveProductTab] = useState(0);
    const [activeStoreTab, setActiveStoreTab] = useState(0);

    useEffect(() => {
        fetchProductDetails();
    }, []);

    const fetchProductDetails = async () => {
        setLoading(true);
        try {
            const response = await axios.get('/api/product_details');
            if (response.data) {
                setProductData(response.data);
            } else {
                console.error("Unexpected response data format:", response.data);
                setProductData([]);
            }
        } catch (error) {
            console.error("There was an error fetching the product details!", error);
            setProductData([]);
        } finally {
            setLoading(false);
        }
    };

    const handleProductTabClick = (index) => {
        setActiveProductTab(index);
        setActiveStoreTab(0); // Reset store tab when product changes
    };

    const handleStoreTabClick = (index) => {
        setActiveStoreTab(index);
    };

    const formatNumber = (number) => {
        return number !== undefined && number !== null ? number.toFixed(2) : 'N/A';
    };

    return (
        <div className="predictions-container">
            <h1>Product Details</h1>
            {loading ? (
                <div>Loading...</div>
            ) : (
                <div className="tabs-container">
                    <div className="product-tabs-slider">
                        <div className="product-tabs">
                            {productData.map((product, index) => (
                                <div
                                    key={index}
                                    className={`tab ${activeProductTab === index ? 'active' : ''}`}
                                    onClick={() => handleProductTabClick(index)}
                                >
                                    {product.product_name}
                                </div>
                            ))}
                        </div>
                    </div>
                    {productData.length > 0 && (
                        <div className="store-tabs">
                            {productData[activeProductTab].stores.map((store, index) => (
                                <div
                                    key={index}
                                    className={`tab ${activeStoreTab === index ? 'active' : ''}`}
                                    onClick={() => handleStoreTabClick(index)}
                                >
                                    {store.store_name}
                                </div>
                            ))}
                        </div>
                    )}
                    {productData.length > 0 && productData[activeProductTab].stores.length > 0 && (
                        <div className="tab-content">
                            <h2>{productData[activeProductTab].stores[activeStoreTab].store_name}</h2>
                            <ul>
                                <li><strong>Warehouse:</strong> {productData[activeProductTab].stores[activeStoreTab].warehouse_name || 'N/A'}</li>
                                <li><strong>Average Inventory Level (AIL):</strong> {formatNumber(productData[activeProductTab].stores[activeStoreTab].ail)}</li>
                                <li><strong>Economic Order Quantity (EOQ):</strong> {formatNumber(productData[activeProductTab].stores[activeStoreTab].eoq)}</li>
                                <li><strong>Reorder Point (ROP):</strong> {formatNumber(productData[activeProductTab].stores[activeStoreTab].rop)}</li>
                                <li><strong>Safety Stock:</strong> {formatNumber(productData[activeProductTab].stores[activeStoreTab].safety_stock)}</li>
                                <li><strong>Total Cost:</strong> {formatNumber(productData[activeProductTab].stores[activeStoreTab].total_cost)}</li>
                                <li><strong>Transport Cost:</strong> {formatNumber(productData[activeProductTab].stores[activeStoreTab].transport_cost)}</li>
                            </ul>
                            <p className="description">
    <strong>Warehouse:</strong>
    This refers to the specific storage facility where the products are kept before being distributed to stores or customers. The warehouse manages the stock levels and ensures that products are available to meet demand.

    <strong>Average Inventory Level (AIL):</strong>
    The Average Inventory Level represents the typical amount of inventory that is kept on hand in the warehouse over a certain period of time. It helps in determining the efficiency of inventory management and is crucial for balancing holding costs against stockout risks.

    <strong>Economic Order Quantity (EOQ):</strong>
    The Economic Order Quantity is the optimal number of units that should be ordered to minimize the total inventory costs, which include ordering costs and holding costs. EOQ helps in determining the most cost-effective quantity to order to replenish stock.

    <strong>Reorder Point (ROP):</strong>
    The Reorder Point is the inventory level at which a new order should be placed to replenish stock before it runs out. It ensures that there is enough lead time to receive new inventory without causing a stockout.

    <strong>Safety Stock:</strong>
    Safety Stock refers to the extra inventory that is held in reserve to protect against uncertainties in demand or supply chain disruptions. It acts as a buffer to prevent stockouts in case of unexpected demand spikes or delays in delivery.

    <strong>Total Cost:</strong>
    This represents the total cost associated with managing the inventory in the warehouse. It includes all relevant costs such as purchasing, holding, ordering, and handling of the products. Reducing total cost while maintaining adequate stock levels is a key goal of inventory management.

    <strong>Transport Cost:</strong>
    Transport Cost refers to the expenses incurred in moving products from the warehouse to the stores or customers. This cost is an important factor in determining the overall efficiency of the supply chain. Reducing transport costs can significantly impact the total cost of inventory management.
</p>

                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default Predictions;
