import sys
import re

def main():
    if len(sys.argv) < 3:
        print("Usage: python update_profile.py <bat_path> <email>")
        sys.exit(1)
        
    bat_path = sys.argv[1]
    new_email = sys.argv[2]
    
    try:
        with open(bat_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        pattern = r'^SET "ACCOUNT_EMAIL=[^"]*"'
        replacement = f'SET "ACCOUNT_EMAIL={new_email}"'
        
        if re.search(pattern, content, flags=re.MULTILINE):
            new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        else:
            lines = content.splitlines()
            insert_idx = 0
            for i, line in enumerate(lines):
                if line.strip().lower() == "@echo off":
                    insert_idx = i + 1
                    break
            lines.insert(insert_idx, replacement)
            new_content = "\n".join(lines)
            
        with open(bat_path, "w", encoding="utf-8", newline="\r\n") as f:
            f.write(new_content)
            
        print(f"Successfully updated {bat_path} with email '{new_email}'.")
    except Exception as e:
        print(f"Error updating profile: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
