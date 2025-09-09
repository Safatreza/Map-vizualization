import React, { useMemo } from 'react';

const Controls = ({ customers, filteredCustomers, filters, onFilterChange }) => {
  // Get unique countries for filter dropdown
  const countries = useMemo(() => {
    if (!customers.length) return [];
    return [...new Set(customers.map(c => c.country).filter(c => c))].sort();
  }, [customers]);

  // Calculate statistics
  const stats = useMemo(() => {
    const total = filteredCustomers.length;
    const active = filteredCustomers.filter(c => c.is_active).length;
    const inactive = total - active;
    
    return { total, active, inactive };
  }, [filteredCustomers]);

  const handleStatusChange = (e) => {
    onFilterChange({ status: e.target.value });
  };

  const handleCountryChange = (e) => {
    onFilterChange({ country: e.target.value });
  };

  const handleSearchChange = (e) => {
    onFilterChange({ search: e.target.value });
  };

  return (
    <div className="controls">
      <div className="controls-header">Map Controls & Analytics</div>
      
      <div className="filter-group">
        <label htmlFor="statusFilter">Status:</label>
        <select 
          id="statusFilter" 
          value={filters.status} 
          onChange={handleStatusChange}
        >
          <option value="all">All Customers</option>
          <option value="active">Active Only</option>
          <option value="inactive">Inactive Only</option>
        </select>
      </div>
      
      <div className="filter-group">
        <label htmlFor="countryFilter">Country:</label>
        <select 
          id="countryFilter" 
          value={filters.country} 
          onChange={handleCountryChange}
        >
          <option value="all">All Countries</option>
          {countries.map(country => (
            <option key={country} value={country}>
              {country}
            </option>
          ))}
        </select>
      </div>
      
      <div className="filter-group">
        <label htmlFor="searchInput">Search:</label>
        <input 
          type="text" 
          id="searchInput" 
          placeholder="Customer name or number..."
          value={filters.search}
          onChange={handleSearchChange}
        />
      </div>
      
      <div className="stats">
        <div className="stat-item">
          <div className="stat-number">{stats.total}</div>
          <div className="stat-label">Total</div>
        </div>
        <div className="stat-item">
          <div className="stat-number">{stats.active}</div>
          <div className="stat-label">Active</div>
        </div>
        <div className="stat-item">
          <div className="stat-number">{stats.inactive}</div>
          <div className="stat-label">Inactive</div>
        </div>
      </div>
    </div>
  );
};

export default Controls;