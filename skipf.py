import pandas as pd
from tqdm import tqdm

# Define the file paths for your input CSV files
file1_path = 'input/2018-01.csv'
file2_path = 'input/2019-01.csv'

# Load both CSV files into pandas dataframes
df1 = pd.read_csv(file1_path)
df2 = pd.read_csv(file2_path)

# Merge dataframes based on the 'VehRegNo' column
merged_df = df1.merge(df2, on='VehRegNo')

# Create an empty list to store distance values
distances = []

# Counter for valid entries
valid_entries = 0

# Create a tqdm progress bar
with tqdm(total=len(merged_df), desc="Processing") as pbar:
    for _, row in merged_df.iterrows():
        if row['TestResult_x'] != 'F' and row['TestResult_y'] != 'F':
            try:
                # Convert mileage values to numeric (float)
                mileage1 = float(row['VehCurrentMileage_x'])
                mileage2 = float(row['VehCurrentMileage_y'])
                # Calculate the distance traveled
                distance = abs(mileage1 - mileage2)
                distances.append(distance)
                valid_entries += 1
            except ValueError:
                # Handle non-numeric values or conversion errors
                distances.append(None)  # You can choose how to handle these cases
        pbar.update(1)

# Create a new dataframe with just the 'VehRegNo' and 'DistanceTraveled' columns for valid entries
valid_entries_df = merged_df.loc[merged_df['TestResult_x'] != 'F']
valid_entries_df = valid_entries_df.loc[valid_entries_df['TestResult_y'] != 'F']
valid_entries_df['DistanceTraveled'] = distances

# Reset the index of the valid entries DataFrame
valid_entries_df.reset_index(drop=True, inplace=True)

# Save the result to a new CSV file
result_file = 'output/vehicle_distance.csv'
valid_entries_df[['VehRegNo', 'DistanceTraveled']].to_csv(result_file, index=False)

print(f"Results saved to {result_file}")
