import pandas as pd

# 1. Load the raw dataset
# Ensure 'online_retail (1).csv' is uploaded to your Colab files section
try:
    df = pd.read_csv('online_retail (1).csv')
    print("File loaded successfully.")
except FileNotFoundError:
    print("Error: 'online_retail (1).csv' not found. Please upload it to the Colab files sidebar.")

# 2. Data Cleaning
# Convert InvoiceDate to datetime objects
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Remove duplicate rows
df.drop_duplicates(inplace=True)

# Remove rows where CustomerID is missing
df_clean = df.dropna(subset=['CustomerID'])

# Filter for successful sales only (Quantity and Price must be positive)
df_clean = df_clean[(df_clean['Quantity'] > 0) & (df_clean['UnitPrice'] > 0)]

# 3. Feature Engineering
# Calculate Total Price for each transaction
df_clean['TotalPrice'] = df_clean['Quantity'] * df_clean['UnitPrice']

# 4. Save the processed data
# This creates the file that your Streamlit app (app.py) will use
df_clean.to_csv('cleaned_online_retail.csv', index=False)

print("Cleaning complete! 'cleaned_online_retail.csv' has been created.")
