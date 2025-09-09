import React from 'react';

const Header = () => {
  return (
    <div className="header">
      <div className="server-id">SERVER: AW-2024-001</div>
      <div className="logo-container">
        <div className="logo">
          <div className="logo-circle">
            <div className="logo-letter">A</div>
            <div className="logo-droplet"></div>
          </div>
          <div className="logo-text">aboutwater</div>
        </div>
      </div>
      <h1>Enhanced Customer Map</h1>
      <p>Interactive React visualization with Google Maps integration</p>
    </div>
  );
};

export default Header;