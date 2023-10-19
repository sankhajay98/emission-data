import pandas as pd
from tqdm import tqdm

# Define the file paths for your input Excel files
file1_path = 'input/2018-01.xlsx'
file2_path = 'input/2019-01.xlsx'

# Load both Excel files into pandas dataframes
df1 = pd.read_excel(file1_path)
df2 = pd.read_excel(file2_path)

# Merge dataframes based on the 'VehRegNo' column
merged_df = df1.merge(df2, on='VehRegNo')

# Create an empty list to store distance values
distances = []

# Create a tqdm progress bar
with tqdm(total=len(merged_df), desc="Processing") as pbar:
    for _, row in merged_df.iterrows():
        # Calculate the distance traveled
        distance = abs(row['VehCurrentMileage_x'] - row['VehCurrentMileage_y'])
        distances.append(distance)
        pbar.update(1)

# Add the 'DistanceTraveled' column to the merged dataframe
merged_df['DistanceTraveled'] = distances

# Create a new dataframe with just the 'VehRegNo' and 'DistanceTraveled' columns
result_df = merged_df[['VehRegNo', 'DistanceTraveled']]

# Save the result to a new Excel file
result_file = 'output/vehicle_distance.xlsx'
result_df.to_excel(result_file, index=False)

print(f"Results saved to {result_file}")

