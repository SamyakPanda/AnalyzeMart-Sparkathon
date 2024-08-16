import React from 'react';
import './Customer.css'; // Ensure this import is present

function RecommendationForm({ customerId, setCustomerId, handleSubmit }) {
    return (
        <form className="RecommendationForm" onSubmit={handleSubmit}>
            <label htmlFor="customerId">Customer ID:</label>
            <input
                type="text"
                id="customerId"
                value={customerId}
                onChange={(e) => setCustomerId(e.target.value)}
                required
            />
            <button type="submit">Get Recommendations</button>
        </form>
    );
}

export default RecommendationForm;
