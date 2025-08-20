#!/usr/bin/env python3
"""
Recursive Directory Cleaner
A script to recursively delete files matching a regex pattern from a directory tree.
"""

import os
import re
import argparse
from pathlib import Path


def find_matching_files(directory, pattern):
    """
    Find all files that match the given regex pattern.
    
    Args:
        directory (str): Root directory to search
        pattern (str): Regex pattern to match filenames
    
    Returns:
        list: List of Path objects for matching files
    """
    compiled_pattern = re.compile(pattern)
    matching_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if compiled_pattern.match(file):
                matching_files.append(Path(root) / file)
    
    return matching_files


def delete_files(file_list, dry_run=False):
    """
    Delete files from the provided list.
    
    Args:
        file_list (list): List of Path objects to delete
        dry_run (bool): If True, only print what would be deleted
    
    Returns:
        tuple: (successful_deletions, failed_deletions)
    """
    successful = 0
    failed = 0
    
    for file_path in file_list:
        try:
            if dry_run:
                print(f"Would delete: {file_path}")
            else:
                file_path.unlink()
                print(f"Deleted: {file_path}")
            successful += 1
        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")
            failed += 1
    
    return successful, failed


def main():
    parser = argparse.ArgumentParser(
        description="Recursively delete files matching a regex pattern",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Delete files starting with ._ (like ._filename.jpg)
  python clean_directory.py /path/to/folder "^\._.*"
  
  # Delete all .tmp files
  python clean_directory.py /path/to/folder ".*\.tmp$"
  
  # Dry run to see what would be deleted
  python clean_directory.py /path/to/folder "^\._.*" --dry-run
        """
    )
    
    parser.add_argument(
        "directory",
        help="Root directory to search"
    )
    
    parser.add_argument(
        "pattern",
        help="Regex pattern to match filenames (e.g., '^\._.*' for files starting with ._)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without actually deleting"
    )
    
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Ask for confirmation before deleting files"
    )
    
    args = parser.parse_args()
    
    # Validate directory
    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a valid directory")
        return 1
    
    # Validate regex pattern
    try:
        re.compile(args.pattern)
    except re.error as e:
        print(f"Error: Invalid regex pattern '{args.pattern}': {e}")
        return 1
    
    print(f"Searching for files matching pattern: {args.pattern}")
    print(f"In directory: {args.directory}")
    print()
    
    # Find matching files
    matching_files = find_matching_files(args.directory, args.pattern)
    
    if not matching_files:
        print("No files found matching the pattern.")
        return 0
    
    print(f"Found {len(matching_files)} files matching the pattern:")
    for file_path in matching_files:
        print(f"  {file_path}")
    print()
    
    # Confirm deletion if requested
    if args.confirm and not args.dry_run:
        response = input(f"Are you sure you want to delete these {len(matching_files)} files? (y/N): ")
        if response.lower() not in ['y', 'yes']:
            print("Deletion cancelled.")
            return 0
    
    # Delete files
    successful, failed = delete_files(matching_files, args.dry_run)
    
    print(f"\nSummary:")
    if args.dry_run:
        print(f"  Would delete: {successful} files")
        print(f"  Would fail: {failed} files")
    else:
        print(f"  Successfully deleted: {successful} files")
        print(f"  Failed to delete: {failed} files")
    
    return 0


if __name__ == "__main__":
    exit(main())
