import os
import csv

def write_filenames_to_csv(root_directory, output_file):
    # Recursively write directory subfolder and file namess to a csv
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Folder', 'Filename'])  # Write header

        for foldername, subfolders, filenames in os.walk(root_directory):
            for filename in filenames:
                relative_path = os.path.relpath(foldername, root_directory)
                csv_writer.writerow([relative_path, filename])

    print(f"Filenames have been written to {output_file}")


def main():
    # Get folder name
    root_directory = os.getcwd()
    output_file = 'folder_names.csv'

    write_filenames_to_csv(root_directory, output_file)


if __name__ == '__main__':
    main()
