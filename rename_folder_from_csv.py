# Rename folders from csv file. 
import os
import csv

# Define the path to the directory and the CSV file
folder_path = os.getcwd() 
csv_file_path = 'folder_names.csv'

# Function to read the CSV and return a dictionary of old-new name pairs
def read_csv(file_path):
    name_mapping = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            old_name, new_name = row
            name_mapping[old_name] = f"{old_name} - {new_name}"
    return name_mapping

# Rename folders based on the CSV mapping
def rename_folders(folder_path, name_mapping):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):  # Check if the item is a directory
            if item in name_mapping:
                old_folder_path = os.path.join(folder_path, item)
                new_folder_path = os.path.join(folder_path, name_mapping[item])
                # Check if a folder with the new name already exists
                if not os.path.exists(new_folder_path):
                    os.rename(old_folder_path, new_folder_path)
                    print(f'Renamed folder "{item}" to "{name_mapping[item]}"')
                else:
                    print(f'Cannot rename folder "{item}" to "{name_mapping[item]}" because the target folder already exists.')

# Read the CSV file to get the mapping
name_mapping = read_csv(csv_file_path)

# Rename the folders in the directory based on the CSV
rename_folders(folder_path, name_mapping)
