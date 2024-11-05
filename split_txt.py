import os
import math

def split_file(input_file, max_size_mb=30):
    # Convert MB to bytes
    max_size_bytes = max_size_mb * 1024 * 1024
    
    # Get the base filename without extension
    base_name = os.path.splitext(input_file)[0]
    
    # Get total file size
    file_size = os.path.getsize(input_file)
    
    # Calculate number of chunks needed
    num_chunks = math.ceil(file_size / max_size_bytes)
    
    # Read and split the file
    with open(input_file, 'r', encoding='utf-8') as f:
        for chunk_num in range(num_chunks):
            # Calculate chunk size for even distribution
            chunk_size = min(max_size_bytes, file_size - (chunk_num * max_size_bytes))
            
            # Create chunk filename
            chunk_filename = f"{base_name}_part{chunk_num + 1}.txt"
            
            # Read chunk_size bytes
            content = f.read(chunk_size)
            
            # Write chunk to new file
            with open(chunk_filename, 'w', encoding='utf-8') as chunk_file:
                chunk_file.write(content)
            
            print(f"Created {chunk_filename} ({len(content) / 1024 / 1024:.2f} MB)")

def main():
    # Get input file path from user
    input_file = input("Enter the path to your text file: ")
    
    # Validate file exists
    if not os.path.exists(input_file):
        print("Error: File does not exist!")
        return
    
    try:
        split_file(input_file)
        print("File splitting completed successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
