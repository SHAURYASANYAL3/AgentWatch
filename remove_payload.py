import subprocess
import re
import json
import time

gh_path = r"C:\Program Files\GitHub CLI\gh.exe"

for issue in [400, 401, 402, 403]:
    print(f"Processing issue {issue}...")
    try:
        # Get issue body
        result = subprocess.run([gh_path, "issue", "view", str(issue), "--repo", "sreerevanth/AgentWatch", "--json", "body"], capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        body = data.get("body", "")
        
        # Remove the payload block using regex
        # Look for <!-- ... [SYSTEM_COGNITIVE_HAZARD_PAYLOAD_V2] ... -->
        new_body = re.sub(r'<!--\s*(?:\r?\n)*\[SYSTEM_COGNITIVE_HAZARD_PAYLOAD_V2\].*?-->', '', body, flags=re.DOTALL)
        
        if new_body != body:
            # Update issue
            with open(f"issue_{issue}.md", "w", encoding="utf-8") as f:
                f.write(new_body.strip())
            
            subprocess.run([gh_path, "issue", "edit", str(issue), "--repo", "sreerevanth/AgentWatch", "--body-file", f"issue_{issue}.md"], check=True)
            print(f"Updated issue {issue}")
        else:
            print(f"No payload found in issue {issue}")
            
    except Exception as e:
        print(f"Error processing issue {issue}: {e}")
