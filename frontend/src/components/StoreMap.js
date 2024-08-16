// src/components/StoreMap.js
import React, { useEffect, useState, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './StoreMap.css';
import SidePanel from './SidePanel';

const StoreMap = () => {
    const [storeData, setStoreData] = useState([]);
    const [error, setError] = useState(null);
    const [selectedStore, setSelectedStore] = useState(null);
    const mapRef = useRef(null);

    useEffect(() => {
        const fetchStoreData = async () => {
            try {
                const response = await fetch('/api/store_locations');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setStoreData(data);
            } catch (error) {
                setError(error.toString());
            }
        };

        fetchStoreData();
    }, []);

    useEffect(() => {
        if (mapRef.current) {
            // Destroy previous map instance
            mapRef.current.off();
            mapRef.current.remove();
        }

        // Initialize the map
        const map = L.map('map').setView([20.5937, 78.9629], 5);
        mapRef.current = map;

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        // Add store markers
        storeData.forEach(store => {
            const marker = L.marker([store.latitude, store.longitude])
                .addTo(map)
                .bindTooltip(`<b>Store ID:</b> ${store.store_id}<br/><b>Total Sales:</b> ${store.total_sales}`)
                .on('click', () => {
                    setSelectedStore(store);
                });
        });
    }, [storeData]);

    return (
        <>
        <h2>Store Locations and Sales</h2>
        <div className="store-map-container">
            {error ? (
                <div className="error">{error}</div>
            ) : (
                <div id="map" style={{ height: '500px', width: '100%' }}></div>
            )}
            {selectedStore && (
                <SidePanel store={selectedStore} onClose={() => setSelectedStore(null)} />
            )}
        </div>
        </>
    );
};

export default StoreMap;
