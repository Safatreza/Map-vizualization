#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check for Munich customers in the generated data
"""

import json

def check_munich_customers():
    try:
        with open('customers_for_map.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Total customers: {len(data['customers'])}")
        
        # Find Munich customers
        munich_customers = []
        for customer in data['customers']:
            city = str(customer['city']).strip()
            if 'München' in city or 'Munich' in city:
                munich_customers.append(customer)
        
        print(f"\nMunich customers found: {len(munich_customers)}")
        
        if munich_customers:
            print("\nSample Munich customer:")
            sample = munich_customers[0]
            print(f"  Customer ID: {sample['customer_identifier']}")
            print(f"  City: {sample['city']}")
            print(f"  Street: {sample['street']}")
            print(f"  Coordinates: {sample['latitude']:.6f}, {sample['longitude']:.6f}")
            print(f"  Active: {sample['is_active']}")
        
        # Check for other major German cities
        major_cities = ['Berlin', 'Hamburg', 'Köln', 'Frankfurt', 'Stuttgart', 'Düsseldorf']
        print(f"\nChecking other major cities:")
        for city_name in major_cities:
            city_customers = [c for c in data['customers'] if city_name in str(c['city'])]
            print(f"  {city_name}: {len(city_customers)} customers")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_munich_customers()
