<<<<<<< HEAD
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

## Run locally (recommended)

Create and activate a virtual environment, install optional dev deps, then run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # PowerShell (Windows)
# or .venv\Scripts\activate.bat # cmd (Windows)
# or source .venv/bin/activate    # macOS / Linux
pip install -r requirements.txt
python main.py
```

## Build a portable executable (Windows example)

1. Install PyInstaller in the virtualenv:

```powershell
pip install pyinstaller
```

2. Build a single-file GUI executable (no console):

```powershell
pyinstaller --onefile --noconsole main.py
```

3. The produced executable will be at `dist\main.exe` — you can copy that to other Windows machines.

Notes:
- Because the project uses only the Python standard library and Tkinter, packaging is usually straightforward on Windows. On macOS/Linux, adjust `pyinstaller` flags and testing accordingly.

## Uploading to your GitHub (private) — suggested workflow

1. Initialize the repository locally (if not already):

```powershell
git init
git add .
git commit -m "Initial import: Idol Manager Save Editor"
```

2. Create a *private* repository on GitHub (via the website) and copy the repo URL (HTTPS or SSH).

3. Add the remote and push:

```powershell
git remote add origin https://github.com/<your-username>/<repo>.git
git branch -M main
git push -u origin main
```

Alternative (if you have GitHub CLI `gh` installed):

```powershell
gh repo create <your-username>/<repo> --private --source=. --remote=origin --push
```

I cannot push to your account for you (no access), but the commands above will do it once you create the remote and authenticate.

## What I changed in this repo (if you want me to automate more)

- Add a minimal `README.md` with run/package/publish instructions.
- Add a `.gitignore` and `requirements.txt` (optional) so the repo is ready for commit.

If you want, I can:

- Initialize the local Git repo and make the initial commit here.
- Walk you through creating the private GitHub repo and pushing.
- Run `pyinstaller` to produce a portable executable and attach the produced `dist\main.exe` for download (note: large binary).

Tell me which of those you'd like me to do next.
