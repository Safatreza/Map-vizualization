import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Controls from './components/Controls';
import MapContainer from './components/MapContainer';
import LoadingSpinner from './components/LoadingSpinner';
import { useCustomers } from './hooks/useCustomers';
import './styles/App.css';

function App() {
  const [filters, setFilters] = useState({
    status: 'all',
    country: 'all',
    search: ''
  });

  const { customers, loading, error, filteredCustomers } = useCustomers(filters);

  const handleFilterChange = (newFilters) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  };

  if (error) {
    return (
      <div className="error-container">
        <h2>Error Loading Customer Data</h2>
        <p>{error}</p>
        <p>Please make sure the customer data file is available and try refreshing the page.</p>
      </div>
    );
  }

  return (
    <div className="app">
      <Header />
      
      <Controls 
        customers={customers}
        filteredCustomers={filteredCustomers}
        filters={filters}
        onFilterChange={handleFilterChange}
      />
      
      <MapContainer 
        customers={filteredCustomers}
        loading={loading}
      />
      
      {loading && <LoadingSpinner />}
    </div>
  );
}

export default App;
