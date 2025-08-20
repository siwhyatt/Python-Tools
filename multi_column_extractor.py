# Extract all unique entries from multiple csv columns by header names
import csv
import os
from helpers import GetArgument


cwd = os.getcwd()

def extract_columns_data(filename, column_headers):
    """Extract unique data from multiple columns"""
    columns_data = {}
    file_path = cwd + "/" + filename
    
    with open(file_path) as csvfile:
        raw_data = csv.DictReader(csvfile, delimiter=',')
        
        # Check if all column headers exist
        missing_columns = [col for col in column_headers if col not in raw_data.fieldnames]
        if missing_columns:
            print(f"Error: Column(s) {missing_columns} not found in CSV file.")
            print(f"Available columns: {raw_data.fieldnames}")
            return None
        
        # Initialize sets for each column
        for header in column_headers:
            columns_data[header] = set()
        
        # Extract data for each column
        for row in raw_data:
            for header in column_headers:
                value = row[header]
                if value:  # Only add non-empty values
                    columns_data[header].add(value.strip())  # Strip whitespace

    return columns_data


def columns_to_csv(columns_data, output_filename):
    """Save multiple columns of unique data to a single CSV file"""
    if columns_data is None:
        return
        
    file_path = cwd + "/" + output_filename
    
    # Find the maximum number of unique values across all columns
    max_length = max(len(data) for data in columns_data.values()) if columns_data else 0
    
    with open(file_path, 'w', newline='') as csvfile:
        output = csv.writer(csvfile)
        
        # Write headers
        headers = list(columns_data.keys())
        output.writerow(headers)
        
        # Convert sets to sorted lists for consistent output
        columns_lists = {header: sorted(list(data)) for header, data in columns_data.items()}
        
        # Write data rows
        for i in range(max_length):
            row = []
            for header in headers:
                if i < len(columns_lists[header]):
                    row.append(columns_lists[header][i])
                else:
                    row.append('')  # Empty cell if this column has fewer values
            output.writerow(row)


def columns_to_separate_csvs(columns_data):
    """Save each column's unique data to separate CSV files"""
    if columns_data is None:
        return
        
    for header, unique_data in columns_data.items():
        output_filename = f"{header}_unique.csv"
        file_path = cwd + "/" + output_filename
        
        with open(file_path, 'w', newline='') as csvfile:
            output = csv.writer(csvfile)
            output.writerow(['unique_values'])
            for item in sorted(unique_data):
                output.writerow([item])
        
        print(f"Saved {len(unique_data)} unique values from '{header}' to {output_filename}")


def parse_column_headers(headers_input):
    """Parse column headers from various input formats"""
    # Remove any surrounding quotes and whitespace
    headers_input = headers_input.strip().strip('"').strip("'")
    
    # Try different delimiters
    for delimiter in [',', ';', '|', '\t']:
        if delimiter in headers_input:
            headers = [h.strip().strip('"').strip("'") for h in headers_input.split(delimiter)]
            return [h for h in headers if h]  # Remove empty strings
    
    # If no delimiter found, treat as single header
    return [headers_input] if headers_input else []


def load_headers_from_csv(csv_filename):
    """Load column headers from a CSV file (assumes headers are in first column)"""
    headers = []
    file_path = cwd + "/" + csv_filename
    
    try:
        with open(file_path) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row and row[0].strip():  # Skip empty rows
                    headers.append(row[0].strip())
        return headers
    except FileNotFoundError:
        print(f"Error: Headers file '{csv_filename}' not found.")
        return []


def main():
    filename = GetArgument("Enter filename in current directory\n", 1)
    
    print("\nHow would you like to provide column headers?")
    print("1. Type them directly (comma-separated)")
    print("2. Load from a CSV file")
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        headers_file = input("Enter headers CSV filename: ").strip()
        column_headers = load_headers_from_csv(headers_file)
    else:
        headers_input = input("Enter column header names (comma-separated): ").strip()
        column_headers = parse_column_headers(headers_input)
    
    if not column_headers:
        print("No valid column headers provided.")
        return
    
    print(f"Processing columns: {column_headers}")
    
    columns_data = extract_columns_data(filename, column_headers)
    
    if columns_data:
        print(f"\nFound unique values:")
        for header, data in columns_data.items():
            print(f"  {header}: {len(data)} unique values")
        
        print("\nHow would you like to save the output?")
        print("1. All columns in one CSV file")
        print("2. Separate CSV file for each column")
        output_choice = input("Enter choice (1 or 2): ").strip()
        
        if output_choice == "2":
            columns_to_separate_csvs(columns_data)
        else:
            output_filename = "unique_values_combined.csv"
            columns_to_csv(columns_data, output_filename)
            print(f"Output saved to {output_filename}")
    else:
        print("No data extracted.")


if __name__ == '__main__':
    main()