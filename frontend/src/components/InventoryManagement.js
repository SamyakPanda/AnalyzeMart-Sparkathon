import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './InventoryManagement.css';

const InventoryManagement = () => {
    const [storeId, setStoreId] = useState(1);
    const [inventoryData, setInventoryData] = useState([]);
    const [salesData, setSalesData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchInventoryData(storeId);
    }, [storeId]);

    const fetchInventoryData = async (storeId) => {
        setLoading(true);
        try {
            const response = await axios.get(`/api/store_sales/${storeId}`);
            if (response.data && response.data.inventory && response.data.sales) {
                setInventoryData(response.data.inventory);
                setSalesData(response.data.sales);
            } else {
                console.error("Unexpected response data format:", response.data);
                setInventoryData([]);
                setSalesData([]);
            }
            setLoading(false);
        } catch (error) {
            console.error("There was an error fetching the inventory data!", error);
            setInventoryData([]);
            setSalesData([]);
            setLoading(false);
        }
    };

    const handleStoreChange = (e) => {
        setStoreId(e.target.value);
    };

    const mergedData = inventoryData.map(item => {
        const salesItem = salesData.find(sale => sale.product === item.product) || { quantity_sold: 0 };
        return {
            product: item.product,
            quantity_present: item.quantity_present,
            quantity_sold: salesItem.quantity_sold
        };
    });

    return (
        <div className="inventory-management-container">
            <h1>Inventory Management</h1>
            <div className="store-selector">
                <label htmlFor="storeSelect">Select Store:</label>
                <select id="storeSelect" value={storeId} onChange={handleStoreChange}>
                    {Array.from({ length: 18 }, (_, i) => (
                        <option key={i + 1} value={i + 1}>Store {i + 1}</option>
                    ))}
                </select>
            </div>
            {loading ? (
                <div>Loading...</div>
            ) : (
                <div className="chart-container">
                    {mergedData.map((item, index) => (
                        <div key={index} className="bar-group">
                            <div className="bar" 
                                style={{ backgroundColor: item.quantity_sold  >= (0.2 * item.quantity_present) ? '#90EE90' : item.quantity_sold  < (0.05 * item.quantity_present) ? '#FF7F7F ':'#ddd' }}>
                                <div
                                    className="bar-quantity"
                                    style={{ height: `${item.quantity_present * 5}px` }}  // Scaled for better visibility
                                    title={`Quantity in Inventory: ${item.quantity_present}`}
                                >
                                    <span className="bar-label">{item.quantity_present}</span>
                                </div>
                                <div
                                    className="bar-sold"
                                    style={{ height: `${item.quantity_sold * 5}px` }}  // Scaled for better visibility
                                    title={`Quantity Sold: ${item.quantity_sold}`}
                                >
                                    <span className="bar-label">{item.quantity_sold}</span>
                                </div>
                            </div>
                            <div className="bar-product">{item.product}</div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default InventoryManagement;
