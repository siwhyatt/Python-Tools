import os
import re
from helpers import GetArgument

def rename_folders(directory, search_pattern, replace_pattern):
    for foldername in os.listdir(directory):
        folder_path = os.path.join(directory, foldername)
        if os.path.isdir(folder_path):
            new_name = re.sub(search_pattern, replace_pattern, foldername)
            if new_name != foldername:
                new_path = os.path.join(directory, new_name)
                os.rename(folder_path, new_path)
                print(f"Renamed: {foldername} -> {new_name}")

# Get folder name
folder_name = GetArgument("Choose folder: ", 1)
search_pattern = GetArgument("Enter search pattern (regex): ", 2)
replace_pattern = GetArgument("Enter replace pattern: ", 3)

# Replace this with the path to your directory
directory_path = f"../../{folder_name}"

rename_folders(directory_path, search_pattern, replace_pattern)
