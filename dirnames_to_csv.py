import os
import csv

def list_folders_in_directory():
    """ This function writes a csv file with all the folder names in a directory
    """
    directory = os.getcwd()
    # Define the path for the output CSV file
    output_file = os.path.join(directory, 'folder_list.csv')
    
    # Open the CSV file for writing
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Foldername'])  # Header row
        
        # Walk through the user-provided directory
        for root, dirs, files in os.walk(directory):
            for folder in dirs:
                writer.writerow([ folder ])
                
        print(f"CSV file has been created: {output_file}")

def main():
    list_folders_in_directory()

if __name__ == "__main__":
    main()
