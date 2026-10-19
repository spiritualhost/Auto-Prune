# Auto-Prune

## Setup

The auto-pruner uses a config file called `config.toml` to hold settings. This allows the defaults to be set once instead of at every launch. These defaults include the threshold beyond which files should be deleted (i.e. older than in days) and the directory to prune.

The script will automatically index the directory on every run to ensure the most up-to-date structure is in use. The script defaults to False for each directory, meaning it won't delete them unless that value is adjusted to True. This can be done in the `index.json` file.

To expedite installation on a Windows system, run the `setup.ps1` script an Administrator:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\setup.ps1
```

This will create a directory in Program Files, send a shortcut to the desktop, and create a Task Scheduler task to make the program run automatically at 8 AM daily.

## Execution

Command line options:

```powershell
usage: prune.exe [-h] [-t] [-c] [-r]

options:
  -h, --help       show this help message and exit
  -t, --test       run the program in test mode
  -c, --configure  configure the folder pruning
  -r, --reset      reset user preferences file
```

The test flag will only write to the log, but is a good way of seeing how user preferences will impact an actual run.

The configure flag will allow the user to select or deselect specific folders for pruning. This can also be done manually by changing the values to "true" or false" in the `index.json` after the first run.

The reset flag will remove all old user preferences from the `index.json` for a fresh run.

The executable can be run from anywhere the first time, as it will spawn the necessary files wherever it is placed.

## Compilation

Compile the script into an executable with pyinstaller:

```powershell
pyinstaller --onefile --icon=assets\bonsai.ico prune.py
```
