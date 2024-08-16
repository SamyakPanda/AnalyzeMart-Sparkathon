import React, { useState } from 'react';
import axios from 'axios';
import RecommendationForm from './RecommendationForm';
import RecommendationResults from './RecommendationResults';
import './Customer.css'; // Ensure this import is present

function Customer() {
    const [customerId, setCustomerId] = useState('');
    const [results, setResults] = useState(null);
    const [error, setError] = useState(null);

    const fetchRecommendations = async (id) => {
        try {
            const response = await axios.get(`http://localhost:5001/api/recommendations/${id}`);
            setResults(response.data);
            setError(null);
        } catch (err) {
            setError(err.message);
            setResults(null);
        }
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        fetchRecommendations(customerId);
    };

    return (
        <div className="App">
            <h1>Customer Recommendations</h1>
            <RecommendationForm
                customerId={customerId}
                setCustomerId={setCustomerId}
                handleSubmit={handleSubmit}
            />
            {error && <p className="error">{error}</p>}
            {results && <RecommendationResults data={results} />}
        </div>
    );
}

export default Customer;
