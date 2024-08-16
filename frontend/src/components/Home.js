import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Home.css';

const HomePage = () => {
    const [analytics, setAnalytics] = useState({
        topProducts: [],
        topIndustries: [],
        topSubgroups: [],
        salesPerStore: {}
    });

    useEffect(() => {
        // Fetch data from the backend
        axios.get('/api/analytics')
            .then(response => {
                setAnalytics(response.data);
                console.log(response.data);
            })
            .catch(error => {
                console.error("There was an error fetching the analytics data!", error);
            });
    }, []);

    console.log(analytics);

    return (
        <div className="home-page">
            <h1>Sales Analytics</h1>
            <div className="analytics-section">
                <h2>Top Products Sold</h2>
                <ul>
                    {analytics.topProducts.map((product, index) => (
                        <li key={index}>{product.name}: {product.count} units</li>
                    ))}
                </ul>
            </div>

            <div className="analytics-section">
                <h2>Top Industries</h2>
                <ul>
                    {analytics.topIndustries.map((industry, index) => (
                        <li key={index}>{industry.name}: {industry.count} units</li>
                    ))}
                </ul>
            </div>

            <div className="analytics-section">
                <h2>Top Subgroups in Each Industry</h2>
                {analytics.topSubgroups.map((industry, index) => (
                    <div key={index} className="subgroup">
                        <h3>{industry.name}</h3>
                        <ul>
                            {industry.subgroups.map((subgroup, subIndex) => (
                                <li key={subIndex}>{subgroup.name}: {subgroup.count} units</li>
                            ))}
                        </ul>
                    </div>
                ))}
            </div>

            <div className="analytics-section">
                <h2>Sales Per Store</h2>
                <ul>
                    {Object.entries(analytics.salesPerStore).map(([storeId, sales], index) => (
                        <li key={index}>Store {storeId}: {sales} units</li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default HomePage;
