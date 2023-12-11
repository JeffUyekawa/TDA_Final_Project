#%%
import numpy as np
import pandas as pd
import kmapper as km
from geopy.geocoders import Nominatim

#%%
'''
This file reads in vaccination data and adds latitude and longitude.
In recent runs, the latitude/longitude addition has been throwing time out errors,
for that reason, It is suggested to use the dataframe that already has lat/long
which is included, and starting from line 32 after importing packages.

Next, we add GDP, median age, and life expectancy before dropping null values
and scaling each column for use with persistent homology calculation.
'''
polio_df = pd.read_csv(r"C:\Users\jeffu\Downloads\polio_data.csv")
polio_df = polio_df[['ParentLocation','Location','Value','Period']]

#Geolocator for looking up lat/long values by country name
geolocator = Nominatim(user_agent="my_geocoder")
# Function to get latitude and longitude for a given country
# Note, this section takes a LONG time to run
def get_lat_lon(country):
    location = geolocator.geocode(country)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

# Apply the function to the 'Country' column to create new 'Latitude' and 'Longitude' columns
polio_df[['Latitude', 'Longitude']] = polio_df['Location'].apply(lambda x: pd.Series(get_lat_lon(x)))
polio_df.dropna(inplace=True)
#%%
#Read in dataframe with Latitude and Longitude Included
polio_df = pd.read_csv(r"C:\Users\jeffu\Downloads\polio_data_latlong.csv")
polio_2022 = polio_df[polio_df.Year==2022]
#Read in csv for life expectency, gdp, median age
expectency = pd.read_csv(r"C:\Users\jeffu\OneDrive\Documents\Jeff's Math\TDA\Life_Expectency_Worldbank_org\Life_Expectency.csv")
gdp = pd.read_csv(r"C:\Users\jeffu\OneDrive\Documents\Jeff's Math\TDA\GDP_Worldbank_org\GDP.csv")
med_age = pd.read_csv(r"C:\Users\jeffu\OneDrive\Documents\Jeff's Math\TDA\Median_Age_CIA_gov.csv")
expectency.dropna(inplace=True)
gdp.dropna(inplace=True)
med_age.dropna(inplace=True)
#Merge to orininal 2022 dataframe
merged_polio = polio_2022.merge(expectency, left_on='Location', right_on='Country Name', how='left')
merged_polio = merged_polio.merge(gdp,left_on='Location', right_on='Country Name', how='left')
merged_polio = merged_polio.merge(med_age,left_on='Location', right_on='name', how='left')
merged_polio.dropna(inplace=True)
#Drop unneeded columns
merged_polio.drop(['Period','Country Name_x', 'Country Name_y','name' ],axis=1,inplace=True)

scaled_polio = merged_polio.copy()
#Perform min/max scaling column by column so large values don't dominate the rips filtration
#Scale all values between 0 and 1
num_cols = ['Value','Latitude','Longitude','LifeExpect','GDP','MedianAge']
for name in num_cols:
    col_vals = scaled_polio.loc[:,[name]]
    scaled_polio.loc[:,[name]] = (col_vals - col_vals.min())/(col_vals.max()-col_vals.min())
#Save to csv file
scaled_polio.to_csv(r"C:\Users\jeffu\Downloads\scaled_polio.csv",index=False) 
# %%
