import pandas as pd
import requests
from io import StringIO

def update_feed():
    # Fetch the original CSV
    url = "https://albarautos.co.uk/aia-feed/6181bf0c-0565-483d-8d47-decff1d423cd.csv"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    df = pd.read_csv(StringIO(response.text))

    # Create the ultimate Meta dataframe
    meta_df = pd.DataFrame()

    meta_df['vehicle_id'] = df['registration']
    meta_df['title'] = df['derivative']
    meta_df['description'] = df['derivative']
    meta_df['url'] = df['url']
    
    # Image Fix (Providing both names so Meta never asks you to map it again)
    clean_image = df['photos'].apply(lambda x: str(x).split('|')[0].replace('{resize}', 'w1024') if pd.notnull(x) else '')
    meta_df['image'] = clean_image
    meta_df['image_url'] = clean_image
    
    # The Address Fix (Using Meta's exact backend prefixes to bypass the UI mapper)
    meta_df['address.street_address'] = '177 Leicester Road'
    meta_df['address.city'] = 'Mountsorrel'
    meta_df['address.region'] = 'Leicestershire'
    meta_df['address.postal_code'] = 'LE12 7DB'
    meta_df['address.country'] = 'GB'

    meta_df['make'] = df['make']
    meta_df['model'] = df['model']
    meta_df['year'] = df['yearOfManufacture']
    meta_df['price'] = df['suppliedPrice'].astype(str) + " GBP"
    meta_df['state_of_vehicle'] = 'used'
    meta_df['mileage'] = df['odometerReadingMiles'].astype(str) + ' mi'
    
    # --- THE NEW DICTIONARY TRANSLATORS ---
    # Translate Transmissions
    transmission_map = {'Automatic': 'AUTO', 'Manual': 'MANUAL'}
    meta_df['transmission'] = df['transmissionType'].map(transmission_map).fillna(df['transmissionType'])
    
    # Translate Fuel Types
    fuel_map = {
        'Petrol': 'PETROL', 
        'Electric': 'ELECTRIC', 
        'Diesel': 'DIESEL', 
        'Petrol Hybrid': 'HYBRID', 
        'Petrol Plug-in Hybrid': 'PLUGIN_HYBRID'
    }
    meta_df['fuel_type'] = df['fuelType'].map(fuel_map).fillna(df['fuelType'])

    # Translate Drivetrains
    drivetrain_map = {
        'Front Wheel Drive': 'FWD', 
        'Four Wheel Drive': '4X4',
        'All Wheel Drive': 'AWD',
        'Rear Wheel Drive': 'RWD'
    }
    meta_df['drivetrain'] = df['drivetrain'].map(drivetrain_map).fillna(df['drivetrain'])
    # --------------------------------------

    meta_df['body_style'] = df['bodyType']
    meta_df['exterior_color'] = df['colour']

    # Save the file
    meta_df.to_csv('meta_feed.csv', index=False)
    print("Feed successfully translated and saved as meta_feed.csv")

if __name__ == "__main__":
    update_feed()
