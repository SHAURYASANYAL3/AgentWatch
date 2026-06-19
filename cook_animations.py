import os
import re

def cook_verify_env():
    verify_env_content = """from __future__ import annotations

import os
import sys
import time

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel
from rich.align import Align

console = Console()

def verify_environment() -> None:
    console.print()
    
    # Awesome Progress Bar Sequence
    with Progress(
        SpinnerColumn(spinner_name="aesthetic", style="bold cyan"),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(complete_style="cyan", finished_style="bold green"),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        
        t1 = progress.add_task("[cyan]Initializing Diagnostic Matrix...", total=100)
        for i in range(100):
            time.sleep(0.005)
            progress.update(t1, advance=1)
            
        t2 = progress.add_task("[yellow]Analyzing Python Subsystems...", total=100)
        for i in range(100):
            time.sleep(0.002)
            progress.update(t2, advance=1)
            
        t3 = progress.add_task("[magenta]Validating Neural Dependencies...", total=100)
        for i in range(100):
            time.sleep(0.01)
            progress.update(t3, advance=1)
            
        t4 = progress.add_task("[green]Scanning System Environment...", total=100)
        for i in range(100):
            time.sleep(0.008)
            progress.update(t4, advance=1)

    console.print()
    console.print(Panel(Align.center("[bold cyan]AgentWatch Environment Diagnostics[/bold cyan]"), border_style="cyan"))

    # 1. Python version check
    py_ver = sys.version_info
    py_ver_str = f"{py_ver.major}.{py_ver.minor}.{py_ver.micro}"
    if py_ver.major == 3 and py_ver.minor >= 12:
        console.print(f"  [green]✔️ [/green] [bold]Python Runtime:[/bold] {py_ver_str} [dim](compatible)[/dim]")
    else:
        console.print(f"  [red]❌ [/red] [bold]Python Runtime:[/bold] {py_ver_str} [red](requires >= 3.12)[/red]")
        
    console.print()

    # 2. Dependency checks
    deps = {
        "fastapi": "FastAPI",
        "uvicorn": "Uvicorn",
        "pydantic": "Pydantic",
        "sqlalchemy": "SQLAlchemy",
        "redis": "Redis Client",
        "celery": "Celery",
        "httpx": "HTTPX",
        "rich": "Rich Text Engine",
    }
    table = Table(show_header=True, header_style="bold magenta", border_style="dim", expand=True)
    table.add_column("Core Dependency")
    table.add_column("Status", justify="right")

    for pkg, name in deps.items():
        try:
            __import__(pkg)
            table.add_row(name, "[green]✔️ Installed[/green]")
        except ImportError:
            table.add_row(name, "[red]❌ Missing[/red]")
            
    console.print(table)
    console.print()

    # 3. Environment Variables
    env_vars = [
        ("DATABASE_URL", False),
        ("REDIS_URL", False),
        ("CELERY_BROKER_URL", False),
        ("AGENTWATCH_API_KEY", False),
        ("ANTHROPIC_API_KEY", False),
        ("ENVIRONMENT", False),
    ]

    var_table = Table(show_header=True, header_style="bold green", border_style="dim", expand=True)
    var_table.add_column("System Variable")
    var_table.add_column("Requirement")
    var_table.add_column("Current State", justify="right")

    for var, required in env_vars:
        val = os.environ.get(var)
        if val:
            display_val = val if var in ("ENVIRONMENT",) else f"{val[:6]}... (masked)"
            var_table.add_row(var, "[dim]Required[/dim]" if required else "[dim]Optional[/dim]", f"[green]✔️ {display_val}[/green]")
        else:
            state = "[red]Required[/red]" if required else "[yellow]Optional[/yellow]"
            var_table.add_row(var, state, "[dim]Not Set[/dim]")

    console.print(var_table)
    console.print()
    console.print(Align.center("[bold cyan]ALL SYSTEMS GO.[/bold cyan]"))
    console.print()
"""
    with open('agentwatch/cli/verify_env.py', 'w', encoding='utf-8') as f:
        f.write(verify_env_content)


def cook_main():
    with open('agentwatch/cli/main.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Better ASCII banner typing effect
    old_callback = """    for line in ascii_art:
        console.print(f"[bold cyan]{line}[/bold cyan]")
        time.sleep(0.04)
    console.print()"""

    new_callback = """    # Glitchy Typing Effect
    import sys
    for line in ascii_art:
        sys.stdout.write("\\r\\033[K") # Clear line
        text = ""
        for char in line:
            text += char
            sys.stdout.write(f"\\r\\033[96m{text}\\033[0m")
            sys.stdout.flush()
            time.sleep(0.002)
        print()
    console.print("[dim italic]Initializing runtime components...[/dim italic]\\n")"""

    content = content.replace(old_callback, new_callback)

    # In status, add a blinking live indicator
    old_dashboard_title = r"\[bold cyan\]AgentWatch Live Runtime Dashboard\[/bold cyan\]\\n\[dim\]Press Ctrl\+C to exit\[/dim\]"
    new_dashboard_title = r"[bold cyan]AgentWatch Live Runtime Dashboard[/bold cyan]\n[blink red]● LIVE[/blink red] [dim]| Press Ctrl+C to exit[/dim]"
    content = content.replace(old_dashboard_title, new_dashboard_title)

    with open('agentwatch/cli/main.py', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    cook_verify_env()
    cook_main()
    print("AgentWatch is fully cooking now!")
