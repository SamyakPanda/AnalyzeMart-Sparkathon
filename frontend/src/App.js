import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Home from './components/Home';
import Orders from './components/Orders';
import About from './components/About';
import './App.css';
import DemandForecast from './components/DemandForecast';
import StoreMap from './components/StoreMap';
import InventoryManagement from './components/InventoryManagement';
import Predictions from './components/Predictions';
import Customer from './components/Customer';

function App() {
    const [currentPage, setCurrentPage] = useState('home');

    const renderPage = () => {
        switch (currentPage) {
            case 'home':
                return <Home />;
            case 'orders':
                return <Orders />;
            case 'about':
                return <About />;
            case 'demand-forecast':
                return <DemandForecast/>;
            case 'store-map':
                return <StoreMap />;
            case 'inventory-management':
                return <InventoryManagement />;
            case 'product-details':
                return <Predictions/>
            case 'customer':
                return <Customer />;
            default:
                return <Home />;
        }
    };

    return (
        <div className="App">
            <Navbar setCurrentPage={setCurrentPage} />
            {renderPage()}
        </div>
    );
}

export default App;
