# Extract all unique entries from a specific csv column by header name
import csv
import os
from helpers import GetArgument


cwd = os.getcwd()

def extract_column_data(filename, column_header):
    unique_data = set()
    file_path = cwd + "/" + filename
    
    with open(file_path) as csvfile:
        raw_data = csv.DictReader(csvfile, delimiter=',')
        
        # Check if the column header exists
        if column_header not in raw_data.fieldnames:
            print(f"Error: Column '{column_header}' not found in CSV file.")
            print(f"Available columns: {raw_data.fieldnames}")
            return None
        
        for row in raw_data:
            value = row[column_header]
            if value:  # Only add non-empty values
                unique_data.add(value.strip())  # Strip whitespace

    return unique_data


def set_to_csv(python_set, output_filename):
    if python_set is None:
        return
        
    file_path = cwd + "/" + output_filename
    with open(file_path, 'w', newline='') as csvfile:
        output = csv.writer(csvfile)
        # Write header for output file
        output.writerow(['unique_values'])
        for item in python_set:
            output.writerow([item])

def main():
    filename = GetArgument("Enter filename in current directory\n", 1)
    column_header = GetArgument("Enter column header name\n", 2)
    
    unique_data = extract_column_data(filename, column_header)

    output_filename = f"{column_header}.csv"
    
    if unique_data:
        set_to_csv(unique_data, output_filename)
        print(f"Extracted {len(unique_data)} unique values from column '{column_header}'")
        print(f"Output saved to {output_filename}")
    else:
        print("No data extracted.")



if __name__ == '__main__':
    main()
