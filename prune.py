import os
from pathlib import Path

#import tkinter as tk
#from tkinter import filedialog

#Index the provided file path recursively.
def fs_index(directory: str) -> list:

    #Check if directory exists
    if os.path.exists(directory):
        print(f"Good to go, path \"{directory}\" exists.")

    folders = [p for p in directory.rglob("*") if p.is_dir()]

    print("Current folder structure:\n")
    for folder in folders:
        print(folder)

    return folders

def main():
    print("This is the main function of this script.")

    #Check if the config.toml file exists

    #Check if the config.toml file has a path in it already
    #If not, open filedialog to allow the user to select a path
    #directory = filedialog.askdirectory()

    #Index the file system as it currently exists
    directory = Path("testdir\\migration") #Testing
    fs_index(directory)

    return 0

if __name__ == "__main__":
    main()
