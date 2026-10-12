# Auto-Prune

## Setup

The auto-pruner uses a config file called `config.toml` to hold settings. This allows the defaults to be set once instead of at every launch.

## Compilation

Compile the script into an executable with pyinstaller:

```powershell
pyinstaller --onefile --icon=assets\bonsai.ico prune.py
```
