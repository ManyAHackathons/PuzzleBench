from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich import print as rprint
from rich.table import Table
from bomb.module import Module
from bomb.bomb import Bomb
from rich.align import Align

console = Console()

def print_panel(role, content, model: str = ""):
    text = content or ""
    label = f"({model}) " if model else ""
    if role == "defuser":
        console.print(Panel(text, title=f"[bold red]{label}DEFUSER[/bold red]", border_style="red"))
    else:
        console.print(Panel(text, title=f"[bold blue]{label}TECHNICIAN[/bold blue]", border_style="blue"))

def print_bomb(bomb):
    table = Table(title="BOMB", border_style="yellow", show_lines=True)
    table.add_column("ID", style="dim", width=4)
    table.add_column("Module", width=16)
    table.add_column("Status", width=10)

    for i, module in enumerate(bomb.get_modules()):
        status = "[green]DEFUSED ✓[/green]" if module.is_defused() else "[red]ACTIVE ●[/red]"
        table.add_row(str(i), module.getName(), status)

    console.print(table)

def print_start():
    centered_content = Align.center("[bold green]BOMB DEFUSAL INITIATED[/bold green]", vertical="middle")
    console.print(Panel(centered_content, border_style="green"))

def print_win():
    console.print(Align.center(Panel("[bold gold]BOMB DEFUSED! CONGRATULATIONS![/bold gold]", border_style="white")))

def print_loss():
    console.print(Panel("[bold red]TIME RAN OUT! THE BOMB EXPLODED![/bold red]", border_style="red"))

def print_turn(n: int):
    console.rule(f"[dim]Turn {n}[/dim]")

