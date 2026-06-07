import os
import sys
import json
import re
import subprocess

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".codex_profiles.json")
TOTAL_SLOTS = 8

# ANSI colors
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_GRAY = "\033[90m"
COLOR_RESET = "\033[0m"

def load_config():
    if not os.path.exists(CONFIG_PATH):
        # Initialize with empty slots
        config = {str(i): "" for i in range(1, TOTAL_SLOTS + 1)}
        save_config(config)
        return config
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
            # Ensure all slots are present
            for i in range(1, TOTAL_SLOTS + 1):
                if str(i) not in config:
                    config[str(i)] = ""
            return config
    except Exception:
        config = {str(i): "" for i in range(1, TOTAL_SLOTS + 1)}
        save_config(config)
        return config

def save_config(config):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"Error saving config: {e}")

def get_codex_accounts():
    """Returns (registered_emails, active_email)"""
    try:
        out = subprocess.check_output(['npx', '@loongphy/codex-auth', 'list'], text=True, shell=True)
        emails = []
        active_email = ""
        for line in out.splitlines():
            parts = line.split()
            if not parts:
                continue
            if parts[0] == '*' and len(parts) > 2:
                emails.append(parts[2])
                active_email = parts[2]
            elif parts[0].isdigit() and len(parts) > 1:
                emails.append(parts[1])
        return emails, active_email
    except Exception as e:
        print(f"Error listing accounts: {e}")
        return [], ""

def autobind():
    config = load_config()
    registered_emails, _ = get_codex_accounts()
    if not registered_emails:
        return

    # Determine which emails are already bound
    bound_emails = {email.lower() for email in config.values() if email}
    unbound_emails = [email for email in registered_emails if email.lower() not in bound_emails]

    if not unbound_emails:
        return

    bound_count = 0
    for email in unbound_emails:
        # Find first empty slot
        bound = False
        for i in range(1, TOTAL_SLOTS + 1):
            slot_str = str(i)
            if not config[slot_str]:
                config[slot_str] = email
                print(f"Auto-bound {email} to Slot {slot_str}")
                bound_count += 1
                bound = True
                break
        if not bound:
            print(f"No empty slots available to bind {email}!")
            break

    if bound_count > 0:
        save_config(config)
        print(f"Auto-binding completed. Bound {bound_count} account(s).")

def get_slot_email(slot):
    config = load_config()
    email = config.get(str(slot), "")
    print(email)

def unbind_slot(slot):
    config = load_config()
    slot_str = str(slot)
    if slot_str in config and config[slot_str]:
        old_email = config[slot_str]
        config[slot_str] = ""
        save_config(config)
        print(f"Cleared Slot {slot_str} (was bound to {old_email}).")
    else:
        print(f"Slot {slot_str} is already empty.")

def bind_slot(slot, email):
    config = load_config()
    slot_str = str(slot)
    config[slot_str] = email
    save_config(config)
    print(f"Bound Slot {slot_str} to {email}.")

def show_menu():
    config = load_config()
    _, active_email = get_codex_accounts()
    active_email_lower = active_email.lower() if active_email else ""

    print(" Slot   Status     Profile Account")
    print("------------------------------------------------------------")
    for i in range(1, TOTAL_SLOTS + 1):
        slot_str = str(i)
        email = config.get(slot_str, "")
        
        if email:
            is_active = (email.lower() == active_email_lower)
            if is_active:
                status_str = f"{COLOR_GREEN}ACTIVE{COLOR_RESET}   "
                email_str = f"{COLOR_GREEN}{email}{COLOR_RESET}"
            else:
                status_str = "INACTIVE "
                email_str = email
            print(f"  [{i}]   {status_str}  {email_str}")
        else:
            print(f"  [{i}]   {COLOR_GRAY}[Empty]{COLOR_RESET}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python manage_profiles.py <command> [args]")
        sys.exit(1)

    command = sys.argv[1].lower()
    if command == "init":
        load_config()
    elif command == "autobind":
        autobind()
    elif command == "get":
        if len(sys.argv) < 3:
            print("Missing slot number.")
            sys.exit(1)
        get_slot_email(sys.argv[2])
    elif command == "unbind":
        if len(sys.argv) < 3:
            print("Missing slot number.")
            sys.exit(1)
        unbind_slot(sys.argv[2])
    elif command == "bind":
        if len(sys.argv) < 4:
            print("Usage: bind <slot> <email>")
            sys.exit(1)
        bind_slot(sys.argv[2], sys.argv[3])
    elif command == "show-menu":
        show_menu()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
