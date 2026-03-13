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
    
    # --- THE IMAGE URL FIX ---
    # This splits the pipe, grabs the first image, and replaces {resize} with a real dimension
    meta_df['image_url'] = df['photos'].apply(lambda x: str(x).split('|')[0].replace('{resize}', 'w1024') if pd.notnull(x) else '')
    # -------------------------
    
    # The Address Fix
    meta_df['address'] = '{"street_address": "177 Leicester Road", "city": "Mountsorrel", "region": "Leicestershire", "postal_code": "LE12 7DB", "country": "GB"}'
    meta_df['street_address'] = '177 Leicester Road'
    meta_df['city'] = 'Mountsorrel'
    meta_df['region'] = 'Leicestershire'
    meta_df['postal_code'] = 'LE12 7DB'
    meta_df['country'] = 'GB'

    meta_df['make'] = df['make']
    meta_df['model'] = df['model']
    meta_df['year'] = df['yearOfManufacture']
    meta_df['price'] = df['suppliedPrice'].astype(str) + " GBP"
    
    meta_df['state_of_vehicle'] = 'used'
    
    # The Mileage Fix
    meta_df['mileage'] = df['odometerReadingMiles'].astype(str) + ' mi'
    
    meta_df['transmission'] = df['transmissionType']
    meta_df['body_style'] = df['bodyType']
    meta_df['fuel_type'] = df['fuelType']
    meta_df['exterior_color'] = df['colour']
    meta_df['drivetrain'] = df['drivetrain']

    # Save the file
    meta_df.to_csv('meta_feed.csv', index=False)
    print("Feed successfully translated and saved as meta_feed.csv")

if __name__ == "__main__":
    update_feed()
