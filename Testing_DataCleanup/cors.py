import pandas as pd
import numpy as np

# Replace 'file.json' with your JSON file path
df = pd.read_json("result.json")
df = df.select_dtypes(include=[np.number])
cols = list(df.columns)
print(cols)

selected_cols: list = [
    "price",
    "age_range_min",
    "sqft_range_min",
    "Bedrooms",
    "Bathrooms",
    "Kitchens",
]

correlation = df[cols].corr()
print(correlation)


unique = df["Furnished"].unique()
print(unique)
