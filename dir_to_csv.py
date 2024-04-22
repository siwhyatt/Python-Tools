import os
import csv
import sys

def list_files_in_directory(directory):
    """ This function takes a directory path and writes a CSV file with filenames,
        their extension, and size in bytes in that directory.
    """
    try:
        # Normalize the directory path
        directory = os.path.normpath(directory)

        # Check if the directory exists
        if not os.path.exists(directory):
            print(f"The specified directory does not exist: {directory}")
            return

        # Check if the script has permission to write in the directory
        if not os.access(directory, os.W_OK):
            print("You do not have write permissions for this directory.")
            return
        
        # Define the path for the output CSV file
        output_file = os.path.join(directory, 'file_list.csv')
        
        # Open the CSV file for writing
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Folder', 'File Name', 'File Type', 'Size (bytes)'])  # Header row
            
            # Walk through the user-provided directory
            for root, dirs, files in os.walk(directory):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    folder = root.split(directory)[-1]
                    file_extension = os.path.splitext(filename)[1]
                    file_size = os.path.getsize(filepath)
                    writer.writerow([folder, filename, file_extension, file_size])
                    
        print(f"CSV file has been created: {output_file}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    if len(sys.argv) > 1:
        # Use the absolute path directly if provided via command line
        directory = sys.argv[1]
        list_files_in_directory(directory)
    else:
        # Interactive mode: ask the user to input the directory path
        while True:
            user_input_directory = input("Enter the directory path (or type 'exit' to quit): ")
            if user_input_directory.lower() == 'exit':
                break
            # Use the path as is if it's absolute, otherwise join it with the current working directory
            if not os.path.isabs(user_input_directory):
                user_input_directory = os.path.join(os.getcwd(), user_input_directory)
            list_files_in_directory(user_input_directory)

if __name__ == "__main__":
    main()
