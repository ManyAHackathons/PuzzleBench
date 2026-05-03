from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from bomb.bomb import Bomb

console = Console()

def print_panel(role: str, content: str, model: str = ""):
    text = content or ""
    label = f"({model}) " if model else ""

    if role == "defuser":
        console.print(Panel(text, title=f"[bold red]{label}DEFUSER[/bold red]", border_style="red"))
    elif role == "defuser_tool":
        console.print(Panel(text, title=f"[bold yellow]DEFUSER TOOL CALL[/bold yellow]", border_style="yellow"))
    elif role == "defuser_sees":
        console.print(Panel(text, title=f"[bold yellow]DEFUSER SEES[/bold yellow]", border_style="dark_orange"))

    elif role == "technician":
        console.print(Panel(text, title=f"[bold blue]{label}TECHNICIAN[/bold blue]", border_style="blue"))
    elif role == "technician_tool":
        console.print(Panel(text, title=f"[bold cyan]TECHNICIAN TOOL CALL[/bold cyan]", border_style="cyan"))
    elif role == "technician_sees":
        console.print(Panel(text, title=f"[bold cyan]TECHNICIAN SEES[/bold cyan]", border_style="bright_cyan"))

    else:
        console.print(Panel(text, title=f"[bold dim]{role}[/bold dim]", border_style="dim"))

def print_bomb(bomb: Bomb):
    table = Table(title="BOMB", border_style="yellow", show_lines=True)
    table.add_column("ID", style="dim", width=4)
    table.add_column("Module", width=16)
    table.add_column("Status", width=10)

    for i, module in enumerate(bomb.get_modules()):
        status = "[green]DEFUSED ✓[/green]" if module.is_defused() else "[red]ACTIVE ●[/red]"
        table.add_row(str(i), module.getName(), status)

    console.print(table)

def print_start():
    console.print(Panel(Align.center("[bold green]BOMB DEFUSAL INITIATED[/bold green]", vertical="middle"), border_style="green"))

def print_win():
    console.print(Align.center(Panel("[bold gold]BOMB DEFUSED! CONGRATULATIONS![/bold gold]", border_style="white")))

def print_loss():
    console.print(Panel("[bold red]TIME RAN OUT! THE BOMB EXPLODED![/bold red]", border_style="red"))

def print_turn(n: int):
    console.rule(f"[dim]Turn {n}[/dim]")