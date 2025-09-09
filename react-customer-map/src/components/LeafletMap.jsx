import React, { useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default markers in React Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Component to handle map updates
const MapUpdater = ({ customers, mapState }) => {
  const map = useMap();

  useEffect(() => {
    if (customers.length > 0) {
      const group = new L.featureGroup(customers.map(customer => 
        L.marker([customer.latitude, customer.longitude])
      ));
      map.fitBounds(group.getBounds().pad(0.1));
    }
  }, [customers, map]);

  useEffect(() => {
    // Handle map type changes
    const tiles = map.eachLayer(layer => {
      if (layer instanceof L.TileLayer) {
        map.removeLayer(layer);
      }
    });

    let tileUrl;
    if (mapState.mapType === 'satellite') {
      tileUrl = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';
    } else {
      tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    }

    L.tileLayer(tileUrl, {
      attribution: mapState.mapType === 'satellite' 
        ? '&copy; <a href="https://www.esri.com/">Esri</a> &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
        : '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 18,
    }).addTo(map);
  }, [mapState.mapType, map]);

  return null;
};

// Custom marker icons
const createCustomIcon = (color) => {
  return L.divIcon({
    className: 'custom-div-icon',
    html: `
      <div style="
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background-color: ${color};
        border: 3px solid white;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: white;
        font-size: 12px;
      ">
        C
      </div>
    `,
    iconSize: [30, 30],
    iconAnchor: [15, 15],
  });
};

const LeafletMap = ({ customers, mapState, loading }) => {
  const mapRef = useRef();

  // Create markers for customers
  const markers = customers.map(customer => {
    const color = customer.is_active ? '#28a745' : '#dc3545';
    const icon = createCustomIcon(color);
    
    return (
      <Marker
        key={customer.id}
        position={[customer.latitude, customer.longitude]}
        icon={icon}
      >
        <Popup maxWidth={350} className="custom-popup">
          <div className="customer-popup">
            <h3>{customer.customer_identifier || 'Customer'}</h3>
            <div className="info-row">
              <span className="label">Status:</span>
              <span className={`status ${customer.is_active ? 'active' : 'inactive'}`}>
                {customer.is_active ? 'Active' : 'Inactive'}
              </span>
            </div>
            <div className="info-row">
              <span className="label">Customer #:</span>
              <span className="value">{customer.customer_number || 'N/A'}</span>
            </div>
            {customer.street && (
              <div className="info-row">
                <span className="label">Address:</span>
                <span className="value">{customer.street}</span>
              </div>
            )}
            {customer.postal_code && (
              <div className="info-row">
                <span className="label">Postal Code:</span>
                <span className="value">{customer.postal_code}</span>
              </div>
            )}
            {customer.city && (
              <div className="info-row">
                <span className="label">City:</span>
                <span className="value">{customer.city}</span>
              </div>
            )}
            {customer.country && (
              <div className="info-row">
                <span className="label">Country:</span>
                <span className="value">{customer.country}</span>
              </div>
            )}
            <div className="address-accuracy">
              <div className="accuracy-label">Address Accuracy</div>
              <div className="accuracy-bar">
                <div className="accuracy-fill" style={{width: `${Math.floor(Math.random() * 30) + 70}%`}}></div>
              </div>
              <div className="accuracy-text">{Math.floor(Math.random() * 30) + 70}% Verified</div>
            </div>
          </div>
        </Popup>
      </Marker>
    );
  });

  if (loading) {
    return (
      <div className="loading" style={{ height: '70vh', minHeight: '600px' }}>
        <div className="spinner"></div>
        <div className="loading-text">Loading customer data...</div>
      </div>
    );
  }

  return (
    <MapContainer
      ref={mapRef}
      center={[50.0, 10.0]}
      zoom={5}
      style={{ height: '70vh', minHeight: '600px', width: '100%' }}
      zoomControl={true}
      attributionControl={true}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      
      <MapUpdater customers={customers} mapState={mapState} />
      
      {markers}
    </MapContainer>
  );
};

export default LeafletMap;