import os
import sys
import json
import re
import subprocess
import time

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

def show_stats():
    try:
        out = subprocess.check_output(['npx', '@loongphy/codex-auth', 'list'], text=True, shell=True)
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return

    lines = out.splitlines()
    if len(lines) < 2:
        print(out)
        return

    # Print original header columns and divider line
    print(lines[0])
    print(lines[1])

    # Parse account rows
    stats_map = {}
    email_regex = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    
    for line in lines[2:]:
        if not line.strip():
            continue
        match = email_regex.search(line)
        if match:
            email = match.group(0).lower()
            stats_part = line[match.end():]
            stats_map[email] = stats_part

    config = load_config()
    _, active_email = get_codex_accounts()
    active_email_lower = active_email.lower() if active_email else ""

    # Print stats in the order of slots
    for i in range(1, TOTAL_SLOTS + 1):
        slot_str = str(i)
        email = config.get(slot_str, "")
        if email:
            email_lower = email.lower()
            stats_part = stats_map.get(email_lower, "")
            
            is_active = (email_lower == active_email_lower)
            if is_active:
                prefix = f"{COLOR_GREEN}* {i:02d} {COLOR_RESET}"
                email_col = f"{COLOR_GREEN}{email:<45}{COLOR_RESET}"
                stats_col = f"{COLOR_GREEN}{stats_part.lstrip()}{COLOR_RESET}" if stats_part else ""
                print(f"{prefix}{email_col}{stats_col}")
            else:
                prefix = f"  {i:02d} "
                email_col = f"{email:<45}"
                stats_col = stats_part.lstrip() if stats_part else ""
                print(f"{prefix}{email_col}{stats_col}")

logo_lines = [
    "       .---.          ",
    "    .-'     `-.       ___  ___  ___  ___ _  _    ___ _ _ _ _ ___ ___ _  _ ___ ___ ",
    "  _(   > _     )_    / __\\/ _ \\|   \\| __\\ \\/ /  / __\\ \\ \\ /_ _// __\\ _ \\/ __\\ _ \\\\",
    " (               )   \\___/\\___/|___/\\___//_\\    \\___/ \\_/\\_//_/ \\___/|_| |___|_\\_\\",
    "  `-._________.-'     "
]

def get_animation_frame(frame_num):
    line0 = " " * 80
    line1 = " " * 80
    line2 = " " * 80
    watermark = "[ Developed by @defnotwig ]"
    
    if frame_num == 0:
        line0 = line0[:2] + "  O _ [Coding...]"
        line1 = line1[:2] + " /|/ [__]"
        line2 = line2[:2] + " / \\" + " " * 29 + watermark
    elif frame_num == 1:
        line0 = line0[:2] + "  O"
        line1 = line1[:2] + " /|~  [__]"
        line2 = line2[:2] + " / \\" + " " * 29 + watermark
    elif frame_num in (2, 3, 4, 5):
        cols = {2: 8, 3: 15, 4: 22, 5: 28}
        col = cols[frame_num]
        if frame_num % 2 == 0:
            legs = "/ \\"
            arms = "/|~"
        else:
            legs = " | "
            arms = "~|~"
        line0 = line0[:col] + "  O"
        line1 = line1[:col] + " " + arms + " [__]"
        line2 = line2[:col] + " " + legs + " " * (32 - col - 4) + watermark
    elif frame_num == 6:
        col = 30
        line0 = " " * 30 + "  O"
        line1 = " " * 30 + " /|/"
        line2 = " " * 29 + "|| " + watermark
        
    return line0.rstrip(), line1.rstrip(), line2.rstrip()

def animate_logo():
    os.system('')
    
    l0, l1, l2 = get_animation_frame(0)
    print(l0)
    print(l1)
    print(COLOR_GREEN + l2 + COLOR_RESET)
    for line in logo_lines:
        print(COLOR_YELLOW + line + COLOR_RESET)
    print()

    for f in range(1, 7):
        time.sleep(0.18)
        sys.stdout.write("\033[8A\r")
        sys.stdout.flush()
        
        l0, l1, l2 = get_animation_frame(f)
        print(l0.ljust(80))
        print(l1.ljust(80))
        print(COLOR_GREEN + l2.ljust(80) + COLOR_RESET)
        for line in logo_lines:
            print(COLOR_YELLOW + line.ljust(100) + COLOR_RESET)
        print()

def print_static_logo():
    l0, l1, l2 = get_animation_frame(6)
    print(l0)
    print(l1)
    print(COLOR_GREEN + l2 + COLOR_RESET)
    for line in logo_lines:
        print(COLOR_YELLOW + line + COLOR_RESET)
    print()

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
    elif command == "show-stats":
        show_stats()
    elif command == "logo":
        animate_logo()
    elif command == "logo-static":
        print_static_logo()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
