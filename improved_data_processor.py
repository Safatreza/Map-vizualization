import pandas as pd
import numpy as np
import json
import re
from datetime import datetime

def clean_and_standardize_data():
    """Clean and standardize all customer data from the CSV files with improved data quality handling"""
    
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
    
    # Clean and validate country codes
    df['country'] = clean_country_codes(df['country'])
    
    # Clean postal codes
    df['postal_code'] = df['postal_code'].astype(str).str.strip()
    df['postal_code'] = df['postal_code'].replace(['nan', '0', ''], '')
    
    # Clean cities
    df['city'] = df['city'].astype(str).str.strip()
    df['city'] = df['city'].replace(['nan', '0'], '')
    
    # Clean streets
    df['street'] = df['street'].astype(str).str.strip()
    df['street'] = df['street'].replace(['nan', '0'], '')
    
    # Create full address for geocoding
    df['full_address'] = df.apply(lambda row: create_full_address(row), axis=1)
    
    # Remove rows with no address information
    df_with_addresses = df[df['full_address'] != ''].copy()
    
    # Create customer identifier (name or number if name is missing)
    df_with_addresses['customer_identifier'] = df_with_addresses.apply(lambda row: 
        row['customer_name'] if pd.notna(row['customer_name']) and row['customer_name'].strip() != '' 
        else f"Customer {int(row['customer_number'])}", axis=1)
    
    # Add a unique ID for each record
    df_with_addresses['id'] = range(1, len(df_with_addresses) + 1)
    
    print(f"Records with addresses: {len(df_with_addresses)}")
    print(f"Active customers: {df_with_addresses['is_active'].sum()}")
    print(f"Inactive customers: {len(df_with_addresses) - df_with_addresses['is_active'].sum()}")
    
    # Show data quality statistics
    print(f"\nData quality:")
    print(f"Records with street: {(df_with_addresses['street'].str.len() > 0).sum()}")
    print(f"Records with postal code: {(df_with_addresses['postal_code'].str.len() > 0).sum()}")
    print(f"Records with city: {(df_with_addresses['city'].str.len() > 0).sum()}")
    print(f"Records with country: {(df_with_addresses['country'].str.len() > 0).sum()}")
    
    return df_with_addresses

def clean_country_codes(country_series):
    """Clean and standardize country codes"""
    
    # Define valid country codes
    valid_countries = {
        'DE', 'AT', 'IT', 'FR', 'ES', 'PL', 'CZ', 'PT', 'LU', 'CH', 'NL', 'BE', 'DK', 'SE', 'NO', 'FI',
        'GB', 'IE', 'HR', 'SI', 'SK', 'HU', 'RO', 'BG', 'GR', 'CY', 'LT', 'LI', 'MC', 'MA', 'ZA', 'US',
        'CN', 'IN', 'IS', 'GE', 'RE', 'SG'
    }
    
    def clean_country(country):
        if pd.isna(country) or country == '' or country == '0':
            return ''
        
        # Convert to string and clean
        country_str = str(country).strip().upper()
        
        # Check if it's a valid country code
        if country_str in valid_countries:
            return country_str
        
        # Check if it looks like an address (contains numbers or common address words)
        if re.search(r'\d', country_str) or any(word in country_str.lower() for word in ['straße', 'str', 'platz', 'weg', 'allee']):
            return ''
        
        # Check if it's a variation of known countries
        country_variations = {
            'D': 'DE', 'DEUTSCHLAND': 'DE', 'GERMANY': 'DE',
            'AT': 'AT', 'ÖSTERREICH': 'AT', 'AUSTRIA': 'AT',
            'IT': 'IT', 'ITALIEN': 'IT', 'ITALY': 'IT',
            'FR': 'FR', 'FRANKREICH': 'FR', 'FRANCE': 'FR',
            'ES': 'ES', 'SPANIEN': 'ES', 'SPAIN': 'ES',
            'PL': 'PL', 'POLEN': 'PL', 'POLAND': 'PL',
            'CZ': 'CZ', 'TSCHECHIEN': 'CZ', 'CZECH': 'CZ',
            'CH': 'CH', 'SCHWEIZ': 'CH', 'SWITZERLAND': 'CH',
            'NL': 'NL', 'NIEDERLANDE': 'NL', 'NETHERLANDS': 'NL',
            'BE': 'BE', 'BELGIEN': 'BE', 'BELGIUM': 'BE',
            'DK': 'DK', 'DÄNEMARK': 'DK', 'DENMARK': 'DK',
            'SE': 'SE', 'SCHWEDEN': 'SE', 'SWEDEN': 'SE',
            'NO': 'NO', 'NORWEGEN': 'NO', 'NORWAY': 'NO',
            'FI': 'FI', 'FINNLAND': 'FI', 'FINLAND': 'FI',
            'GB': 'GB', 'GROSSBRITANNIEN': 'GB', 'UNITED KINGDOM': 'GB',
            'IE': 'IE', 'IRLAND': 'IE', 'IRELAND': 'IE',
            'PT': 'PT', 'PORTUGAL': 'PT',
            'LU': 'LU', 'LUXEMBURG': 'LU', 'LUXEMBOURG': 'LU'
        }
        
        if country_str in country_variations:
            return country_variations[country_str]
        
        return ''
    
    return country_series.apply(clean_country)

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

