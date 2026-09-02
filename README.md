# idol_manager_save_editor

A small desktop tool for viewing and editing Idol Manager save JSON files.

## What it does

- Open Idol Manager save JSON files and inspect global save state (player name, group, money, scandal points).
- Browse and select idols from the save and edit personal fields: first/last name, nickname, birthday, MBTI, trait ID, parameters (Cute/Cool/etc.), and trivia lines (up to 4).
- Apply global changes (player/group/money/scandal) and per-idol changes in-memory, and save them back to disk.
- Convenience buttons for common actions (maximize parameters, auto-sync zodiac from birthday, and manage trivia entries).

The UI is intentionally lightweight and built with Tkinter so the codebase is a single-file, easy to inspect and modify.

## Download and run (no Python required)

- Pre-built binaries are provided as GitHub Release assets for each release tag. Download the appropriate platform artifact from the Releases page: https://github.com/sandroramosjr/idol_manager_save_editor/releases
- The provided `.exe` (Windows) or `.zip` (macOS) is a self-contained executable produced by PyInstaller — users do NOT need Python or any dependencies to run the binary. Just download and double-click.

Security note: verify checksums published alongside each release asset before running any binary.

## Run from source (if you want to inspect or modify code)

If you prefer to run the app from source you will need Python 3.8+ and Tkinter:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # PowerShell (Windows)
pip install -r requirements.txt
python main.py
```

## Build releases locally (optional)

Use `pyinstaller` to create single-file executables locally. Example (Windows):

```powershell
pip install pyinstaller
pyinstaller --onefile --noconsole --name idol-manager-windows main.py
```

On macOS you must build on a macOS host:

```bash
pip install pyinstaller
pyinstaller --onefile --name idol-manager-macos main.py
zip idol-manager-macos_v0.1.zip dist/idol-manager-macos
```

## Releases and CI

This repository provides GitHub Actions workflows that build release artifacts on tag creation and attach the compiled binaries and SHA256 checksums to the GitHub Release. To build artifacts on CI, push a tag like `v0.1` and the workflows will run automatically.

## Contributing / Further work

- If you share example save files I can add preset field mappings and nicer UI mappings for common save fields.
- I can add more checks (format validation), or convert the parameter editors into sliders.

## License

This repository does not include a license file. Add one if you plan to publish or share the code publicly.
