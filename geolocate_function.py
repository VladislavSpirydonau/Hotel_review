#Function for filling mising values in lat and lng columns with use of google maps API
from geopy.geocoders import GoogleV3
import config
import pandas as pd

geolocator = GoogleV3(api_key=config.google_api_key)

def coordinate_fill(df):
    hotel_missing_list = []
    for i, row in df.iterrows():
        if pd.isna(row['lat']) or pd.isna(row['lng']):
            location = geolocator.geocode(row['Hotel_Address'])
            if location is not None:
                df.loc[i, 'lat'] = location.latitude
                df.loc[i, 'lng'] = location.longitude
            else:
                hotel_missing_list.append(row.Hotel_Name)
    return df, hotel_missing_list

