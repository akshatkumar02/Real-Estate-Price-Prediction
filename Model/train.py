import pandas as pd
import numpy as np
import json
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder

# ✅ Function to clean 'total_sqft'
def convert_sqft_to_number(x):
    try:
        tokens = str(x).split('-')
        if len(tokens) == 2:
            return (float(tokens[0]) + float(tokens[1])) / 2
        return float(x)
    except:
        return None

# Load and clean the dataset
df = pd.read_csv("bengaluru_house_prices.csv")
df = df.dropna()

# ✅ Convert and clean 'total_sqft'
df['total_sqft'] = df['total_sqft'].apply(convert_sqft_to_number)
df = df.dropna(subset=['total_sqft'])

# ✅ Extract 'bhk' from 'size' column
df['bhk'] = df['size'].apply(lambda x: int(x.split(' ')[0]))

# Prepare features
X = df[['total_sqft', 'bath', 'bhk', 'location']]
y = df['price']

# One-hot encode location
encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
loc_encoded = encoder.fit_transform(X[['location']])
loc_columns = [col.replace("location_", "") for col in encoder.get_feature_names_out(['location'])]  # ✅ Removed prefix

# Combine all features
X_final = np.concatenate([
    X[['total_sqft', 'bath', 'bhk']].values,
    loc_encoded
], axis=1)

# Train model
model = LinearRegression()
model.fit(X_final, y)

# Save model
with open("banglore_home_prices_model.pickle", "wb") as f:
    pickle.dump(model, f)

# ✅ Save columns without "location_" prefix
columns = ['total_sqft', 'bath', 'bhk'] + list(loc_columns)
with open("columns.json", "w") as f:
    json.dump({"data_columns": columns}, f)

print("✅ Model and columns saved successfully!")
