import json
import subprocess
import time

try:
    with open('pylint_report.json', encoding='utf-16') as f:
        data = json.load(f)
except Exception as e:
    print(f"Error reading pylint report: {e}")
    exit(1)

# Filter for warnings and errors to make sure they are meaningful (skip simple conventions)
meaningful_issues = [d for d in data if d.get('type') in ['warning', 'error']]

# Take up to 30 issues
issues_to_push = meaningful_issues[:30]

print(f"Found {len(meaningful_issues)} meaningful pylint warnings/errors. Pushing {len(issues_to_push)} issues to GitHub...")

for i, issue in enumerate(issues_to_push, 1):
    title = f"Pylint {issue['type'].capitalize()}: {issue['message-id']} in {issue['path']}:{issue['line']}"
    # Truncate title if it's too long
    if len(title) > 100:
        title = title[:97] + "..."
        
    body = f"**Pylint reported a {issue['type']} ({issue['message-id']})**\n\n"
    body += f"- **File**: `{issue['path']}`\n"
    body += f"- **Line**: {issue['line']}\n"
    body += f"- **Message**: {issue['message']}\n"
    
    print(f"[{i}/{len(issues_to_push)}] Creating: {title}")
    
    cmd = [
        "gh", "issue", "create",
        "--title", title,
        "--body", body
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"Success: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create issue. Error: {e.stderr}")
    
    time.sleep(2)

print("Done creating additional issues!")
