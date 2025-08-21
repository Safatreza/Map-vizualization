import pandas as pd
import numpy as np
import json
import os
from datetime import datetime

def clean_and_standardize_data():
    """Clean and standardize all customer data from the CSV files"""
    
    print("Reading and processing customer data...")
    
    # Read the main CSV file
    df = pd.read_csv('updated_Excel_with_Customer_details - updated_Excel_with_Customer_details.csv.csv')
    
    # Clean column names
    df.columns = ['customer_number', 'customer_name', 'is_active', 'street', 'postal_code', 'city', 'country']
    
    print(f"Total records: {len(df)}")
    
    # Clean the data
    print("Cleaning data...")
    
    # Standardize active status
    df['is_active'] = df['is_active'].str.lower().map({'ja': True, 'nein': False, 'yes': True, 'no': False})
    df['is_active'] = df['is_active'].fillna(False)
    
    # Clean country codes
    df['country'] = df['country'].replace('0', '')
    df['country'] = df['country'].fillna('')
    
    # Clean postal codes
    df['postal_code'] = df['postal_code'].astype(str).str.strip()
    df['postal_code'] = df['postal_code'].replace('nan', '')
    
    # Clean cities
    df['city'] = df['city'].astype(str).str.strip()
    df['city'] = df['city'].replace('nan', '')
    
    # Clean streets
    df['street'] = df['street'].astype(str).str.strip()
    df['street'] = df['street'].replace('nan', '')
    
    # Create full address for geocoding
    df['full_address'] = df.apply(lambda row: create_full_address(row), axis=1)
    
    # Remove rows with no address information
    df_with_addresses = df[df['full_address'] != ''].copy()
    
    # Create customer identifier (name or number if name is missing)
    df_with_addresses['customer_identifier'] = df_with_addresses.apply(lambda row: 
        row['customer_name'] if pd.notna(row['customer_name']) and row['customer_name'].strip() != '' 
        else f"Customer {row['customer_number']}", axis=1)
    
    # Add a unique ID for each record
    df_with_addresses['id'] = range(1, len(df_with_addresses) + 1)
    
    print(f"Records with addresses: {len(df_with_addresses)}")
    print(f"Active customers: {df_with_addresses['is_active'].sum()}")
    print(f"Inactive customers: {len(df_with_addresses) - df_with_addresses['is_active'].sum()}")
    
    # Show data quality statistics
    print(f"\nData quality:")
    print(f"Records with street: {df_with_addresses['street'].str.len() > 0}.sum()")
    print(f"Records with postal code: {df_with_addresses['postal_code'].str.len() > 0}.sum()")
    print(f"Records with city: {df_with_addresses['city'].str.len() > 0}.sum()")
    print(f"Records with country: {df_with_addresses['country'].str.len() > 0}.sum()")
    
    return df_with_addresses

def create_full_address(row):
    """Create a full address string for geocoding"""
    parts = []
    
    if pd.notna(row['street']) and row['street'].strip() != '':
        parts.append(row['street'].strip())
    
    if pd.notna(row['postal_code']) and row['postal_code'].strip() != '':
        parts.append(row['postal_code'].strip())
    
    if pd.notna(row['city']) and row['city'].strip() != '':
        parts.append(row['city'].strip())
    
    if pd.notna(row['country']) and row['country'].strip() != '':
        parts.append(row['country'].strip())
    
    return ', '.join(parts) if parts else ''

def create_sample_geocoded_data(df, sample_size=100):
    """Create sample geocoded data for demonstration purposes"""
    
    print(f"Creating sample geocoded data for {sample_size} customers...")
    
    # Sample customers with good address data
    sample_df = df.sample(n=min(sample_size, len(df)), random_state=42)
    
    # Create mock coordinates for demonstration
    # In a real scenario, you would use a geocoding service
    sample_data = []
    
    # Germany coordinates (approximate center)
    germany_coords = {
        'DE': {'lat': 51.1657, 'lng': 10.4515},
        'AT': {'lat': 47.5162, 'lng': 14.5501},
        'IT': {'lat': 41.8719, 'lng': 12.5674},
        'FR': {'lat': 46.2276, 'lng': 2.2137},
        'ES': {'lat': 40.4637, 'lng': -3.7492},
        'PL': {'lat': 51.9194, 'lng': 19.1451},
        'CZ': {'lat': 49.8175, 'lng': 15.4730},
        'PT': {'lat': 39.3999, 'lng': -8.2245},
        'LU': {'lat': 49.8153, 'lng': 6.1296},
        'CH': {'lat': 46.8182, 'lng': 8.2275}
    }
    
    for idx, row in sample_df.iterrows():
        # Get base coordinates for the country
        country = row['country'] if row['country'] else 'DE'
        base_coords = germany_coords.get(country, germany_coords['DE'])
        
        # Add some random variation to spread out customers
        lat_variation = np.random.uniform(-0.5, 0.5)
        lng_variation = np.random.uniform(-0.5, 0.5)
        
        sample_data.append({
            'id': row['id'],
            'customer_number': row['customer_number'],
            'customer_identifier': row['customer_identifier'],
            'is_active': bool(row['is_active']),
            'street': row['street'],
            'postal_code': row['postal_code'],
            'city': row['city'],
            'country': row['country'],
            'full_address': row['full_address'],
            'latitude': base_coords['lat'] + lat_variation,
            'longitude': base_coords['lng'] + lng_variation
        })
    
    return sample_data

def save_data_for_map(data, filename='customers_for_map.json'):
    """Save data in the format needed for the map"""
    
    map_data = {
        'metadata': {
            'total_customers': len(data),
            'active_customers': sum(1 for c in data if c['is_active']),
            'inactive_customers': sum(1 for c in data if not c['is_active']),
            'generated_at': datetime.now().isoformat(),
            'note': 'This is sample data with mock coordinates for demonstration purposes'
        },
        'customers': data
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(map_data, f, ensure_ascii=False, indent=2)
    
    print(f"Map data saved to {filename}")
    return map_data

def create_csv_summary(df, filename='customer_summary.csv'):
    """Create a summary CSV file"""
    
    summary = df.groupby(['country', 'is_active']).size().unstack(fill_value=0)
    summary.columns = ['Inactive', 'Active']
    summary['Total'] = summary['Active'] + summary['Inactive']
    
    summary.to_csv(filename)
    print(f"Summary saved to {filename}")
    
    return summary

def main():
    """Main function to process all customer data"""
    print("=== AboutWater Customer Data Processing ===")
    print()
    
    # Clean and standardize the data
    df = clean_and_standardize_data()
    
    # Create sample geocoded data
    sample_data = create_sample_geocoded_data(df, sample_size=200)
    
    # Save data for the map
    map_data = save_data_for_map(sample_data)
    
    # Create summary
    summary = create_csv_summary(df)
    
    print("\n=== Processing Complete ===")
    print(f"Total customers processed: {len(df)}")
    print(f"Sample data created: {len(sample_data)}")
    print(f"Active customers in sample: {map_data['metadata']['active_customers']}")
    print(f"Inactive customers in sample: {map_data['metadata']['inactive_customers']}")
    
    print("\nFiles created:")
    print("- customers_for_map.json (for the map)")
    print("- customer_summary.csv (summary statistics)")
    
    print("\nNext steps:")
    print("1. Open the HTML map file to visualize customers")
    print("2. Use the JSON data for further analysis")
    print("3. For production use, replace mock coordinates with real geocoding")

if __name__ == "__main__":
    main()
