import os
import shutil


def extract_files_from_subfolders(input_folder_path, output_folder_path):
    os.makedirs(output_folder_path, exist_ok=True)
    for foldername, subfolders, filenames in os.walk(input_folder_path):
        for filename in filenames:
            old_path = os.path.join(foldername, filename)
            new_path = os.path.join(output_folder_path, filename)
            shutil.move(old_path, new_path)
            print(f"Moved: {old_path} to {new_path}")


def main():
    # Get the current working directory (Input Folder)
    input_folder_path = os.getcwd()

    # Get the parent directory (Home)
    parent_dir = os.path.dirname(input_folder_path)

    # Specify the output folder name
    output_folder_name = "Output Folder"

    # Create full path for output folder
    output_folder_path = os.path.join(parent_dir, output_folder_name)

    # Call the function
    extract_files_from_subfolders(input_folder_path, output_folder_path)


if __name__ == "__main__":
    main()
