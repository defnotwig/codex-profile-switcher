# Codex Switcher Suite

A simple, robust, single-launcher profile management suite for the OpenAI Codex desktop client. This suite enables quick switching between multiple profile accounts (e.g., when usage limits are reached) while sharing the same underlying conversation database.

It integrates with the `@loongphy/codex-auth` CLI tool.

## Key Features

1. **Single Entry Point**: All profiles, login status, stats summary, and account removal options are consolidated into a single interactive launcher (`Codex Switcher.bat`).
2. **Centralized Configuration**: Profile slot mappings are saved locally in a JSON file at `%USERPROFILE%\.codex_profiles.json` (outside the Git repository, keeping your private account emails secure and preventing accidental commits).
3. **Auto-Binding**: Launching the switcher automatically scans registered accounts in the system and binds new/unbound accounts to available empty slots (up to 8 slots).
4. **Interactive colored CLI**: Active accounts are highlighted in bright green, and empty slots are shown in gray.
5. **Switch & Launch**: Selecting a slot (1-8) automatically switches Codex's active authentication to that account, terminates the running Codex client, and restarts it with the new profile.
6. **Easy Installer**: Copies `Codex Switcher.bat` straight to your Desktop.

---

## File Structure

- `Install.bat`: Copies the launcher batch file to your Desktop.
- `Codex Switcher.bat`: The consolidated interactive profile switcher launcher.
- `manage_profiles.py`: Backend python script managing configurations, registry scans, and ANSI CLI display.

---

## Installation & Setup

1. Clone or copy this repository to your Documents folder: `C:\Users\Ludwig Rivera\Documents\codex-profile-switcher`
2. Run `Install.bat` to copy the launcher to your Desktop.
3. Open `Codex Switcher.bat` on your Desktop to manage profiles, switch accounts, log in new ones, or see your usage stats.
