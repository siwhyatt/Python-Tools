import os
import csv
from helpers import GetArgument

def write_filenames_to_csv(root_directory, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Folder', 'Filename'])  # Write header

        for foldername, subfolders, filenames in os.walk(root_directory):
            for filename in filenames:
                relative_path = os.path.relpath(foldername, root_directory)
                csv_writer.writerow([relative_path, filename])

    print(f"Filenames have been written to {output_file}")

# Get folder name
folder_name = GetArgument("Choose folder: ", 1)
root_directory = f"../../{folder_name}"
output_file = GetArgument("Output filename", 2)

write_filenames_to_csv(root_directory, output_file)
