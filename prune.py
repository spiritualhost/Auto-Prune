import os
import logging
import tomllib
from pathlib import Path
from datetime import datetime
from tqdm import tqdm
import tomli_w

#import tkinter as tk
#from tkinter import filedialog

#Set global variables
date_today = datetime.now()

#Logging set up
logging.basicConfig(
    filename="app.log",
    filemode="w",
    level=logging.INFO, #Set minimum logging threshold to INFO
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

#Make a config file
def make_config():
    lines = ["[settings]\n"]
    with open("config.toml", "w", encoding="utf-8") as f:
        f.writelines(lines)

#Index the provided file path recursively.
def fs_index(directory: str) -> list:

    logging.info("Starting index of directory %s.", directory)

    #Check if directory exists
    if not os.path.exists(directory):
        logging.exception("Provided directory does not exist. Exiting.")
        os._exit(1)

    #Comprehend a list of all directories under the head
    #tqdm will count all items considered prior to the filter and won't match the final item count
    folders = [p for p in tqdm(directory.rglob("*")) if p.is_dir()]

    print("Current folder structure:")
    for folder in folders:
        print(folder)

    logging.info("Succcessful index -- returning pathlist.")

    return folders

#Check the age of the items at the provided paths against threshold
def too_old(path: Path, threshold: int) -> bool:

    logging.info("Checking age of %s", path)

    #Get the modification time timestamp
    timestamp = path.stat().st_mtime

    #Convert timestamp to a datetime object
    modification_date = datetime.fromtimestamp(timestamp)

    #Get difference between today and the modification time
    difference = (date_today - modification_date).days

    if difference >= threshold:
        print(f"Test ~~ Deleting folder {path}")
        logging.info("Folder older than threshold.")
        return True
    return False

def main():
    #Log beginning of script runtime
    logging.info("Beginning auto-prune.")

    #Check if the config.toml file exists
    if not os.path.exists("config.toml"):
        logging.warning("No config file exists. Creating new config file.")
        make_config()

    #Load and parse the config file
    config_path = Path("config.toml")
    with open(config_path, "rb") as f:
        config = tomllib.load(f)

    #Check if threshold value present
    if "threshold" not in config:
        days_input = input("Enter a threshold for deletion in days: ").strip()

        while True:
            try:
                threshold = int(days_input)
                
                #Disallow negatives
                if threshold <= 0:
                    raise ValueError("Negative numbers are not allowed.")
                
                print(f"You have selected {threshold} days as your threshold.")
                break
            
            except ValueError:
                print("Invalid entry, please try again.")
                days_input = input("Enter a threshold for deletion in days: ").strip()

        config["settings"]["threshold"] = threshold




    #Write to config
    with open(config_path, "wb") as f:
        tomli_w.dump(config, f)

    #print(config["settings"]["threshold"])

    #Check if the config.toml file has a path in it already
    #If not, open filedialog to allow the user to select a path
    #directory = filedialog.askdirectory()

    #Index the file system as it currently exists
    directory = Path("testdir\\migration") #Testing
    index = fs_index(directory)

    for path in index:
        too_old(path, 90)

    return 0

if __name__ == "__main__":
    main()
