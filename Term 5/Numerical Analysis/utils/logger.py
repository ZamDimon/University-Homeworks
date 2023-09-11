from rich import print
from rich.panel import Panel
from rich.table import Table
import typing
from typing import Any

def print_list_rich(arr: list[Any], term_prefix="") -> None:
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_column(justify="right")
    for i, term in enumerate(arr):
        grid.add_row(f"{term_prefix} #{i}:", f"{term}")
    print(grid)

def print_list_rich_with_result(arr: list[Any], result: str, term_prefix="") -> None:
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_column(justify="right")
    for i, term in enumerate(arr):
        grid.add_row(f"{term_prefix} #{i}:", f"{term}")
    grid.add_row("[b]Result:", f"{result}")
    grid.add_row()
    print(grid)

def print_panel(title: str) -> None:
    print(Panel(f"[blue]{title}"))
