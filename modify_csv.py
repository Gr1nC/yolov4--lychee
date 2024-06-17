import pandas as pd
import random

df = pd.read_csv('trees.csv')

for i, row in df.iterrows():
    # lat = random.uniform(113.406273, 113.413837)
    # lon = random.uniform(23.04718, 23.058386)
    lat = random.uniform(113, 114)
    lon = random.uniform(23.04, 23.05)
    df.loc[i, 'latitude'] = lat
    df.loc[i, 'longitude'] = lon

df.to_csv('new_data.csv', index=False)
