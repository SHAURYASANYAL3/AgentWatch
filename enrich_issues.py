import json
import subprocess
import time
import re

def enrich_body(title, original_body):
    if "Security:" in title:
        match = re.search(r"in ([\w/._-]+):(\d+)", title)
        file_path = match.group(1) if match else "Unknown"
        line_num = match.group(2) if match else "Unknown"
        
        return f"""### 🛡️ Security Vulnerability Detected

**File:** `{file_path}`
**Line:** `{line_num}`

#### Description
During our automated security sweep (via Bandit), we detected a potential security issue in the codebase. 
{original_body}

#### Impact
Security issues, even low severity ones, can accumulate and create blind spots in our infrastructure or expose our agents to unintended risks (e.g. untrusted inputs, weak RNG, unauthorized bindings).

#### Proposed Solution
1. Review the affected code block to understand the context.
2. If it is a false positive, add the appropriate `# nosec` comment with a justification.
3. Otherwise, refactor the code to use secure alternatives (e.g. `secrets` module instead of `random`, safe subprocess calls, explicitly binding to localhost).

#### Steps to Verify
Run `bandit -r .` after applying your changes to ensure the issue is resolved.
"""

    elif "Type Error:" in title:
        match = re.search(r"in ([\w/._-]+):(\d+)", title)
        file_path = match.group(1) if match else "Unknown"
        line_num = match.group(2) if match else "Unknown"
        
        return f"""### 🏷️ Static Type Checking Error

**File:** `{file_path}`
**Line:** `{line_num}`

#### Description
Our static type checker (`mypy`) reported a type inconsistency.
{original_body}

#### Impact
Type hinting errors defeat the purpose of our static analysis tools and can hide runtime bugs (such as `AttributeError` or `TypeError`). A strongly typed codebase is essential for maintaining a reliable orchestration engine.

#### Proposed Solution
1. Inspect the variable assignments, function arguments, or return types at the specified line.
2. Provide the correct explicit type annotations (e.g. `list[str]`, `Optional[int]`, `Any` if strictly necessary).
3. Ensure that upstream dependencies and downstream consumers agree on the data shapes.

#### Steps to Verify
Run `mypy {file_path}` after applying your changes to verify the error is cleared.
"""

    elif "Pylint" in title:
        match = re.search(r"in ([\w/._-]+):(\d+)", title)
        file_path = match.group(1) if match else "Unknown"
        line_num = match.group(2) if match else "Unknown"
        
        return f"""### 🧹 Linter Warning (Code Smell)

**File:** `{file_path}`
**Line:** `{line_num}`

#### Description
Our linter (`pylint`) flagged this section of the code for violating standard conventions or exhibiting a code smell.
{original_body}

#### Impact
While this may not cause an immediate runtime crash, accumulating linter warnings degrades code quality, readability, and maintainability over time. Things like broad exception catching or unused arguments can mask logic errors.

#### Proposed Solution
1. Review the flagged warning.
2. If it's an unused variable, remove it (or prefix with `_` if required by an interface).
3. If it's a broad exception, narrow it down to the specific exception class expected.
4. If it's a protected member access, consider adding a public accessor method.

#### Steps to Verify
Run `pylint {file_path}` to confirm the warning has been resolved.
"""
    return original_body

def main():
    try:
        with open('my_issues_utf8.json', 'r', encoding='utf-8-sig') as f:
            issues = json.load(f)
    except Exception as e:
        print(f"Error loading issues: {e}")
        return

    # Filter out issues that might not be ours or are already enriched (just in case)
    # We will target issues > 248 because we created 249 to 316
    target_issues = [issue for issue in issues if issue['number'] >= 249 and issue['number'] <= 316]
    
    print(f"Found {len(target_issues)} issues to enrich.")

    for i, issue in enumerate(target_issues, 1):
        num = issue['number']
        title = issue['title']
        old_body = issue['body']
        
        new_body = enrich_body(title, old_body)
        
        print(f"[{i}/{len(target_issues)}] Enriching Issue #{num}: {title}")
        
        cmd = [
            "gh", "issue", "edit", str(num),
            "--body", new_body
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"  -> Success: Updated #{num}")
        except subprocess.CalledProcessError as e:
            print(f"  -> Failed to update #{num}. Error: {e.stderr}")
        
        time.sleep(2)

    print("Done enriching all issues!")

if __name__ == "__main__":
    main()
