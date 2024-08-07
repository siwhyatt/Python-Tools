# NOTE: Function to count the files in directory and subfolders

import os
import csv
import sys

def list_subfolders_with_file_counts(directory: str) -> None:
    """ This function takes a directory path and writes a CSV file with subfolders and their file counts.
    """
    try:
        # Normalize the directory path and check if it's absolute
        directory = os.path.normpath(directory)

        # Check if the directory exists
        if not os.path.exists(directory):
            print(f"The specified directory does not exist: {directory}")
            return

        # Check for write permissions in the directory
        if not os.access(directory, os.W_OK):
            print("You do not have write permissions for this directory.")
            return
        
        # Define the path for the output CSV file
        output_file = os.path.join(directory, 'subfolder_file_counts.csv')
        
        # Open the CSV file for writing
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['SKU', 'Subfolder', 'File Count'])  # Header row
            
            # Walk through the directory
            for root, dirs, files in os.walk(directory):
                for subfolder in dirs:
                    subfolder_path = os.path.join(root, subfolder)
                    subfolder = subfolder
                    sku = subfolder.split(" ")[0]
                    file_count = sum(len(files) for _, _, files in os.walk(subfolder_path))
                    writer.writerow([sku, subfolder, file_count])
                    
        print(f"CSV file has been created: {output_file}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    if len(sys.argv) > 1:
        # Use the absolute path directly if provided via command line
        directory = sys.argv[1]
        list_subfolders_with_file_counts(directory)
    else:
        # Interactive mode: ask the user to input the directory path
        while True:
            user_input_directory = input("Enter the directory path (or type 'exit' to quit): ")
            if user_input_directory.lower() == 'exit':
                break
            # Use the path as is if it's absolute, otherwise join it with the current working directory
            if not os.path.isabs(user_input_directory):
                user_input_directory = os.path.join(os.getcwd(), user_input_directory)
            list_subfolders_with_file_counts(user_input_directory)

if __name__ == "__main__":
    main()
