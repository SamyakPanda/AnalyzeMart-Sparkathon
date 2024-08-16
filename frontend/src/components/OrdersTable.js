import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './OrdersTable.css';

const OrdersTable = () => {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        axios.get('/api/orders')
            .then(response => {
                setOrders(response.data);
                setLoading(false);
            })
            .catch(error => {
                console.error("There was an error fetching the orders!", error);
                setLoading(false);
            });
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div className="orders-table-container">
            <h1>Orders Table</h1>
            <table className="orders-table">
                <thead>
                    <tr>
                        <th>Order ID</th>
                        <th>Customer ID</th>
                        <th>Product Name</th>
                        <th>Price Sold At</th>
                        <th>Industry</th>
                        <th>Subgroup</th>
                        {/* <th>Order Time</th> */}
                        <th>Order Date</th>
                        <th>Store ID</th>
                    </tr>
                </thead>
                <tbody>
                    {orders.map(order => (
                        <tr key={order.order_id}>
                            <td>{order.order_id}</td>
                            <td>{order.customer_id}</td>
                            <td>{order.product_name}</td>
                            <td>{order.price_sold_at}</td>
                            <td>{order.industry}</td>
                            <td>{order.subgroup}</td>
                            {/* <td>{order.order_time}</td> */}
                            <td>{order.order_date}</td>
                            <td>{order.store_id}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default OrdersTable;
