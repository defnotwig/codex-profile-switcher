import os
import re
import subprocess

DESKTOP_DIR = r"C:\Users\Ludwig Rivera\Desktop"

def get_registered_emails():
    try:
        out = subprocess.check_output(['npx', '@loongphy/codex-auth', 'list'], text=True, shell=True)
        emails = []
        for line in out.splitlines():
            parts = line.split()
            if not parts:
                continue
            if parts[0] == '*' and len(parts) > 2:
                emails.append(parts[2])
            elif parts[0].isdigit() and len(parts) > 1:
                emails.append(parts[1])
        return emails
    except Exception as e:
        print(f"Error listing accounts: {e}")
        return []

def get_profile_files():
    files = []
    if not os.path.exists(DESKTOP_DIR):
        return []
    for f in os.listdir(DESKTOP_DIR):
        if f.startswith("Codex Profile ") and f.endswith(".bat"):
            files.append(os.path.join(DESKTOP_DIR, f))
    
    def get_num(filename):
        match = re.search(r'Codex Profile (\d+)\.bat', filename)
        return int(match.group(1)) if match else 999
    files.sort(key=get_num)
    return files

def get_bound_email(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        match = re.search(r'^SET "ACCOUNT_EMAIL=([^"]*)"', content, flags=re.MULTILINE)
        return match.group(1) if match else ""
    except Exception:
        return ""

def main():
    registered_emails = get_registered_emails()
    if not registered_emails:
        print("No registered accounts found.")
        return
        
    profile_files = get_profile_files()
    if not profile_files:
        print("No profile batch files found on Desktop.")
        return
        
    bound_emails = set()
    empty_profiles = []
    
    for f in profile_files:
        email = get_bound_email(f)
        if email:
            bound_emails.add(email.lower())
        else:
            empty_profiles.append(f)
            
    unbound_emails = [email for email in registered_emails if email.lower() not in bound_emails]
    
    print(f"Registered accounts: {registered_emails}")
    print(f"Bound accounts: {list(bound_emails)}")
    print(f"Unbound accounts: {unbound_emails}")
    
    if not unbound_emails:
        print("All registered accounts are already bound to profiles.")
        return
        
    if not empty_profiles:
        print("No empty profile slots available.")
        return
        
    bound_count = 0
    for email in unbound_emails:
        if not empty_profiles:
            break
        empty_profile = empty_profiles.pop(0)
        try:
            with open(empty_profile, "r", encoding="utf-8") as f:
                content = f.read()
            pattern = r'^SET "ACCOUNT_EMAIL=[^"]*"'
            replacement = f'SET "ACCOUNT_EMAIL={email}"'
            new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            with open(empty_profile, "w", encoding="utf-8", newline="\r\n") as f:
                f.write(new_content)
            print(f"Auto-bound {email} to {os.path.basename(empty_profile)}")
            bound_count += 1
        except Exception as e:
            print(f"Error binding to {empty_profile}: {e}")
            
    print(f"Auto-binding completed. Bound {bound_count} accounts.")

if __name__ == "__main__":
    main()
