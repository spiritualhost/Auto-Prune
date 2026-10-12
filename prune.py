import os
import logging
import tomllib
import argparse
import json
from pathlib import Path
from datetime import datetime
from tkinter import filedialog
from tqdm import tqdm
import tomli_w
from InquirerPy import inquirer
from InquirerPy.base import Choice


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

#Add argparse setup for cmd line flags
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--test", help="run the program in test mode",
                    action="store_true")
parser.add_argument("-c", "--configure", help="configure the folder pruning",
                    action="store_true")
parser.add_argument("-r", "--reset", help="reset user preferences file",
                    action="store_true")
args = parser.parse_args()
if args.test:
    print("Running in test mode.")

#Make a config file
def make_config():
    lines = ["[settings]\n"]
    with open("config.toml", "w", encoding="utf-8") as f:
        f.writelines(lines)

#User configuration of pruning
def configure():
    print("Entering configuration mode.")
    try:
        with open("index.json", "r") as f:
            loaded_index = json.load(f)

        choices = [Choice(value=str(key), enabled=value) for key, value in loaded_index.items()]

        #Allow the user to fuzzy search through index and select folders to prune
        pruned_paths = inquirer.fuzzy(
            message="Select multiple items (Type to filter, Tab to toggle, Enter to submit):",
            choices=choices,
            multiselect=True
        ).execute()

        #Apply the configurations
        for path in pruned_paths:
            loaded_index[path] = True

        with open("index.json", "w") as f:
            json.dump(loaded_index, f, indent=4)

        os._exit(0)

    except FileNotFoundError:
        logging.critical("Index file not found for configuration.")
        os._exit(1)

    except PermissionError:
        logging.critical("You do not have permissions to access the index file.")
        os._exit(1)

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

    #Dictionarify the index (default to not prune: False)
    index_dict = {str(folder): False for folder in index}

    #If user wants to reset user preferences (-r | --reset)
    if args.reset == True:
        try:
            os.remove("index.json")
            logging.info("Removed old index.")
        except FileNotFoundError:
            logging.error("File 'index.json' not found. No file deleted.")
        except PermissionError:
            logging.error("You do not have permission to delete 'index.json'.")

    #Compare the new index to the previous index if it exists
    if os.path.exists("index.json"):
        with open("index.json", "r") as file:
            previous_index = json.load(file)
        
        for key, value in previous_index.items():
            #If there is a matching key in both dictionaries
            #And the previous dictionary was already set to True
            #Change the new key's value to True before dumping to file (maintains preferences)
            if value is True and key in index_dict:
                index_dict[key] = True 

    #Dump dictionarified index into json file
    logging.info("Writing dictionarified index to json file.")
    with open("index.json", "w") as f:
        json.dump(index_dict, f, indent=4)

    #If running in configuration mode (-c | --configure), then exit
    if args.configure:
        configure()

    #If running in test mode, find all the applicable files and write to the log

    #Else: just run through and prune automatically

    #Check folders against threshold
    threshold = config["settings"]["threshold"]
    for path in index:
        too_old(path, threshold)

    return 0

if __name__ == "__main__":
    main()
