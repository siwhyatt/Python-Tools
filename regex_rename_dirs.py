import os
import re
import sys


def rename_folders(directory, search_pattern, replace_pattern):
    for foldername in os.listdir(directory):
        folder_path = os.path.join(directory, foldername)
        if os.path.isdir(folder_path):
            new_name = re.sub(search_pattern, replace_pattern, foldername)
            if new_name != foldername:
                new_path = os.path.join(directory, new_name)
                os.rename(folder_path, new_path)
                print(f"Renamed: {foldername} -> {new_name}")


def GetArgument(prompt: str, arg_no: int) -> str:
    # Get variable from CLI args. If no arg gien, will prompt.
    if len(sys.argv) > arg_no:
        arg = sys.argv[arg_no]
    else:
        arg = input(prompt)
    return arg


def main():
    # Get CWD
    directory_path = os.getcwd()
    # Prompt for search pattern
    search_pattern = GetArgument("Enter search pattern (regex): ", 2)
    # Prompt for replace pattern
    replace_pattern = GetArgument("Enter replace pattern: ", 3)

    rename_folders(directory_path, search_pattern, replace_pattern)


if __name__ == "__main__":
    main()
