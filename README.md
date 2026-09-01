# idol_manager_save_editor

A small Python/Tkinter GUI for viewing and editing Idol Manager JSON save files.

## What it is

- Desktop GUI (Tkinter) that opens an Idol Manager save JSON, lets you edit idol fields, traits, parameters, and save changes.
- Small, single-file codebase with no non-standard runtime dependencies.

## Requirements

- Python 3.8+ (Windows, macOS, Linux)
- Tkinter (usually included with standard Python installers)

Optional (for creating a standalone executable):
- `pyinstaller`

## Run locally

Create and activate a virtual environment, install optional dev deps, then run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # PowerShell (Windows)
# or .venv\Scripts\activate.bat # cmd (Windows)
# or source .venv/bin/activate    # macOS / Linux
pip install -r requirements.txt
python main.py
```
