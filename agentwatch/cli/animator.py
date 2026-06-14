import sys
import time
import random
import os
import subprocess
from typing import List, Any
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.align import Align

console = Console()

CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*!?"

def speak_welcome() -> None:
    """Uses Windows speech synthesis in the background to say welcome."""
    try:
        user = os.getlogin()
    except Exception:
        user = "Commander"
        
    if sys.platform == "win32":
        cmd = f"Add-Type -AssemblyName System.speech; $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; $synth.Rate = 1; $synth.Speak('Welcome {user}, to Agent Watch.')"
        # Run in background so it talks while animating
        subprocess.Popen(["powershell", "-WindowStyle", "Hidden", "-Command", cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def cinematic_logo_reveal(ascii_art: List[str]) -> None:
    """A highly animated movie-style reveal for the ASCII logo."""
    # Start talking!
    speak_welcome()
    
    # Make space for the logo
    sys.stdout.write("\n" * len(ascii_art))
    
    # 1. Glitch Slide-in effect
    frames = 25
    for frame in range(frames):
        sys.stdout.write(f"\033[{len(ascii_art)}A") # Move up
        for i, line in enumerate(ascii_art):
            reveal_len = int((frame / frames) * len(line))
            visible = line[:reveal_len]
            
            # The leading edge has intense matrix characters
            edge = ""
            if reveal_len < len(line):
                edge = f"\033[92m{random.choice(CHARS)}\033[0m"
                
            sys.stdout.write(f"\r\033[K\033[96m{visible}\033[0m{edge}\n")
        sys.stdout.flush()
        time.sleep(0.03)
        
    # 2. Cinematic Flash (White -> Cyan)
    colors = ["\033[97m", "\033[1;96m", "\033[96m"]
    for c in colors:
        sys.stdout.write(f"\033[{len(ascii_art)}A")
        for line in ascii_art:
            sys.stdout.write(f"\r\033[K{c}{line}\033[0m\n")
        sys.stdout.flush()
        time.sleep(0.08)

def matrix_type_print(text: str, color: str = "96m", delay: float = 0.01) -> None:
    """Print text with a Matrix-style character decryption effect."""
    sys.stdout.write("\r\033[K")
    current_text = ""
    for char in text:
        if char.strip():
            # Show random character briefly
            sys.stdout.write(f"\r\033[{color}{current_text}\033[0m\033[92m{random.choice(CHARS)}\033[0m")
            sys.stdout.flush()
            time.sleep(0.005)
        current_text += char
        sys.stdout.write(f"\r\033[{color}{current_text}\033[0m")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def animate_table_rows(table: Table, rows: List[List[Any]], delay: float = 0.05) -> None:
    """Animate adding rows to a rich Table."""
    with Live(table, console=console, refresh_per_second=20) as live:
        for row in rows:
            time.sleep(delay)
            table.add_row(*row)
            live.update(table)

def glitch_ascii_art(ascii_art: List[str]) -> None:
    """Legacy glitch function, kept for backward compat."""
    cinematic_logo_reveal(ascii_art)

def print_systematic_menu() -> None:
    """Prints a beautiful, animated systematic command menu."""
    table = Table(show_edge=False, show_header=False, box=None, padding=(1, 4))
    table.add_column("Command", style="bold cyan")
    table.add_column("Description", style="dim")
    
    commands = [
        ("🚀 [bold]check-env[/bold]", "Run full system diagnostic & dependency check"),
        ("🖥️  [bold]server start[/bold]", "Boot the local AgentWatch API server"),
        ("📊 [bold]server status[/bold]", "Open the real-time live performance dashboard"),
        ("👀 [bold]session watch[/bold]", "Watch a Claude Code execution with full safety"),
        ("⏪ [bold]session replay[/bold]", "Replay a captured session step-by-step"),
        ("📋 [bold]session list[/bold]", "List recent agent sessions from the API"),
        ("🛡️  [bold]safety check[/bold]", "Score the risk level of a shell command"),
    ]
    
    for cmd, desc in commands:
        table.add_row(cmd, desc)
        
    panel = Panel(
        table,
        title="[bold green]S Y S T E M   C O M M A N D S[/bold green]",
        border_style="cyan",
        expand=False
    )
    
    console.print()
    # A short delay before the menu pops up for cinematic pacing
    time.sleep(0.2)
    console.print(Align.center(panel))
    console.print()
