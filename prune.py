import os
import logging
import tomllib
from pathlib import Path
from datetime import datetime
from tkinter import filedialog
from tqdm import tqdm
import tomli_w

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

    #Creates settings table if missing and returns it; add flag
    changed = False
    settings = config.setdefault("settings", {})

    #Check if threshold value present
    if "threshold" not in settings:
        days_input = input("Enter a threshold for deletion in days: ").strip()

        while True:
            try:
                threshold = int(days_input)
              
                #Disallow negatives
                if threshold <= 0:
                    raise ValueError("Must be a positive number.")
                          
                print(f"You have selected {threshold} days as your threshold.")
                changed = True
                break
            
            except ValueError:
                print("Invalid entry, please try again.")
                days_input = input("Enter a threshold for deletion in days: ").strip()

        settings["threshold"] = threshold

    #Check if a directory value is present
    if "directory" not in settings:

        while True:
            directory = filedialog.askdirectory()

            if len(directory) == 0:
                continue

            changed = True
            break

        settings["directory"] = directory

    #Write to config
    if changed:
        with open(config_path, "wb") as f:
            tomli_w.dump(config, f)

    #Index the file system as it currently exists
    directory = Path(config["settings"]["directory"]) 
    index = fs_index(directory)

    for path in index:
        too_old(path, 90)

    return 0

if __name__ == "__main__":
    main()
