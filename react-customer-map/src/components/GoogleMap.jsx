import React, { useEffect, useRef, useCallback } from 'react';

const GoogleMap = ({ customers, mapState, loading }) => {
  const mapRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const markersRef = useRef([]);

  // Custom map styles for professional look
  const getCustomMapStyles = () => [
    {
      featureType: 'water',
      elementType: 'geometry',
      stylers: [{ color: '#e9e9e9' }, { lightness: 17 }]
    },
    {
      featureType: 'landscape',
      elementType: 'geometry',
      stylers: [{ color: '#f5f5f2' }, { lightness: 20 }]
    },
    {
      featureType: 'road.highway',
      elementType: 'geometry.stroke',
      stylers: [{ color: '#ffffff' }, { lightness: 29 }]
    },
    {
      featureType: 'road.highway',
      elementType: 'geometry.fill',
      stylers: [{ color: '#ffffff' }, { lightness: 17 }]
    },
    {
      featureType: 'road.arterial',
      elementType: 'geometry',
      stylers: [{ color: '#ffffff' }, { lightness: 18 }]
    },
    {
      featureType: 'road.local',
      elementType: 'geometry',
      stylers: [{ color: '#ffffff' }, { lightness: 16 }]
    },
    {
      featureType: 'poi',
      elementType: 'geometry',
      stylers: [{ color: '#f5f5f2' }, { lightness: 21 }]
    },
    {
      featureType: 'poi.park',
      elementType: 'geometry',
      stylers: [{ color: '#dedede' }, { lightness: 21 }]
    }
  ];

  // Initialize map
  const initializeMap = useCallback(() => {
    if (!mapRef.current || !window.google || !window.google.maps) {
      console.error('Google Maps API not loaded');
      return;
    }

    try {
      mapInstanceRef.current = new window.google.maps.Map(mapRef.current, {
        center: { lat: 50.0, lng: 10.0 },
        zoom: 5,
        mapTypeId: window.google.maps.MapTypeId.ROADMAP,
        mapTypeControl: false,
        streetViewControl: false,
        fullscreenControl: false,
        zoomControl: true,
        styles: getCustomMapStyles(),
        tilt: 0
      });

      // Add fade-in effect
      if (mapRef.current) {
        mapRef.current.style.opacity = '0';
        mapRef.current.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
          if (mapRef.current) {
            mapRef.current.style.transition = 'all 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
            mapRef.current.style.opacity = '1';
            mapRef.current.style.transform = 'translateY(0)';
          }
        }, 100);
      }

      console.log('Google Map initialized successfully');
    } catch (error) {
      console.error('Error initializing Google Map:', error);
    }
  }, []);

  // Initialize map when Google Maps API is available
  useEffect(() => {
    if (window.google && window.google.maps) {
      initializeMap();
    }
  }, [initializeMap]);

  // Update map type
  useEffect(() => {
    if (mapInstanceRef.current && window.google) {
      const mapTypeId = mapState.mapType === 'satellite' 
        ? window.google.maps.MapTypeId.SATELLITE 
        : window.google.maps.MapTypeId.ROADMAP;
      mapInstanceRef.current.setMapTypeId(mapTypeId);
    }
  }, [mapState.mapType]);

  // Update 3D tilt
  useEffect(() => {
    if (mapInstanceRef.current) {
      mapInstanceRef.current.setTilt(mapState.is3DEnabled ? 45 : 0);
    }
  }, [mapState.is3DEnabled]);

  // Update street view
  useEffect(() => {
    if (mapInstanceRef.current) {
      const streetView = mapInstanceRef.current.getStreetView();
      if (streetView) {
        streetView.setVisible(mapState.streetViewVisible);
      }
    }
  }, [mapState.streetViewVisible]);

  // Create marker SVG
  const createMarkerSVG = (color, borderColor) => {
    const svg = `
      <svg width="36" height="36" viewBox="0 0 36 36" xmlns="http://www.w3.org/2000/svg">
        <circle cx="18" cy="18" r="16" fill="${color}" stroke="${borderColor}" stroke-width="3"/>
        <text x="18" y="24" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="14" font-weight="bold">
          C
        </text>
      </svg>
    `;
    return 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(svg);
  };

  // Create info window content
  const createInfoWindowContent = (customer) => {
    const statusClass = customer.is_active ? 'active' : 'inactive';
    const statusText = customer.is_active ? 'Active' : 'Inactive';
    const accuracy = Math.floor(Math.random() * 30) + 70; // Mock accuracy 70-100%
    
    return `
      <div class="customer-popup">
        <h3>${customer.customer_identifier || 'Customer'}</h3>
        <div class="info-row">
          <span class="label">Status:</span>
          <span class="status ${statusClass}">${statusText}</span>
        </div>
        <div class="info-row">
          <span class="label">Customer #:</span>
          <span class="value">${customer.customer_number || 'N/A'}</span>
        </div>
        ${customer.street ? `<div class="info-row">
          <span class="label">Address:</span>
          <span class="value">${customer.street}</span>
        </div>` : ''}
        ${customer.postal_code ? `<div class="info-row">
          <span class="label">Postal Code:</span>
          <span class="value">${customer.postal_code}</span>
        </div>` : ''}
        ${customer.city ? `<div class="info-row">
          <span class="label">City:</span>
          <span class="value">${customer.city}</span>
        </div>` : ''}
        ${customer.country ? `<div class="info-row">
          <span class="label">Country:</span>
          <span class="value">${customer.country}</span>
        </div>` : ''}
        
        <div class="address-accuracy">
          <div class="accuracy-label">Address Accuracy</div>
          <div class="accuracy-bar">
            <div class="accuracy-fill" style="width: ${accuracy}%"></div>
          </div>
          <div class="accuracy-text">${accuracy}% Verified</div>
        </div>
      </div>
    `;
  };

  // Clear all markers
  const clearMarkers = useCallback(() => {
    markersRef.current.forEach(marker => {
      if (marker && marker.setMap) {
        marker.setMap(null);
      }
    });
    markersRef.current = [];
  }, []);

  // Create markers for customers
  const createMarkers = useCallback(() => {
    if (!mapInstanceRef.current || !window.google || loading || !customers.length) {
      return;
    }

    console.log(`Creating ${customers.length} markers...`);

    customers.forEach((customer, index) => {
      try {
        const color = customer.is_active ? '#28a745' : '#dc3545';
        const borderColor = customer.is_active ? '#1e7e34' : '#c82333';
        
        const marker = new window.google.maps.Marker({
          position: { 
            lat: parseFloat(customer.latitude), 
            lng: parseFloat(customer.longitude) 
          },
          map: mapInstanceRef.current,
          icon: {
            url: createMarkerSVG(color, borderColor),
            scaledSize: new window.google.maps.Size(36, 36),
            anchor: new window.google.maps.Point(18, 18)
          },
          title: customer.customer_identifier || `Customer ${index + 1}`,
          animation: window.google.maps.Animation.DROP
        });

        const infoWindow = new window.google.maps.InfoWindow({
          content: createInfoWindowContent(customer),
          maxWidth: 350
        });

        marker.addListener('click', () => {
          infoWindow.open(mapInstanceRef.current, marker);
        });

        marker.addListener('mouseover', () => {
          marker.setAnimation(window.google.maps.Animation.BOUNCE);
        });

        marker.addListener('mouseout', () => {
          marker.setAnimation(null);
        });

        markersRef.current.push(marker);
      } catch (error) {
        console.error(`Error creating marker for customer ${customer.id}:`, error);
      }
    });

    // Fit map to show all markers if we have any
    if (markersRef.current.length > 0) {
      try {
        const bounds = new window.google.maps.LatLngBounds();
        markersRef.current.forEach(marker => {
          const position = marker.getPosition();
          if (position) {
            bounds.extend(position);
          }
        });
        
        mapInstanceRef.current.fitBounds(bounds);
        
        // Limit zoom level
        const listener = window.google.maps.event.addListener(mapInstanceRef.current, 'idle', function() {
          if (mapInstanceRef.current.getZoom() > 10) {
            mapInstanceRef.current.setZoom(10);
          }
          window.google.maps.event.removeListener(listener);
        });
      } catch (error) {
        console.error('Error fitting bounds:', error);
      }
    }
  }, [customers, loading, createMarkerSVG, createInfoWindowContent]);

  // Update markers when customers change
  useEffect(() => {
    clearMarkers();
    createMarkers();
  }, [customers, clearMarkers, createMarkers]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      clearMarkers();
    };
  }, [clearMarkers]);

  if (!window.google) {
    return (
      <div className="loading" style={{ height: '70vh', minHeight: '600px' }}>
        <div className="spinner"></div>
        <div className="loading-text">Loading Google Maps...</div>
      </div>
    );
  }

  return (
    <div 
      ref={mapRef} 
      id="map" 
      style={{ 
        width: '100%', 
        height: '70vh', 
        minHeight: '600px',
        backgroundColor: '#f0f0f0'
      }} 
    />
  );
};

export default GoogleMap;