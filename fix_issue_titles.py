import json
import subprocess
import time
import re
import os

def generate_better_title(title, body):
    # Extract file name without path
    file_match = re.search(r"in ([\w/._\\\\-]+):", title)
    if not file_match:
        file_match = re.search(r"in ([\w/._\\\\-]+)$", title)
    
    if file_match:
        full_path = file_match.group(1).replace('\\', '/')
        file_name = os.path.basename(full_path)
    else:
        file_name = "unknown_file.py"

    if "Pylint" in title:
        # Extract the actual message from the original body
        msg_match = re.search(r"- \*\*Message\*\*: (.*)", body)
        if msg_match:
            msg = msg_match.group(1).strip()
            # E.g. "Unused argument 'parent_run_id'"
            return f"Code Quality: {msg} in {file_name}"
        else:
            # Fallback
            return f"Code Quality: Fix Pylint Warning in {file_name}"
            
    elif "Type Error" in title:
        # E.g. "Type Error: Incompatible argument type 'evidence' in tests/test_safety.py:341"
        # We can extract the core message from the title or body
        # Body starts with "Mypy reported: "
        if body.startswith("Mypy reported: "):
            msg = body.replace("Mypy reported: ", "").strip()
            # truncate message if too long
            if len(msg) > 60:
                msg = msg[:57] + "..."
            return f"Type Check: {msg} in {file_name}"
        else:
            title_core = title.split(" in ")[0].replace("Type Error: ", "")
            return f"Type Check: Fix {title_core} in {file_name}"

    elif "Security" in title:
        # E.g. "Security: Weak pseudo-random generator in agentwatch/tracing/sampling.py:86"
        title_core = title.split(" in ")[0].replace("Security: ", "")
        return f"Security: Resolve '{title_core}' in {file_name}"

    return title

def main():
    try:
        with open('my_issues_utf8.json', 'r', encoding='utf-8-sig') as f:
            issues = json.load(f)
    except Exception as e:
        print(f"Error loading issues: {e}")
        return

    # Filter target issues
    target_issues = [issue for issue in issues if 249 <= issue['number'] <= 316]
    
    print(f"Found {len(target_issues)} issues to update titles.")

    for i, issue in enumerate(target_issues, 1):
        num = issue['number']
        old_title = issue['title']
        body = issue['body']
        
        new_title = generate_better_title(old_title, body)
        
        # If new title is basically the same, skip or if it failed to parse nicely
        if new_title == old_title:
            continue
            
        print(f"[{i}/{len(target_issues)}] Updating #{num}")
        print(f"  Old: {old_title}")
        print(f"  New: {new_title}")
        
        cmd = [
            "gh", "issue", "edit", str(num),
            "--title", new_title
        ]
        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"  -> Success")
        except subprocess.CalledProcessError as e:
            print(f"  -> Failed. Error: {e.stderr}")
        
        time.sleep(2)

if __name__ == "__main__":
    main()
