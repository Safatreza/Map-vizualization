import React from 'react';

const LoadingSpinner = () => {
  return (
    <div className="loading">
      <div className="spinner"></div>
      <div className="loading-text">Loading enhanced customer data...</div>
      <div className="loading-progress">
        <div className="loading-progress-bar"></div>
      </div>
    </div>
  );
};

export default LoadingSpinner;