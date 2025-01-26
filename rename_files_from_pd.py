# Rename files based on folder name

import os

def rename_files_in_subfolders(root_dir):
    """
    Renames files within subfolders, preserving their original order.

    Args:
        root_dir: The root directory to start the search from.
    """
    for foldername, subfolders, filenames in os.walk(root_dir):
        for index, filename in enumerate(filenames): 
            old_path = os.path.join(foldername, filename)
            new_filename = f"{os.path.basename(foldername)}_{index+1}{os.path.splitext(filename)[1]}"  # Start index at 1
            new_path = os.path.join(foldername, new_filename)
            os.rename(old_path, new_path)
            print(f"Renamed: {old_path} to {new_path}")

parent_directory = os.getcwd()
rename_files_in_subfolders(parent_directory)
