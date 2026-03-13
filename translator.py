import pandas as pd
import requests
from io import StringIO

def update_feed():
    # Fetch the original CSV
    url = "https://albarautos.co.uk/aia-feed/6181bf0c-0565-483d-8d47-decff1d423cd.csv"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    df = pd.read_csv(StringIO(response.text))

    # Create the ultimate Meta dataframe using the exact AIA Template columns
    meta_df = pd.DataFrame()

    meta_df['vehicle_id'] = df['registration']
    meta_df['title'] = df['derivative']
    meta_df['description'] = df['derivative']
    meta_df['url'] = df['url']
    
    # --- EXACT TEMPLATE MATCHES ---
    # Image must be an array format
    meta_df['image[0].url'] = df['photos'].apply(lambda x: str(x).split('|')[0].replace('{resize}', 'w1024') if pd.notnull(x) else '')
    
    # Address must use .addr1
    meta_df['address.addr1'] = '177 Leicester Road'
    meta_df['address.city'] = 'Mountsorrel'
    meta_df['address.region'] = 'Leicestershire'
    meta_df['address.postal_code'] = 'LE12 7DB'
    meta_df['address.country'] = 'GB'
    
    # Mileage needs .unit and .value separated again, using 'MI' for miles
    meta_df['mileage.value'] = df['odometerReadingMiles']
    meta_df['mileage.unit'] = 'MI'
    # ------------------------------

    meta_df['make'] = df['make']
    meta_df['model'] = df['model']
    meta_df['year'] = df['yearOfManufacture']
    meta_df['price'] = df['suppliedPrice'].astype(str) + " GBP"
    
    # Template requires 'USED' in all caps
    meta_df['state_of_vehicle'] = 'USED'
    
    # Translators to match the template dictionary exactly
    transmission_map = {'Automatic': 'AUTOMATIC', 'Manual': 'MANUAL'}
    meta_df['transmission'] = df['transmissionType'].map(transmission_map).fillna(df['transmissionType'])
    
    fuel_map = {
        'Petrol': 'PETROL', 
        'Electric': 'ELECTRIC', 
        'Diesel': 'DIESEL', 
        'Petrol Hybrid': 'HYBRID', 
        'Petrol Plug-in Hybrid': 'PLUGIN_HYBRID'
    }
    meta_df['fuel_type'] = df['fuelType'].map(fuel_map).fillna(df['fuelType'])

    drivetrain_map = {
        'Front Wheel Drive': 'FWD', 
        'Four Wheel Drive': '4X4',
        'All Wheel Drive': 'AWD',
        'Rear Wheel Drive': 'RWD'
    }
    meta_df['drivetrain'] = df['drivetrain'].map(drivetrain_map).fillna(df['drivetrain'])

    meta_df['body_style'] = df['bodyType']
    meta_df['exterior_color'] = df['colour']

    # Save the file
    meta_df.to_csv('meta_feed.csv', index=False)
    print("Feed successfully translated to AIA template and saved as meta_feed.csv")

if __name__ == "__main__":
    update_feed()