def create_improved_geocoded_data(df, sample_size=300):
    """Create improved geocoded data with better coordinate distribution"""
    
    print(f"Creating improved geocoded data for {sample_size} customers...")
    
    # Sample customers with good address data
    sample_df = df.sample(n=min(sample_size, len(df)), random_state=42)
    
    # Create mock coordinates for demonstration
    # In a real scenario, you would use a geocoding service
    sample_data = []
    
    # Country coordinates (approximate centers)
    country_coords = {
        'DE': {'lat': 51.1657, 'lng': 10.4515, 'spread': 2.0},
        'AT': {'lat': 47.5162, 'lng': 14.5501, 'spread': 1.0},
        'IT': {'lat': 41.8719, 'lng': 12.5674, 'spread': 2.0},
        'FR': {'lat': 46.2276, 'lng': 2.2137, 'spread': 2.0},
        'ES': {'lat': 40.4637, 'lng': -3.7492, 'spread': 1.5},
        'PL': {'lat': 51.9194, 'lng': 19.1451, 'spread': 1.5},
        'CZ': {'lat': 49.8175, 'lng': 15.4730, 'spread': 0.8},
        'PT': {'lat': 39.3999, 'lng': -8.2245, 'spread': 1.0},
        'LU': {'lat': 49.8153, 'lng': 6.1296, 'spread': 0.3},
        'CH': {'lat': 46.8182, 'lng': 8.2275, 'spread': 1.0},
        'NL': {'lat': 52.1326, 'lng': 5.2913, 'spread': 1.0},
        'BE': {'lat': 50.8503, 'lng': 4.3517, 'spread': 0.5},
        'DK': {'lat': 56.2639, 'lng': 9.5018, 'spread': 0.8},
        'SE': {'lat': 60.1282, 'lng': 18.6435, 'spread': 1.5},
        'NO': {'lat': 60.4720, 'lng': 8.4689, 'spread': 1.5},
        'FI': {'lat': 61.9241, 'lng': 25.7482, 'spread': 1.5},
        'GB': {'lat': 55.3781, 'lng': -3.4360, 'spread': 1.5},
        'IE': {'lat': 53.4129, 'lng': -8.2439, 'spread': 1.0},
        'HR': {'lat': 45.1000, 'lng': 15.2000, 'spread': 0.8},
        'SI': {'lat': 46.1512, 'lng': 14.9955, 'spread': 0.5},
        'SK': {'lat': 48.6690, 'lng': 19.6990, 'spread': 0.8},
        'HU': {'lat': 47.1625, 'lng': 19.5033, 'spread': 0.8},
        'RO': {'lat': 45.9432, 'lng': 24.9668, 'spread': 1.0},
        'BG': {'lat': 42.7339, 'lng': 25.4858, 'spread': 0.8},
        'GR': {'lat': 39.0742, 'lng': 21.8243, 'spread': 1.0},
        'CY': {'lat': 35.1264, 'lng': 33.4299, 'spread': 0.3},
        'LT': {'lat': 55.1694, 'lng': 23.8813, 'spread': 0.5},
        'LI': {'lat': 47.1660, 'lng': 9.5554, 'spread': 0.2},
        'MC': {'lat': 43.7384, 'lng': 7.4246, 'spread': 0.1},
        'MA': {'lat': 31.7917, 'lng': -7.0926, 'spread': 1.0},
        'ZA': {'lat': -30.5595, 'lng': 22.9375, 'spread': 2.0},
        'US': {'lat': 39.8283, 'lng': -98.5795, 'spread': 3.0},
        'CN': {'lat': 35.8617, 'lng': 104.1954, 'spread': 3.0},
        'IN': {'lat': 20.5937, 'lng': 78.9629, 'spread': 2.0},
        'IS': {'lat': 64.9631, 'lng': -19.0208, 'spread': 1.0},
        'GE': {'lat': 42.3154, 'lng': 43.3569, 'spread': 0.5},
        'RE': {'lat': -21.1151, 'lng': 55.5364, 'spread': 0.3},
        'SG': {'lat': 1.3521, 'lng': 103.8198, 'spread': 0.2}
    }
    
    for idx, row in sample_df.iterrows():
        # Get base coordinates for the country
        country = row['country'] if row['country'] else 'DE'
        base_coords = country_coords.get(country, country_coords['DE'])
        
        # Add random variation based on country spread
        spread = base_coords['spread']
        lat_variation = np.random.uniform(-spread/2, spread/2)
        lng_variation = np.random.uniform(-spread/2, spread/2)
        
        # Handle NaN customer numbers
        customer_num = row['customer_number']
        if pd.isna(customer_num):
            customer_num = 0
        else:
            try:
                customer_num = int(customer_num)
            except (ValueError, TypeError):
                customer_num = 0
        
        sample_data.append({
            'id': row['id'],
            'customer_number': customer_num,
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
            'note': 'This is sample data with mock coordinates for demonstration purposes. For production use, replace with real geocoding.'
        },
        'customers': data
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(map_data, f, ensure_ascii=False, indent=2)
    
    print(f"Map data saved to {filename}")
    return map_data

def create_clean_csv_summary(df, filename='customer_summary_clean.csv'):
    """Create a clean summary CSV file"""
    
    # Filter out invalid country codes
    clean_df = df[df['country'] != ''].copy()
    
    summary = clean_df.groupby(['country', 'is_active']).size().unstack(fill_value=0)
    summary.columns = ['Inactive', 'Active']
    summary['Total'] = summary['Active'] + summary['Inactive']
    
    # Sort by total customers
    summary = summary.sort_values('Total', ascending=False)
    
    summary.to_csv(filename)
    print(f"Clean summary saved to {filename}")
    
    return summary

def main():
    """Main function to process all customer data with improved quality"""
    print("=== AboutWater Customer Data Processing (Improved) ===")
    print()
    
    # Clean and standardize the data
    df = clean_and_standardize_data()
    
    # Create improved geocoded data
    sample_data = create_improved_geocoded_data(df, sample_size=300)
    
    # Save data for the map
    map_data = save_data_for_map(sample_data)
    
    # Create clean summary
    summary = create_clean_csv_summary(df)
    
    print("\n=== Processing Complete ===")
    print(f"Total customers processed: {len(df)}")
    print(f"Sample data created: {len(sample_data)}")
    print(f"Active customers in sample: {map_data['metadata']['active_customers']}")
    print(f"Inactive customers in sample: {map_data['metadata']['inactive_customers']}")
    
    print("\nFiles created:")
    print("- customers_for_map.json (for the map)")
    print("- customer_summary_clean.csv (clean summary statistics)")
    
    print("\nNext steps:")
    print("1. Open the HTML map file to visualize customers")
    print("2. Use the JSON data for further analysis")
    print("3. For production use, replace mock coordinates with real geocoding")
    
    # Show top countries
    print(f"\nTop countries by customer count:")
    top_countries = summary.head(10)
    for country, row in top_countries.iterrows():
        print(f"  {country}: {row['Total']} customers ({row['Active']} active, {row['Inactive']} inactive)")

if __name__ == "__main__":
    main()
