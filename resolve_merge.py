import re

def resolve():
    with open('agentwatch/cli/main.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1st conflict
    content = content.replace('<<<<<<< HEAD\nimport time\n=======\nfrom enum import Enum\n>>>>>>> main\n', 'import time\nfrom enum import Enum\n')

    # 2nd conflict (keep HEAD)
    match = re.search(r'<<<<<<< HEAD\n(@server_app\.command\(name=\"status\"\)[\s\S]*?)=======\n[\s\S]*?>>>>>>> main\n', content)
    if match:
        content = content.replace(match.group(0), match.group(1))

    with open('agentwatch/cli/main.py', 'w', encoding='utf-8') as f:
        f.write(content)

resolve()
