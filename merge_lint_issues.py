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
    
    # Separate Pylint issues
    lint_issues = [issue for issue in target_issues if "Pylint" in issue['title'] or "Pylint" in issue['body']]
    
    print(f"Found {len(lint_issues)} lint issues to consolidate.")
    
    if not lint_issues:
        print("No lint issues found.")
        return

    # Create the body for the master issue
    master_body = "### 🧹 Consolidated Code Quality & Linting Issues\n\n"
    master_body += "We are tracking all Pylint warnings here to avoid issue tracker clutter. Please check off items as they are resolved in PRs.\n\n"
    
    # Sort by file path
    lint_issues_sorted = sorted(lint_issues, key=lambda x: x['title'])
    
    for issue in lint_issues_sorted:
        body = issue['body']
        title = issue['title']
        
        # Try to parse the original body
        msg_match = re.search(r"- \*\*Message\*\*: (.*)", body)
        file_match = re.search(r"- \*\*File\*\*: `(.*?)`", body)
        line_match = re.search(r"- \*\*Line\*\*: (.*)", body)
        
        if msg_match and file_match and line_match:
            msg = msg_match.group(1).strip()
            fpath = file_match.group(1).strip()
            line = line_match.group(1).strip()
            master_body += f"- [ ] **{fpath}:{line}** - {msg}\n"
        else:
            master_body += f"- [ ] {title}\n"

    # Create the master issue
    print("Creating Master Issue...")
    cmd_create = [
        "gh", "issue", "create", 
        "--title", "Tracking: Consolidated Code Quality & Pylint Warnings", 
        "--body", master_body
    ]
    try:
        result = subprocess.run(cmd_create, capture_output=True, text=True, check=True)
        # The output of gh issue create is the URL of the new issue, e.g. https://github.com/user/repo/issues/123
        new_issue_url = result.stdout.strip()
        new_issue_num = new_issue_url.split('/')[-1]
        print(f"  -> Success: Created Master Issue #{new_issue_num}")
    except subprocess.CalledProcessError as e:
        print(f"  -> Failed to create Master Issue. Error: {e.stderr}")
        return

    # Close the individual issues
    print(f"Closing {len(lint_issues)} individual lint issues...")
    for i, issue in enumerate(lint_issues, 1):
        num = issue['number']
        print(f"[{i}/{len(lint_issues)}] Closing #{num}")
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
