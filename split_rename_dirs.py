import os


def rename_folders(directory):
    for foldername in os.listdir(directory):
        folder_path = os.path.join(directory, foldername)
        if os.path.isdir(folder_path):
            new_name = foldername.split("_")
            new_name = new_name[0] + "_" + new_name[1]
            new_name = new_name.upper()
            if new_name != foldername:
                new_path = os.path.join(directory, new_name)
                os.rename(folder_path, new_path)
                print(f"Renamed: {foldername} -> {new_name}")


# def GetArgument(prompt: str, arg_no: int) -> str:
#     # Get variable from CLI args. If no arg gien, will prompt.
#     if len(sys.argv) > arg_no:
#         arg = sys.argv[arg_no]
#     else:
#         arg = input(prompt)
#     return arg


def main():
    # Get CWD
    directory_path = os.getcwd()
    rename_folders(directory_path)


if __name__ == "__main__":
    main()
