import sys
import time
import random
from typing import List, Any
from rich.console import Console
from rich.table import Table
from rich.live import Live

console = Console()

CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*!?"

def matrix_type_print(text: str, color: str = "96m", delay: float = 0.01) -> None:
    """Print text with a Matrix-style character decryption effect."""
    for char in text:
        if char.strip():
            # Show random character briefly
            sys.stdout.write(f"\033[92m{random.choice(CHARS)}\033[0m")
            sys.stdout.flush()
            time.sleep(0.005)
            sys.stdout.write("\b") # backspace
        sys.stdout.write(f"\033[{color}{char}\033[0m")
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
    """Print ASCII art with a cool left-to-right matrix glitch effect."""
    for line in ascii_art:
        sys.stdout.write("\r\033[K")
        text = ""
        for char in line:
            if char.strip():
                sys.stdout.write(f"\r\033[92m{text}{random.choice(CHARS)}\033[0m")
                sys.stdout.flush()
                time.sleep(0.001)
            text += char
            sys.stdout.write(f"\r\033[96m{text}\033[0m")
            sys.stdout.flush()
            time.sleep(0.001)
        print()
