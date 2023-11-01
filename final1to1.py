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

# Create lists to store additional columns
test_date_times = []
veh_fuel_types = []
veh_classes = []

# Counter for valid entries
valid_entries = 0

# Create a tqdm progress bar
with tqdm(total=len(merged_df), desc="Processing") as pbar:
    for _, row in merged_df.iterrows():
        test_result_x = row['TestResult_x']
        test_result_y = row['TestResult_y']
        
        if test_result_x not in ('F', 'A') and test_result_y not in ('F', 'A'):
            try:
                # Convert mileage values to numeric (float)
                mileage1 = float(row['VehCurrentMileage_x'])
                mileage2 = float(row['VehCurrentMileage_y'])
                # Calculate the distance traveled
                distance = abs(mileage1 - mileage2)
                distances.append(distance)
                test_date_times.append(row['TestDateTime_x'])
                veh_fuel_types.append(row['VehFuelType_x'])
                veh_classes.append(row['VehClass_x'])
                valid_entries += 1
            except ValueError:
                # Handle non-numeric values or conversion errors
                distances.append(None)  # You can choose how to handle these cases
                test_date_times.append(None)
                veh_fuel_types.append(None)
                veh_classes.append(None)
        pbar.update(1)

# Create a new dataframe for valid entries
valid_entries_df = merged_df.loc[~merged_df['TestResult_x'].isin(['F', 'A'])]
valid_entries_df = valid_entries_df.loc[~valid_entries_df['TestResult_y'].isin(['F', 'A'])]

# Add the 'DistanceTraveled' column to the valid entries DataFrame
valid_entries_df['DistanceTraveled'] = distances
valid_entries_df['TestDateTime'] = test_date_times
valid_entries_df['VehFuelType'] = veh_fuel_types
valid_entries_df['VehClass'] = veh_classes

# Reset the index of the valid entries DataFrame
valid_entries_df.reset_index(drop=True, inplace=True)

# Save the result to a new CSV file
result_file = 'output/vehicle_distance_with_info.csv'
valid_entries_df[['VehRegNo', 'DistanceTraveled', 'TestDateTime', 'VehFuelType', 'VehClass']].to_csv(result_file, index=False)

print(f"Results saved to {result_file}")
