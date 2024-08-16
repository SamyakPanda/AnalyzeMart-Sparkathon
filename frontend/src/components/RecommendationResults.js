import React from 'react';
import './Customer.css'; // Ensure this import is present

function RecommendationResults({ data }) {
    return (
        <div className="RecommendationResults">
            <h2>Recommendations</h2>
            <h3>Top 10 Recommendations:</h3>
            <ul>
                {data.top_10_recommendations.map((item, index) => (
                    <li key={index}>{item}</li>
                ))}
            </ul>
            <h3>Most Interested Category:</h3>
            <p>{data.most_interested_category}</p>
            <h3>Preferred Price Range:</h3>
            <p>{data.preferred_price_range ? data.preferred_price_range.toFixed(2) : 'N/A'}</p>
            <h3>Top 3 Recommendations per Category:</h3>
            {Object.keys(data.top_3_per_category).map((category, index) => (
                <div key={index}>
                    <h4>{category}</h4>
                    <ul>
                        {data.top_3_per_category[category].map((item, idx) => (
                            <li key={idx}>{item}</li>
                        ))}
                    </ul>
                </div>
            ))}
            <img src={`data:image/png;base64,${data.plot_image}`} alt="Customer Clusters" />
        </div>
    );
}

export default RecommendationResults;
