import React from 'react';
import { Eye, Mountain, MapPin } from 'lucide-react';

const MapControls = ({ mapState, onToggleMapType, onToggle3D, onToggleStreetView }) => {
  return (
    <div className="map-controls">
      <button 
        className={`map-control-btn ${mapState.mapType === 'satellite' ? 'active' : ''}`}
        onClick={onToggleMapType}
        title="Toggle Satellite View"
      >
        <Eye size={20} />
      </button>
      
      <button 
        className={`map-control-btn ${mapState.is3DEnabled ? 'active' : ''}`}
        onClick={onToggle3D}
        title="Toggle 3D Terrain"
      >
        <Mountain size={20} />
      </button>
      
      <button 
        className={`map-control-btn ${mapState.streetViewVisible ? 'active' : ''}`}
        onClick={onToggleStreetView}
        title="Toggle Street View"
      >
        <MapPin size={20} />
      </button>
    </div>
  );
};

export default MapControls;