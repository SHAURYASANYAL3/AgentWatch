import json
import subprocess
import time
import re

def main():
    try:
        with open('my_issues_utf8.json', 'r', encoding='utf-8-sig') as f:
            issues = json.load(f)
    except Exception as e:
        print(f"Error loading issues: {e}")
        return

    # Filter target issues (the ones we created recently)
    target_issues = [issue for issue in issues if 249 <= issue['number'] <= 316]
    
    # Separate Type Error issues
    type_issues = [issue for issue in target_issues if "Type Error" in issue['title'] or "Mypy" in issue['title']]
    
    print(f"Found {len(type_issues)} type checking issues to consolidate.")
    
    if not type_issues:
        print("No type checking issues found.")
        return

    # Create the body for the master issue
    master_body = "### 🏷️ Consolidated Static Type Checking Errors\n\n"
    master_body += "We are tracking all `mypy` type inconsistencies here to avoid issue tracker clutter. Please check off items as they are resolved in PRs.\n\n"
    
    # Sort by title (which typically contains the file name at the end)
    type_issues_sorted = sorted(type_issues, key=lambda x: x['title'])
    
    for issue in type_issues_sorted:
        body = issue['body']
        title = issue['title']
        
        # Original titles look like: "Type Error: Incompatible argument type 'evidence' in tests/test_safety.py:341"
        # Original bodies start with: "Mypy reported: Argument 'evidence' to 'StepAudit' has incompatible type 'dict[Never, Never]'; expected 'list[str]'"
        
        file_match = re.search(r"in ([\w/._-]+):(\d+)", title)
        if not file_match:
            file_match = re.search(r"in ([\w/._-]+)$", title)
            
        fpath = file_match.group(1) if file_match else "unknown_file"
        line = file_match.group(2) if file_match and len(file_match.groups()) > 1 else "?"
        
        msg = body.replace("Mypy reported: ", "").strip()
        
        master_body += f"- [ ] **{fpath}:{line}** - {msg}\n"

    # Create the master issue
    print("Creating Master Issue...")
    cmd_create = [
        "gh", "issue", "create", 
        "--title", "Tracking: Consolidated Static Type Checking (Mypy) Errors", 
        "--body", master_body
    ]
    try:
        result = subprocess.run(cmd_create, capture_output=True, text=True, check=True)
        new_issue_url = result.stdout.strip()
        new_issue_num = new_issue_url.split('/')[-1]
        print(f"  -> Success: Created Master Issue #{new_issue_num}")
    except subprocess.CalledProcessError as e:
        print(f"  -> Failed to create Master Issue. Error: {e.stderr}")
        return

    # Close the individual issues
    print(f"Closing {len(type_issues)} individual type checking issues...")
    for i, issue in enumerate(type_issues, 1):
        num = issue['number']
        print(f"[{i}/{len(type_issues)}] Closing #{num}")
        cmd_close = [
            "gh", "issue", "close", str(num), 
            "-c", f"Consolidated into master tracking issue #{new_issue_num}"
        ]
        try:
            subprocess.run(cmd_close, capture_output=True, text=True, check=True)
            print(f"  -> Success")
        except subprocess.CalledProcessError as e:
            print(f"  -> Failed. Error: {e.stderr}")
        
        time.sleep(1)

if __name__ == "__main__":
    main()
