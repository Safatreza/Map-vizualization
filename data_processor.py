import pandas as pd
import numpy as np
import re
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import time
import json

def clean_customer_data():
    """Clean and standardize customer data from CSV files"""
    
    # Read the main CSV file
    print("Reading customer data...")
    df = pd.read_csv('updated_Excel_with_Customer_details - updated_Excel_with_Customer_details.csv.csv')
    
    # Clean column names
    df.columns = ['customer_number', 'customer_name', 'is_active', 'street', 'postal_code', 'city', 'country']
    
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
    df = df[df['full_address'] != '']
    
    # Create customer identifier (name or number if name is missing)
    df['customer_identifier'] = df.apply(lambda row: 
        row['customer_name'] if pd.notna(row['customer_name']) and row['customer_name'].strip() != '' 
        else f"Customer {row['customer_number']}", axis=1)
    
    print(f"Total customers with addresses: {len(df)}")
    print(f"Active customers: {df['is_active'].sum()}")
    print(f"Inactive customers: {len(df) - df['is_active'].sum()}")
    
    return df

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

def geocode_addresses(df, sample_size=None):
    """Geocode addresses to get coordinates"""
    
    if sample_size:
        df = df.sample(n=min(sample_size, len(df)), random_state=42)
    
    geolocator = Nominatim(user_agent="aboutwater_customers")
    
    coordinates = []
    
    for idx, row in df.iterrows():
        try:
            print(f"Geocoding: {row['full_address']}")
            location = geolocator.geocode(row['full_address'])
            
            if location:
                coordinates.append({
                    'customer_number': row['customer_number'],
                    'customer_identifier': row['customer_identifier'],
                    'is_active': row['is_active'],
                    'street': row['street'],
                    'postal_code': row['postal_code'],
                    'city': row['city'],
                    'country': row['country'],
                    'full_address': row['full_address'],
                    'latitude': location.latitude,
                    'longitude': location.longitude
                })
                print(f"✓ Found coordinates: {location.latitude}, {location.longitude}")
            else:
                print(f"✗ No coordinates found")
            
            # Be respectful to the geocoding service
            time.sleep(1)
            
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            print(f"✗ Geocoding error: {e}")
            continue
    
    return pd.DataFrame(coordinates)

def save_processed_data(df, filename='processed_customers.json'):
    """Save processed data to JSON file"""
    data = df.to_dict('records')
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Processed data saved to {filename}")

def main():
    """Main function to process customer data"""
    print("Starting customer data processing...")
    
    # Clean the data
    df = clean_customer_data()
    
    # For demonstration, let's process a sample first
    print("\nGeocoding sample addresses...")
    sample_df = geocode_addresses(df, sample_size=50)
    
    if not sample_df.empty:
        # Save the sample data
        save_processed_data(sample_df, 'sample_customers_geocoded.json')
        
        print(f"\nSuccessfully geocoded {len(sample_df)} addresses")
        print("Sample data saved to 'sample_customers_geocoded.json'")
        
        # Show some statistics
        print(f"\nActive customers geocoded: {sample_df['is_active'].sum()}")
        print(f"Inactive customers geocoded: {len(sample_df) - sample_df['is_active'].sum()}")
        
        # Show countries
        countries = sample_df['country'].value_counts()
        print(f"\nCountries represented:")
        for country, count in countries.head(10).items():
            print(f"  {country}: {count}")
    else:
        print("No addresses were successfully geocoded")

if __name__ == "__main__":
    main()
