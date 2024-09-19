import pandas as pd
import numpy as np
import openpyxl


# Replace 'file.json' with your JSON file path
df = pd.read_json("result.json")

# For distinct
unique = df["sqft_average"].unique()
print(unique)


# For Correlation
df = df.select_dtypes(include=[np.number])
cols = list(df.columns)
# print(cols)


correlation = df[cols].corr()
print(correlation)

correlation.to_excel("correlation.xlsx", index=False)
