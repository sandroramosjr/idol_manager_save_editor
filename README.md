# idol_manager_save_editor

A small desktop tool for viewing and editing Idol Manager save JSON files.

## What it does

- Open Idol Manager save JSON files and inspect global save state (player name, group, money, scandal points).
- Browse and select idols from the save and edit personal fields: first/last name, nickname, birthday, MBTI, trait ID, parameters (Cute/Cool/etc.), and trivia lines (up to 4).
- Apply global changes (player/group/money/scandal) and per-idol changes in-memory, and save them back to disk.
- Convenience buttons for common actions (maximize parameters, auto-sync zodiac from birthday, and manage trivia entries).

The UI is intentionally lightweight and built with Tkinter so the codebase is a single-file, easy to inspect and modify.
