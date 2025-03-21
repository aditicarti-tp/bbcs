import pandas as pd

# Load the dataset
file_path = "deforestation_data.csv"
df = pd.read_csv(file_path)

# Step 1: Rename columns for better readability
df.rename(columns={
    "iso3c": "Country_Code",
    "forests_2000": "Forest_Area_2000",
    "forests_2020": "Forest_Area_2020",
    "trend": "Forest_Change_Percentage"
}, inplace=True)

# Step 2: Handle missing values
# Since only 10 rows have missing 'trend' values, we will drop them
df.dropna(subset=["Forest_Change_Percentage"], inplace=True)

# Step 3: Remove duplicate rows (just in case)
df.drop_duplicates(inplace=True)

# Step 4: Convert country codes to uppercase (if needed)
df["Country_Code"] = df["Country_Code"].str.upper()

# Step 5: Save the cleaned dataset
cleaned_file_path = "cleaned_deforestation_data.csv"
df.to_csv(cleaned_file_path, index=False)

print("✅ Cleaning complete! Cleaned dataset saved as:", cleaned_file_path)

# Step 6: Preview cleaned dataset
print("\nCleaned Dataset Overview:")
print(df.info())
print("\nFirst 5 Rows:")
print(df.head())
