import re

def refactor_cli():
    with open('agentwatch/cli/main.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update completion
    content = content.replace("add_completion=False,", "add_completion=True,")

    # 2. Add Typer groups below console = Console()
    typer_groups = """console = Console()

session_app = typer.Typer(name="session", help="Manage and inspect agent sessions")
server_app = typer.Typer(name="server", help="Manage the AgentWatch API server")
safety_app = typer.Typer(name="safety", help="Safety and risk analysis tools")

app.add_typer(session_app)
app.add_typer(server_app)
app.add_typer(safety_app)
"""
    content = content.replace("console = Console()\n", typer_groups)

    # 3. Update decorators
    content = content.replace("@app.command()\ndef watch(", "@session_app.command(name=\"watch\")\ndef watch(")
    content = content.replace("@app.command()\ndef replay(", "@session_app.command(name=\"replay\")\ndef replay(")
    content = content.replace("@app.command()\ndef sessions(", "@session_app.command(name=\"list\")\ndef sessions(")
    content = content.replace("@app.command()\ndef confidence(", "@session_app.command(name=\"score\")\ndef confidence(")
    content = content.replace("@app.command()\ndef safety(", "@safety_app.command(name=\"check\")\ndef safety(")
    content = content.replace("@app.command()\ndef serve(", "@server_app.command(name=\"start\")\ndef serve(")
    content = content.replace("@app.command(name=\"verify-env\")\ndef verify_env()", "@app.command(name=\"check-env\")\ndef verify_env()")

    # 4. Replace the status command with a Live dashboard
    # Find the status command block
    old_status_regex = r"@app\.command\(\)\ndef status\(.*?\n    asyncio\.run\(_run\(\)\)"
    
    new_status_cmd = """@server_app.command(name="status")
def status(
    api_url: str = typer.Option("http://localhost:8000", "--api"),
    refresh_rate: float = typer.Option(1.0, "--refresh", help="Refresh rate in seconds")
) -> None:
    \"\"\"[bold]Show[/bold] a real-time live dashboard of AgentWatch runtime status.\"\"\"

    async def _run() -> None:
        try:
            import httpx
            from rich.live import Live
            from rich.layout import Layout
            from rich.align import Align
        except ImportError:
            console.print("[red]Missing dependencies. Run: pip install httpx rich[/red]")
            raise typer.Exit(1)

        def generate_dashboard(data, error_msg=None):
            if error_msg:
                return Panel(f"[red]{error_msg}[/red]", title="AgentWatch Error", border_style="red")
            
            # Create sub-panels
            active = data.get('active_sessions', 0)
            failed = data.get('failed_sessions', 0)
            blocked = data.get('blocked_sessions', 0)
            
            activity = Table.grid(padding=(0, 2))
            activity.add_row("Active Sessions:", f"[green]{active}[/green]")
            activity.add_row("Failed Sessions:", f"[red]{failed}[/red]")
            activity.add_row("Blocked Sessions:", f"[yellow]{blocked}[/yellow]")
            p1 = Panel(activity, title="[cyan]Agent Activity[/cyan]", border_style="cyan")

            tokens = data.get('total_tokens', 0)
            cost = data.get('estimated_cost_usd', 0.0)
            
            resources = Table.grid(padding=(0, 2))
            resources.add_row("Total Tokens:", f"[bold]{tokens:,}[/bold]")
            resources.add_row("Est. Cost:", f"[green]${cost:.4f}[/green]")
            p2 = Panel(resources, title="[magenta]Resource Utilization[/magenta]", border_style="magenta")

            safety_stats = data.get("safety_stats", {})
            eb_stats = data.get("event_bus_stats", {})
            
            pipeline = Table.grid(padding=(0, 2))
            pipeline.add_row("Blocked Ops:", f"[red]{safety_stats.get('blocked', 0)}[/red]")
            pipeline.add_row("Event T-Put:", f"{eb_stats.get('total_published', 0):,} processed")
            pipeline.add_row("Subscribers:", f"{eb_stats.get('active_subscribers', 0)}")
            p3 = Panel(pipeline, title="[yellow]Safety & Event Pipeline[/yellow]", border_style="yellow")

            layout = Layout()
            layout.split_column(
                Layout(Panel("[bold cyan]AgentWatch Live Runtime Dashboard[/bold cyan]\\n[dim]Press Ctrl+C to exit[/dim]", justify="center"), size=4),
                Layout(name="body")
            )
            layout["body"].split_row(
                Layout(p1),
                Layout(p2),
                Layout(p3)
            )
            return layout

        async with httpx.AsyncClient() as client:
            with Live(generate_dashboard({}), refresh_per_second=1/refresh_rate, console=console) as live:
                while True:
                    try:
                        resp = await client.get(
                            f"{api_url}/api/v1/dashboard/summary",
                            timeout=2.0,
                        )
                        resp.raise_for_status()
                        live.update(generate_dashboard(resp.json()))
                    except Exception as exc:
                        live.update(generate_dashboard({}, str(exc)))
                    await asyncio.sleep(refresh_rate)

    try:
        asyncio.run(_run())
    except KeyboardInterrupt:
        console.print("[dim]Exited status dashboard.[/dim]")
"""
    
    content = re.sub(old_status_regex, new_status_cmd, content, flags=re.DOTALL)

    with open('agentwatch/cli/main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Refactoring complete.")

if __name__ == "__main__":
    refactor_cli()
