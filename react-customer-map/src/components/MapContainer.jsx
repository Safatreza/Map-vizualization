import React, { useState } from 'react';
import LeafletMap from './LeafletMap';
import MapControls from './MapControls';

const MapContainer = ({ customers, loading }) => {
  const [mapState, setMapState] = useState({
    mapType: 'roadmap', // 'roadmap' or 'satellite'
    is3DEnabled: false,
    streetViewVisible: false
  });

  const toggleMapType = () => {
    setMapState(prev => ({
      ...prev,
      mapType: prev.mapType === 'roadmap' ? 'satellite' : 'roadmap'
    }));
  };

  const toggle3D = () => {
    setMapState(prev => ({
      ...prev,
      is3DEnabled: !prev.is3DEnabled
    }));
  };

  const toggleStreetView = () => {
    setMapState(prev => ({
      ...prev,
      streetViewVisible: !prev.streetViewVisible
    }));
  };

  return (
    <div className="map-container">
      <LeafletMap 
        customers={customers}
        mapState={mapState}
        loading={loading}
      />
      
      <MapControls 
        mapState={mapState}
        onToggleMapType={toggleMapType}
        onToggle3D={toggle3D}
        onToggleStreetView={toggleStreetView}
      />
      
      <div className="legend">
        <h4>Legend</h4>
        <div className="legend-item">
          <div className="legend-color" style={{backgroundColor: '#28a745'}}></div>
          <span>Active Customer</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{backgroundColor: '#dc3545'}}></div>
          <span>Inactive Customer</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{backgroundColor: '#ffc107'}}></div>
          <span>Address Verified</span>
        </div>
      </div>
    </div>
  );
};

export default MapContainer;