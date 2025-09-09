import { useState, useEffect, useMemo } from 'react';

export function useCustomers(filters) {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadCustomers = async () => {
      try {
        setLoading(true);
        const response = await fetch('/customers_for_map.json');
        
        if (!response.ok) {
          throw new Error('Failed to load customer data');
        }
        
        const data = await response.json();
        const customerData = data.customers || [];
        
        // Filter out customers with invalid coordinates
        const validCustomers = customerData.filter(customer => 
          customer.latitude && 
          customer.longitude && 
          !isNaN(customer.latitude) && 
          !isNaN(customer.longitude) &&
          customer.latitude !== 0 && 
          customer.longitude !== 0
        );
        
        setCustomers(validCustomers);
        setError(null);
        console.log(`Loaded ${validCustomers.length} customers with valid coordinates`);
        
      } catch (err) {
        console.error('Error loading customer data:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadCustomers();
  }, []);

  // Filter customers based on current filters
  const filteredCustomers = useMemo(() => {
    if (!customers.length) return [];

    return customers.filter(customer => {
      // Status filter
      if (filters.status !== 'all') {
        const isActive = filters.status === 'active';
        if (customer.is_active !== isActive) return false;
      }
      
      // Country filter
      if (filters.country !== 'all' && customer.country !== filters.country) {
        return false;
      }
      
      // Search filter
      if (filters.search) {
        const searchText = `${customer.customer_identifier} ${customer.customer_number} ${customer.city} ${customer.country}`.toLowerCase();
        if (!searchText.includes(filters.search.toLowerCase())) return false;
      }
      
      return true;
    });
  }, [customers, filters]);

  return {
    customers,
    filteredCustomers,
    loading,
    error
  };
}