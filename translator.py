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
    
    # --- NEW AD FIXES: Reg & Facebook Page ID ---
    meta_df['vehicle_registration_plate'] = df['registration']
    meta_df['fb_page_id'] = '467782659760947' 
    # --------------------------------------------
    
    # The Clean Title Fix
    clean_title = df['yearOfManufacture'].astype(str) + ' ' + df['make'] + ' ' + df['model'] + ' ' + df['trim'].fillna('')
    meta_df['title'] = clean_title.str.replace('  ', ' ').str.strip()
    meta_df['description'] = df['derivative']
    meta_df['url'] = df['url']
    
    # The Multiple Images Fix
    for i in range(10):
        meta_df[f'image[{i}].url'] = df['photos'].apply(
            lambda x: str(x).split('|')[i].replace('{resize}', 'w1024') if pd.notnull(x) and len(str(x).split('|')) > i else ''
        )
    
    meta_df['address.addr1'] = '177 Leicester Road'
    meta_df['address.city'] = 'Mountsorrel'
    meta_df['address.region'] = 'Leicestershire'
    meta_df['address.postal_code'] = 'LE12 7DB'
    meta_df['address.country'] = 'GB'

    meta_df['make'] = df['make']
    meta_df['model'] = df['model']
    meta_df['year'] = df['yearOfManufacture']
    meta_df['price'] = df['suppliedPrice'].astype(str) + " GBP"
    
    meta_df['state_of_vehicle'] = 'USED'
    
    meta_df['mileage.value'] = df['odometerReadingMiles']
    meta_df['mileage.unit'] = 'MI'
    
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
    meta_df.to_csv('facebook_inventory.csv', index=False)
    print("Feed successfully translated with Reg Plate and actual FB Page ID!")

if __name__ == "__main__":
    update_feed()
