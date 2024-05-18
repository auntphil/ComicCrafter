import os

def rename_folder(old, new):
    try:
        os.rename(old, new)
        print(f"Folder '{old}' has been renamed to '{new}'.")
    except FileNotFoundError:
        print(f"Error: Folder '{old}' not found.")
    except FileExistsError:
        print(f"Error: Folder '{new}' already exists.")
    except PermissionError:
        print(f"Error: Permission Issue '{new}'")
        