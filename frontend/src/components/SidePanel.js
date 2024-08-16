// src/components/SidePanel.js
import React, { useEffect, useState } from 'react';
import './SidePanel.css';

const SidePanel = ({ store, onClose }) => {
    const [industryData, setIndustryData] = useState({});
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchIndustryData = async () => {
            try {
                const response = await fetch(`/api/industry_demand/${store.store_id}`);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setIndustryData(data);
            } catch (error) {
                setError(error.toString());
            }
        };

        fetchIndustryData();
    }, [store.store_id]);

    return (
        <div className="side-panel">
            <button className="close-button" onClick={onClose}>X</button>
            <h3>Store Details</h3>
            <p><b>Store ID:</b> {store.store_id}</p>
            <p><b>Total Sales:</b> {store.total_sales}</p>

            <h3>Industry Demand Forecasting</h3>
            {error ? (
                <div className="error">{error}</div>
            ) : (
                <table className="forecast-table">
                    <thead>
                        <tr>
                            <th>Industry</th>
                            <th>Trend</th>
                        </tr>
                    </thead>
                    <tbody>
                        {Object.entries(industryData).map(([industry, trend]) => (
                            <tr key={industry}>
                                <td>{industry}</td>
                                <td>{trend.charAt(0).toUpperCase() + trend.slice(1)}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
};

export default SidePanel;
