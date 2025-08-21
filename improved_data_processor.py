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

def create_improved_geocoded_data(df, sample_size=None):
    """Create improved geocoded data with better coordinate distribution"""
    
    if sample_size is None:
        sample_size = len(df)
    
    print(f"Creating improved geocoded data for {sample_size} customers (including all German cities)...")
    
    # Use all customers or sample if specified
    if sample_size >= len(df):
        sample_df = df
    else:
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
    
    # Major German cities with specific coordinates for better representation
    german_cities = {
        'München': {'lat': 48.1351, 'lng': 11.5820, 'spread': 0.3},
        'Munich': {'lat': 48.1351, 'lng': 11.5820, 'spread': 0.3},
        'Berlin': {'lat': 52.5200, 'lng': 13.4050, 'spread': 0.3},
        'Hamburg': {'lat': 53.5511, 'lng': 9.9937, 'spread': 0.3},
        'Köln': {'lat': 50.9375, 'lng': 6.9603, 'spread': 0.3},
        'Cologne': {'lat': 50.9375, 'lng': 6.9603, 'spread': 0.3},
        'Frankfurt': {'lat': 50.1109, 'lng': 8.6821, 'spread': 0.3},
        'Stuttgart': {'lat': 48.7758, 'lng': 9.1829, 'spread': 0.3},
        'Düsseldorf': {'lat': 51.2277, 'lng': 6.7735, 'spread': 0.3},
        'Dortmund': {'lat': 51.5136, 'lng': 7.4653, 'spread': 0.3},
        'Essen': {'lat': 51.4556, 'lng': 7.0116, 'spread': 0.3},
        'Leipzig': {'lat': 51.3397, 'lng': 12.3731, 'spread': 0.3},
        'Bremen': {'lat': 53.0793, 'lng': 8.8017, 'spread': 0.3},
        'Dresden': {'lat': 51.0504, 'lng': 13.7373, 'spread': 0.3},
        'Hannover': {'lat': 52.3759, 'lng': 9.7320, 'spread': 0.3},
        'Nürnberg': {'lat': 49.4521, 'lng': 11.0767, 'spread': 0.3},
        'Nuremberg': {'lat': 49.4521, 'lng': 11.0767, 'spread': 0.3},
        'Duisburg': {'lat': 51.4344, 'lng': 6.7623, 'spread': 0.3},
        'Bochum': {'lat': 51.4818, 'lng': 7.2162, 'spread': 0.3},
        'Wuppertal': {'lat': 51.2562, 'lng': 7.1508, 'spread': 0.3},
        'Bielefeld': {'lat': 52.0302, 'lng': 8.5325, 'spread': 0.3},
        'Bonn': {'lat': 50.7374, 'lng': 7.0982, 'spread': 0.3},
        'Mannheim': {'lat': 49.4875, 'lng': 8.4660, 'spread': 0.3},
        'Karlsruhe': {'lat': 49.0069, 'lng': 8.4037, 'spread': 0.3},
        'Wiesbaden': {'lat': 50.0782, 'lng': 8.2397, 'spread': 0.3},
        'Münster': {'lat': 51.9607, 'lng': 7.6261, 'spread': 0.3},
        'Gelsenkirchen': {'lat': 51.5177, 'lng': 7.0857, 'spread': 0.3},
        'Aachen': {'lat': 50.7753, 'lng': 6.0839, 'spread': 0.3},
        'Braunschweig': {'lat': 52.2689, 'lng': 10.5267, 'spread': 0.3},
        'Chemnitz': {'lat': 50.8278, 'lng': 12.9249, 'spread': 0.3},
        'Kiel': {'lat': 54.3233, 'lng': 10.1228, 'spread': 0.3},
        'Halle': {'lat': 51.4964, 'lng': 11.9688, 'spread': 0.3},
        'Magdeburg': {'lat': 52.1205, 'lng': 11.6276, 'spread': 0.3},
        'Freiburg': {'lat': 47.9990, 'lng': 7.8421, 'spread': 0.3},
        'Krefeld': {'lat': 51.3392, 'lng': 6.5861, 'spread': 0.3},
        'Lübeck': {'lat': 53.8654, 'lng': 10.6866, 'spread': 0.3},
        'Oberhausen': {'lat': 51.4706, 'lng': 6.8514, 'spread': 0.3},
        'Erfurt': {'lat': 50.9848, 'lng': 11.0299, 'spread': 0.3},
        'Mainz': {'lat': 49.9929, 'lng': 8.2473, 'spread': 0.3},
        'Rostock': {'lat': 54.0924, 'lng': 12.0991, 'spread': 0.3},
        'Kassel': {'lat': 51.3127, 'lng': 9.4797, 'spread': 0.3},
        'Potsdam': {'lat': 52.3906, 'lng': 13.0645, 'spread': 0.3},
        'Hagen': {'lat': 51.3671, 'lng': 7.4634, 'spread': 0.3},
        'Saarbrücken': {'lat': 49.2374, 'lng': 6.9816, 'spread': 0.3},
        'Mülheim': {'lat': 51.4275, 'lng': 6.8827, 'spread': 0.3},
        'Ludwigshafen': {'lat': 49.4744, 'lng': 8.4402, 'spread': 0.3},
        'Leverkusen': {'lat': 51.0459, 'lng': 6.9853, 'spread': 0.3},
        'Oldenburg': {'lat': 53.1434, 'lng': 8.2146, 'spread': 0.3},
        'Osnabrück': {'lat': 52.2799, 'lng': 8.0472, 'spread': 0.3},
        'Solingen': {'lat': 51.1734, 'lng': 7.0845, 'spread': 0.3},
        'Heidelberg': {'lat': 49.3988, 'lng': 8.6724, 'spread': 0.3},
        'Herne': {'lat': 51.5416, 'lng': 7.2208, 'spread': 0.3},
        'Neuss': {'lat': 51.2042, 'lng': 6.6879, 'spread': 0.3},
        'Darmstadt': {'lat': 49.8728, 'lng': 8.6512, 'spread': 0.3},
        'Paderborn': {'lat': 51.7187, 'lng': 8.7575, 'spread': 0.3},
        'Regensburg': {'lat': 49.0134, 'lng': 12.1016, 'spread': 0.3},
        'Ingolstadt': {'lat': 48.7665, 'lng': 11.4241, 'spread': 0.3},
        'Würzburg': {'lat': 49.7913, 'lng': 9.9534, 'spread': 0.3},
        'Fürth': {'lat': 49.4778, 'lng': 10.9887, 'spread': 0.3},
        'Wolfsburg': {'lat': 52.4227, 'lng': 10.7865, 'spread': 0.3},
        'Offenbach': {'lat': 50.1006, 'lng': 8.7665, 'spread': 0.3},
        'Ulm': {'lat': 48.3984, 'lng': 9.9916, 'spread': 0.3},
        'Heilbronn': {'lat': 49.1427, 'lng': 9.2185, 'spread': 0.3},
        'Pforzheim': {'lat': 48.8926, 'lng': 8.6949, 'spread': 0.3},
        'Göttingen': {'lat': 51.5413, 'lng': 9.9158, 'spread': 0.3},
        'Bottrop': {'lat': 51.5235, 'lng': 6.9225, 'spread': 0.3},
        'Trier': {'lat': 49.7499, 'lng': 6.6373, 'spread': 0.3},
        'Recklinghausen': {'lat': 51.6138, 'lng': 7.1977, 'spread': 0.3},
        'Reutlingen': {'lat': 48.4914, 'lng': 9.2045, 'spread': 0.3},
        'Bremerhaven': {'lat': 53.5396, 'lng': 8.5809, 'spread': 0.3},
        'Koblenz': {'lat': 50.3569, 'lng': 7.5940, 'spread': 0.3},
        'Bergisch Gladbach': {'lat': 50.9856, 'lng': 7.1329, 'spread': 0.3},
        'Jena': {'lat': 50.9279, 'lng': 11.5892, 'spread': 0.3},
        'Remscheid': {'lat': 51.1784, 'lng': 7.1894, 'spread': 0.3},
        'Erlangen': {'lat': 49.5897, 'lng': 11.0041, 'spread': 0.3},
        'Moers': {'lat': 51.4514, 'lng': 6.6264, 'spread': 0.3},
        'Siegen': {'lat': 50.8745, 'lng': 8.0243, 'spread': 0.3},
        'Hildesheim': {'lat': 52.1508, 'lng': 9.9513, 'spread': 0.3},
        'Salzgitter': {'lat': 52.1508, 'lng': 10.3333, 'spread': 0.3},
        'Cottbus': {'lat': 51.7216, 'lng': 14.3344, 'spread': 0.3},
        'Gera': {'lat': 50.8803, 'lng': 12.0826, 'spread': 0.3},
        'Kaiserslautern': {'lat': 49.4431, 'lng': 7.7689, 'spread': 0.3},
        'Schwerin': {'lat': 53.6355, 'lng': 11.4012, 'spread': 0.3},
        'Gütersloh': {'lat': 51.9069, 'lng': 8.3785, 'spread': 0.3},
        'Witten': {'lat': 51.4436, 'lng': 7.3305, 'spread': 0.3},
        'Iserlohn': {'lat': 51.3754, 'lng': 7.7020, 'spread': 0.3},
        'Ludwigsburg': {'lat': 48.8974, 'lng': 9.1916, 'spread': 0.3},
        'Hanau': {'lat': 50.1348, 'lng': 8.9144, 'spread': 0.3},
        'Esslingen': {'lat': 48.7424, 'lng': 9.3048, 'spread': 0.3},
        'Zwickau': {'lat': 50.7186, 'lng': 12.4942, 'spread': 0.3},
        'Düren': {'lat': 50.8008, 'lng': 6.4830, 'spread': 0.3},
        'Ratingen': {'lat': 51.2972, 'lng': 6.8497, 'spread': 0.3},
        'Tübingen': {'lat': 48.5206, 'lng': 9.0556, 'spread': 0.3},
        'Villingen-Schwenningen': {'lat': 48.0582, 'lng': 8.4616, 'spread': 0.3},
        'Königs Wusterhausen': {'lat': 52.3014, 'lng': 13.6330, 'spread': 0.3},
        'Lünen': {'lat': 51.6164, 'lng': 7.5282, 'spread': 0.3},
        'Marl': {'lat': 51.6567, 'lng': 7.0904, 'spread': 0.3},
        'Velbert': {'lat': 51.3373, 'lng': 7.0419, 'spread': 0.3},
        'Minden': {'lat': 52.2895, 'lng': 8.9145, 'spread': 0.3},
        'Dessau-Roßlau': {'lat': 51.8364, 'lng': 12.2469, 'spread': 0.3},
        'Viersen': {'lat': 51.2543, 'lng': 6.3944, 'spread': 0.3},
        'Rheine': {'lat': 52.2799, 'lng': 7.4407, 'spread': 0.3},
        'Lüdenscheid': {'lat': 51.2254, 'lng': 7.6273, 'spread': 0.3},
        'Castrop-Rauxel': {'lat': 51.5561, 'lng': 7.3116, 'spread': 0.3},
        'Gladbeck': {'lat': 51.5708, 'lng': 6.9854, 'spread': 0.3},
        'Bocholt': {'lat': 51.8388, 'lng': 6.6153, 'spread': 0.3},
        'Bamberg': {'lat': 49.8988, 'lng': 10.9027, 'spread': 0.3},
        'Detmold': {'lat': 51.9334, 'lng': 8.8733, 'spread': 0.3},
        'Arnsberg': {'lat': 51.3963, 'lng': 8.0641, 'spread': 0.3},
        'Lüneburg': {'lat': 53.2504, 'lng': 10.4145, 'spread': 0.3},
        'Bayreuth': {'lat': 49.9483, 'lng': 11.5783, 'spread': 0.3},
        'Celle': {'lat': 52.6226, 'lng': 10.0805, 'spread': 0.3},
        'Landshut': {'lat': 48.5378, 'lng': 12.1518, 'spread': 0.3},
        'Aschaffenburg': {'lat': 49.9770, 'lng': 9.1521, 'spread': 0.3},
        'Dinslaken': {'lat': 51.5667, 'lng': 6.7333, 'spread': 0.3},
        'Aalen': {'lat': 48.8378, 'lng': 10.0933, 'spread': 0.3},
        'Fulda': {'lat': 50.5598, 'lng': 9.6710, 'spread': 0.3},
        'Lippstadt': {'lat': 51.6733, 'lng': 8.3447, 'spread': 0.3},
        'Weimar': {'lat': 50.9795, 'lng': 11.3235, 'spread': 0.3},
        'Dormagen': {'lat': 51.0963, 'lng': 6.8319, 'spread': 0.3},
        'Neumünster': {'lat': 54.0744, 'lng': 9.9819, 'spread': 0.3},
        'Sindelfingen': {'lat': 48.7136, 'lng': 8.9967, 'spread': 0.3},
        'Rosenheim': {'lat': 47.8564, 'lng': 12.1291, 'spread': 0.3},
        'Herten': {'lat': 51.6000, 'lng': 7.1333, 'spread': 0.3},
        'Bergheim': {'lat': 50.9550, 'lng': 6.6390, 'spread': 0.3},
        'Schwäbisch Gmünd': {'lat': 48.8014, 'lng': 9.7974, 'spread': 0.3},
        'Friedrichshafen': {'lat': 47.6582, 'lng': 9.4758, 'spread': 0.3},
        'Wesel': {'lat': 51.6583, 'lng': 6.6172, 'spread': 0.3},
        'Kempten': {'lat': 47.7278, 'lng': 10.3137, 'spread': 0.3},
        'Görlitz': {'lat': 51.1552, 'lng': 14.9885, 'spread': 0.3},
        'Frankfurt (Oder)': {'lat': 52.3412, 'lng': 14.5500, 'spread': 0.3},
        'Frankfurt Oder': {'lat': 52.3412, 'lng': 14.5500, 'spread': 0.3},
        'Lübeck': {'lat': 53.8654, 'lng': 10.6866, 'spread': 0.3},
        'Mönchengladbach': {'lat': 51.1805, 'lng': 6.4428, 'spread': 0.3},
        'Moenchengladbach': {'lat': 51.1805, 'lng': 6.4428, 'spread': 0.3}
    }
    
    for idx, row in sample_df.iterrows():
        # Get base coordinates for the country and city
        country = row['country'] if row['country'] else 'DE'
        city = str(row['city']).strip() if pd.notna(row['city']) else ''
        
        # Check if we have specific coordinates for this city
        if city in german_cities:
            base_coords = german_cities[city]
            # Add small randomness around the exact city coordinates
            spread = base_coords['spread']
            lat_variation = np.random.uniform(-spread/2, spread/2)
            lng_variation = np.random.uniform(-spread/2, spread/2)
        else:
            # Use country coordinates
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
            'note': 'This data includes ALL customers with mock coordinates for demonstration purposes. German cities have accurate coordinates. For production use, replace with real geocoding.'
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
    
    # Create improved geocoded data for ALL customers
    sample_data = create_improved_geocoded_data(df, sample_size=len(df))
    
    # Save data for the map
    map_data = save_data_for_map(sample_data)
    
    # Create clean summary
    summary = create_clean_csv_summary(df)
    
    print("\n=== Processing Complete ===")
    print(f"Total customers processed: {len(df)}")
    print(f"All customers processed: {len(sample_data)}")
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
