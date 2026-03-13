import pandas as pd
import requests
from io import StringIO

def update_feed():
    # 1. Fetch the original CSV from your website
    url = "https://albarautos.co.uk/aia-feed/6181bf0c-0565-483d-8d47-decff1d423cd.csv"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    # Read the CSV into a pandas dataframe
    df = pd.read_csv(StringIO(response.text))

    # 2. Create a new dataframe specifically formatted for Meta
    meta_df = pd.DataFrame()

    # Map exactly to Meta's required column names
    meta_df['id'] = df['registration']
    meta_df['title'] = df['derivative']
    meta_df['description'] = df['derivative']
    meta_df['url'] = df['url']
    
    # Clean the images: Split by '|' and take only the first image link
    meta_df['image_url'] = df['photos'].apply(lambda x: str(x).split('|')[0] if pd.notnull(x) else '')
    
    meta_df['make'] = df['make']
    meta_df['model'] = df['model']
    meta_df['year'] = df['yearOfManufacture']
    
    # Clean the price: Meta prefers the currency code attached
    meta_df['price'] = df['suppliedPrice'].astype(str) + " GBP"
    
    # Clean condition: Meta requires lowercase 'used'
    meta_df['state_of_vehicle'] = df['ownershipCondition'].str.lower()
    
    # Mileage
    meta_df['mileage.value'] = df['odometerReadingMiles']
    meta_df['mileage.unit'] = 'mi'
    
    # Highly recommended extra fields
    meta_df['transmission'] = df['transmissionType']
    meta_df['body_style'] = df['bodyType']
    meta_df['fuel_type'] = df['fuelType']
    meta_df['exterior_color'] = df['colour']
    meta_df['drivetrain'] = df['drivetrain']

    # 3. Save the translated file
    meta_df.to_csv('meta_feed.csv', index=False)
    print("Feed successfully translated and saved as meta_feed.csv")

if __name__ == "__main__":
    update_feed()
