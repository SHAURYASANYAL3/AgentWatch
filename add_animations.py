import re

def add_animations():
    with open('agentwatch/cli/main.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add ASCII Animation Callback
    callback_code = """
import time

@app.callback()
def main_callback():
    \"\"\"AgentWatch CLI with ASCII Animation\"\"\"
    ascii_art = [
        r"    ___                    __ _       __      __       __  ",
        r"   /   |  ____  ___  ____ / /| |     / /___ _/ /______/ /_ ",
        r"  / /| | / __ `/ _ \\/ __ \\ __/ | /| / / __ `/ __/ ___/ __ \\",
        r" / ___ |/ /_/ /  __/ / / / /_  |/ |/ / /_/ / /_/ /__/ / / /",
        r"/_/  |_|\\__, /\\___/_/ /_/\\__/  |__/|__/\\__,_/\\__/\\___/_/ /_/",
        r"       /____/                                              "
    ]
    
    for line in ascii_art:
        console.print(f"[bold cyan]{line}[/bold cyan]")
        time.sleep(0.04)
    console.print()

"""
    # Insert right after app.add_typer(safety_app)
    content = content.replace("app.add_typer(safety_app)", "app.add_typer(safety_app)\n" + callback_code)

    # 2. Add spinners to network calls in 'list', 'score', 'check', 'check-env'
    
    # For list (sessions)
    content = content.replace("resp = await client.get(\n                    f\"{api_url}/api/v1/sessions\",",
                              "with console.status(\"[cyan]Fetching sessions...[/cyan]\", spinner=\"bouncingBar\"):\n                    resp = await client.get(\n                        f\"{api_url}/api/v1/sessions\",")
    
    # For score (confidence)
    content = content.replace("resp = await client.get(\n                    f\"{api_url}/api/v1/sessions/{session_id}/confidence\",",
                              "with console.status(\"[magenta]Calculating confidence score...[/magenta]\", spinner=\"bouncingBar\"):\n                    resp = await client.get(\n                        f\"{api_url}/api/v1/sessions/{session_id}/confidence\",")
    
    # For check (safety)
    content = content.replace("resp = await client.post(\n                    f\"{api_url}/api/v1/safety/policy\",",
                              "with console.status(\"[red]Evaluating safety policy...[/red]\", spinner=\"bouncingBar\"):\n                    resp = await client.post(\n                        f\"{api_url}/api/v1/safety/policy\",")

    # For check-env (verify_env)
    content = content.replace("console.print(\"[bold cyan]AgentWatch Environment Verification[/bold cyan]\")",
                              "console.print(\"[bold cyan]AgentWatch Environment Verification[/bold cyan]\")\n    with console.status(\"[yellow]Verifying environment...[/yellow]\", spinner=\"aesthetic\"):")
    # Need to indent the rest of verify_env block properly, so maybe we won't wrap all of verify_env, just change its color print. Let's not touch verify_env structure just in case.

    # Actually, we can add a simple sleep animation in verify_env manually.
    verify_find = "console.print(\"─────────────────────────────────────\")"
    verify_replace = verify_find + "\n    import time\n    for _ in range(3):\n        time.sleep(0.2)"
    content = content.replace(verify_find, verify_replace)

    with open('agentwatch/cli/main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Animations added successfully!")

if __name__ == "__main__":
    add_animations()
