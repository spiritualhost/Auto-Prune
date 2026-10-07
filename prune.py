import os
import logging
from pathlib import Path

#import tkinter as tk
#from tkinter import filedialog

#Logging set up
logging.basicConfig(
    filename="app.log",
    filemode="w",
    level=logging.INFO, #Set minimum logging threshold to INFO
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

#Index the provided file path recursively.
def fs_index(directory: str) -> list:

    #Check if directory exists
    if not os.path.exists(directory):
        logging.exception("Provided directory does not exist. Exiting.")
        os._exit(1)
    
    folders = [p for p in directory.rglob("*") if p.is_dir()]

    print("Current folder structure:\n")
    for folder in folders:
        print(folder)

    return folders

def main():
    #Log beginning of script runtime
    logging.info("Began auto-prune.")

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
