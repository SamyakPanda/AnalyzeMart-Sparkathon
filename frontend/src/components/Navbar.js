import React from 'react';
import './Navbar.css';
import logo from '../static/Strong Stock.png'; // Adjust the path to your logo

const Navbar = ({ setCurrentPage }) => {
    return (
        <nav className="navbar">
            <div className="navbar-container">
                <div className="navbar-logo" onClick={() => setCurrentPage('home')}>
                    <img src={logo} alt="Logo" className="logo-image" />
                    <span>AnalyzeMart</span>    
                </div>
                <div className="navbar-menu">
                    <div className="navbar-item" onClick={() => setCurrentPage('home')}>Home</div>
                    <div className="navbar-item" onClick={() => setCurrentPage('orders')}>Orders</div>
                    <div className="navbar-item" onClick={() => setCurrentPage('demand-forecast')}>Demand Forecasts</div>
                    <div className="navbar-item" onClick={() => setCurrentPage('store-map')}>Store Map</div>
                    <div className="navbar-item" onClick={() => setCurrentPage('inventory-management')}>Inventory Management</div>
                    <div className="navbar-item" onClick={() => setCurrentPage('product-details')}>Product Details</div>
                    <div className="navbar-item" onClick={() => setCurrentPage('customer')}>Customer</div>
                    <div className="navbar-item" onClick={() => setCurrentPage('about')}>About</div>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
