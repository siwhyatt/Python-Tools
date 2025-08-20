import os
import sys
from pathlib import Path

def should_exclude_path(path, excluded_folders, excluded_extensions):
    """
    Check if a path should be excluded based on folder names or extensions.
    
    Args:
        path (Path): Path object to check
        excluded_folders (set): Set of folder names to exclude
        excluded_extensions (set): Set of file extensions to exclude
    
    Returns:
        bool: True if path should be excluded, False otherwise
    """
    # Check if any parent folder matches excluded folders
    for parent in path.parents:
        if parent.name in excluded_folders:
            return True
            
    # Check file extension if it's a file
    if path.is_file() and path.suffix.lower() in excluded_extensions:
        return True
        
    return False

def get_default_excluded_folders():
    """Returns the default set of folders to exclude"""
    return {
        'node_modules',
        '__pycache__',
        '.git',
        'venv',
        '.env',
        'dist',
        'build',
        'coverage'
    }

def get_default_excluded_extensions():
    """Returns the default set of extensions to exclude"""
    return {
        '.exe', '.dll', '.so', '.dylib',  # Binaries
        '.png', '.jpg', '.jpeg', '.gif',  # Images
        '.pdf', '.doc', '.docx',          # Documents
        '.zip', '.tar', '.gz', '.7z', '.rar',  # Archives
        '.pyc', '.pyo',                   # Python bytecode
        '.class',                         # Java bytecode
        '.o', '.obj'                      # Object files
    }

def scrape_directory(directory_path, output_file, additional_excluded_folders=None, 
                    additional_excluded_extensions=None):
    """
    Recursively scrape all files in a directory and write their contents to a single file.
    
    Args:
        directory_path (str): Path to the directory to scrape
        output_file (str): Path to the output file
        additional_excluded_folders (set): Additional folder names to exclude
        additional_excluded_extensions (set): Additional file extensions to exclude
    """
    # Combine default and additional exclusions
    excluded_folders = get_default_excluded_folders()
    excluded_extensions = get_default_excluded_extensions()
    
    if additional_excluded_folders:
        excluded_folders.update(additional_excluded_folders)
    
    if additional_excluded_extensions:
        excluded_extensions.update(additional_excluded_extensions)
    
    # Convert directory path to Path object
    directory = Path(directory_path)
    
    # Track processed files for statistics
    stats = {
        'processed_files': 0,
        'skipped_files': 0,
        'errors': 0
    }
    
    # Create or open the output file in write mode
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Write header with scanning information
        outfile.write(f'Directory Scan Results\n')
        outfile.write(f'{"="*80}\n')
        outfile.write(f'Source Directory: {directory}\n')
        outfile.write(f'Excluded Folders: {sorted(excluded_folders)}\n')
        outfile.write(f'Excluded Extensions: {sorted(excluded_extensions)}\n\n')
        
        # Iterate through all files in directory and subdirectories
        for file_path in directory.rglob('*'):
            if should_exclude_path(file_path, excluded_folders, excluded_extensions):
                stats['skipped_files'] += 1
                continue
                
            if file_path.is_file():
                try:
                    # Write file path as a header
                    outfile.write(f'\n{"="*80}\n')
                    outfile.write(f'File: {file_path}\n')
                    outfile.write(f'{"="*80}\n\n')
                    
                    # Read and write the file contents
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                        outfile.write(content)
                        outfile.write('\n')
                        
                    stats['processed_files'] += 1
                        
                except Exception as e:
                    outfile.write(f'Error reading file {file_path}: {str(e)}\n')
                    stats['errors'] += 1
                    continue
        
        # Write summary at the end
        outfile.write(f'\n{"="*80}\n')
        outfile.write('Scan Summary\n')
        outfile.write(f'{"="*80}\n')
        outfile.write(f'Files Processed: {stats["processed_files"]}\n')
        outfile.write(f'Files Skipped: {stats["skipped_files"]}\n')
        outfile.write(f'Errors Encountered: {stats["errors"]}\n')


def GetArgument(prompt: str, arg_no: int) -> str:
    # Get variable from CLI args. If no arg gien, will prompt.
    if len(sys.argv) > arg_no:
        arg = sys.argv[arg_no]
    else:
        arg = input(prompt)
    return arg


def main():
    # Example usage
    filename_prefix = GetArgument("File prefix: ", 1)
    directory_to_scrape = os.getcwd()
    folder = directory_to_scrape.split("/")
    output_file_path = f"/home/siwhyatt/Downloads/{filename_prefix}_{folder[-1]}_content.txt"
    
    # Optional: Add more folders or extensions to exclude
    # These will be added to the default exclusions, not replace them
    additional_excluded_folders = {
        'temp',
        'logs'
    }
    
    additional_excluded_extensions = {
        '.log',
        '.tmp',
        '.json'
    }
    
    try:
        scrape_directory(
            directory_to_scrape,
            output_file_path,
            additional_excluded_folders,
            additional_excluded_extensions
        )
        print(f"Successfully created {output_file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
