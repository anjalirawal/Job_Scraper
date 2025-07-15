import pandas as pd
from geopy.distance import geodesic

def get_cities_within_radius(center_lat, center_lag, radius_miles=150, csv_path = "uszips.csv"):
    zips_df = pd.read_csv(csv_path)

    #calculate the distance from the center point
    def is_within_radius(row):
        city_coords = (row['lat'], row['lng'])
        return geodesic((center_lat, center_lag), city_coords).miles <= radius_miles


    #filter and return lowercased city names
    zip_df['within_radius'] = zip_df.apply(is_within_radius, axis=1)
    filtered = zip_df[zip_df['within_radius']]
    cities = sorted(set(filtered['city'].dropna().str.lower()))

    return cities


los_angeles_lat, los_angeles_lng = 34.0522, -118.2437
CALIFORNIA_CITIES = get_cities_within_radius(los_angeles_lat, los_angeles_lng)
CALIFORNIA_CITIES.append("remote")