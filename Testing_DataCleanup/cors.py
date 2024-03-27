import pandas as pd

# Replace 'file.json' with your JSON file path
df = pd.read_json("result.json")
cols = df.columns
print(cols)

selected_cols: list = [
    "price",
    "age_range_min",
    "sqft_range_min",
    "Bedrooms",
    "Bathrooms",
    "Kitchens",
]

correlation = df[selected_cols].corr()
print(correlation)


unique = df["Pets"].unique()
print(unique)
