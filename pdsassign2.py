# -*- coding: utf-8 -*-
"""pdsassign2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qsdNGS4vu2d5BUXg9u7z3A_aZlsnFLvX
"""

import pandas as pd

# Load dataset
df = pd.read_csv('/content/train.csv')
df.head()

"""## a) **handle missing values**"""

# Step 1: Find columns with missing values
missing = df.isnull().sum()
missing = missing[missing > 0]  # Only show columns with missing values

# Step 2: Impute or drop based on missing percentage and type
for col in missing.index:
    missing_ratio = missing[col] / len(df)

    if missing_ratio > 0.85:
        df.drop(columns=[col], inplace=True)
    else:
        if df[col].dtype == 'object':
            mode_val = df[col].mode()[0]
            df[col] = df[col].fillna(mode_val)
        else:
            skewness = df[col].skew()
            if abs(skewness) > 1:
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
            else:
                mean_val = df[col].mean()
                df[col] = df[col].fillna(mean_val)

# Step 3: Display the cleaned dataset in proper tabular format (first 5 rows)
print(" Cleaned Dataset Preview (First 5 Rows):\n")
print(df.head().to_string(index=False))

"""**justification :**
Using an approach based on data type and missing %, missing values were addressed in order to clean the dataset.  To preserve data integrity, columns that had more than 85% missing data were removed.  To preserve the most prevalent category, missing values for categorical columns like Owner_Type were filled in using the mode.  The distribution of numerical columns, such as Seats, Power, and Mileage, was taken into consideration.  To reduce the impact of outliers, the median was employed when the column was heavily skewed; for normally distributed data, the mean was utilized.  For readability and practicality, the original structure was maintained, including units like "kmpl," "CC," and "bhp."  This methodology guaranteed a comprehensive, dependable, and comprehensible dataset for additional examination.

#**b)remove units from attributes**
"""

#Remove units and convert to float
df['Mileage'] = df['Mileage'].astype(str).str.extract('([\d.]+)').astype(float)
df['Engine'] = df['Engine'].astype(str).str.extract('([\d.]+)').astype(float)
df['Power'] = df['Power'].astype(str).str.extract('([\d.]+)').astype(float)

# Handle 'New_Price' only if it exists (and wasn't dropped)
if 'New_Price' in df.columns:
    df['New_Price'] = df['New_Price'].astype(str).str.replace(' Lakh', '', regex=False)
    df['New_Price'] = pd.to_numeric(df['New_Price'], errors='coerce')

#Display cleaned output (first 5 rows)
print("\n Final Cleaned Dataset (First 5 Rows):\n")
print(df.head().to_string(index=False, float_format='{:,.2f}'.format))

"""#**c)one hot encode categorical variables**"""

# Step 1: One-hot encode if needed
columns_to_encode = [col for col in ['Fuel_Type', 'Transmission'] if col in df.columns]

if columns_to_encode:
    df = pd.get_dummies(df, columns=columns_to_encode, drop_first=True)
    print("One-hot encoding applied for:", columns_to_encode)
else:
    print("Columns already encoded or do not exist:", ['Fuel_Type', 'Transmission'])

# Step 2: Get encoded column names
encoded_cols = [col for col in df.columns if 'Fuel_Type_' in col or 'Transmission_' in col]

# Step 3: Format and display output like your sample
print("\nOne-Hot Encoded Output in Table Format:\n")
print(df[encoded_cols].head(5).astype(int).to_string(index=False))

"""#**d)newfeature car-age**"""

from datetime import datetime

# Create 'Car_Age' by subtracting the manufacturing year from the current year
current_year = datetime.now().year
df['Car_Age'] = current_year - df['Year']

# Display: Confirm new column and show sample values
print(" rows with 'Year' and calculated 'Car_Age':")
print(df[['Year', 'Car_Age']].head())

"""#**e)data operations**"""

# 1. Select & copy subset of columns
selected_df = df[['Location', 'Year', 'Kilometers_Driven', 'Mileage', 'Engine',
                  'Power', 'Seats', 'Car_Age', 'Price']].copy()

# 2. Filter cars: High mileage (>20) and low price (<5)
filtered_df = selected_df[(selected_df['Mileage'] > 20) & (selected_df['Price'] < 5)]

# 3. Rename column safely
selected_df.rename(columns={'Kilometers_Driven': 'KMs_Driven'}, inplace=True)

# 4. Arrange by descending price
arranged_df = selected_df.sort_values(by='Price', ascending=False)

# 5. Summarize: Mean Price and Mileage by Location
summary_df = selected_df.groupby('Location').agg({
    'Price': 'mean',
    'Mileage': 'mean'
}).reset_index()

# === Display or export results ===

print("Filtered Data:")
print(filtered_df.head())

print("\nTop 5 Expensive Cars:")
print(arranged_df.head())

print("\nSummary by Location:")
print(summary_df.head())