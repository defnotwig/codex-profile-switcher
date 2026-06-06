# Codex Profile Switcher Suite

A simple, robust profile management suite for the OpenAI Codex desktop client. This suite enables quick switching between multiple profile accounts (e.g., when usage limits are reached) while sharing the same underlying conversation database.

It integrates with the `@loongphy/codex-auth` CLI tool.

## Key Features

1. **Multiple Profile Slots**: Up to 4 (or more) profile launchers (`Codex Profile 1.bat` to `Codex Profile 4.bat`) that bind to specific OpenAI Codex accounts.
2. **Auto-Binding**: Running `Codex Usage Summary.bat` scans the registered accounts in the system and automatically binds any newly logged-in/unbound accounts to available empty profile slots.
3. **Easy Switching**: Each profile launcher shows its current state (ACTIVE or INACTIVE). Opening it automatically switches Codex's authentication to that profile and restarts the Codex application (auto-selects switch in 5 seconds).
4. **Unbinding/Removal**: Remove/unbind an account from a specific profile slot at any time to free it up for a new account.
5. **Install Script**: Copies all launcher batch files directly to your Desktop.

---

## File Structure

- `Install.bat`: Copies all launcher batch files from this repository directory to your Desktop.
- `Codex Profile 1.bat` - `Codex Profile 4.bat`: Individual profile launcher shortcuts.
- `Codex Usage Summary.bat`: Scanner and statistics summary helper.
- `auto_bind_profiles.py`: Background helper that automatically assigns logged-in accounts to empty profile slots on the Desktop.
- `update_profile.py`: Background helper that updates profile configuration slots.

---

## Installation & Setup

1. Clone or copy this repository to your Documents folder: `C:\Users\Ludwig Rivera\Documents\codex-profile-switcher`
2. Run `Install.bat` to copy the launchers to your Desktop.
3. Open any of the profile launchers on your Desktop to log in or switch accounts.
4. Open `Codex Usage Summary.bat` on your Desktop to view stats, list all active/inactive profiles, and auto-bind new accounts.
