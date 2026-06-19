import json

with open("bandit_report.json", encoding="utf-8") as f:
    d = json.load(f)

for r in d.get("results", []):
    print(f"{r['filename']}:{r['line_number']} - {r['issue_text']} ({r['issue_severity']} severity)")
