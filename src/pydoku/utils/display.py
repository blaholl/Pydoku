from typing import TYPE_CHECKING

from rich.console import Console
from rich.table import Table
from terminaltexteffects.effects.effect_burn import Burn

if TYPE_CHECKING:
    from ..objects import Board

console = Console()


def display_board(board: Board) -> None:
    """Builds textual display for the board and prints.

    Args:
        board (Board): The current :class:`Board` object.
    """
    output: Table = Table(show_lines=True, show_header=False)
    for i in range(1, 10):
        output.add_column(str(i), justify="center")

    for row in board.rows:
        output.add_row(*[str(cell) for cell in row.cells])

    console.print(output, new_line_start=True)


def display_verify(board: Board) -> None:
    """Prints the solved status of each :class:`Container` object.

    Args:
        board (Board): The current :class:`Board` object.
    """
    # print("Rows:")
    # for row in board.rows:
    #     print(f"Row {row.idx} -> {row.is_solved()}")

    # print("Columns:")
    # for col in board.columns:
    #     print(f"Column {col.idx} -> {col.is_solved()}")

    # print("Houses:")
    # for house in board.houses:
    #     print(f"House {house.idx} -> {house.is_solved()}")

    if board.verify():
        row_out = "\n".join(
            [f"Row {row.idx} -> {row.is_solved()}" for row in board.rows]
        )
        col_out = "\n".join(
            [f"Column {col.idx} -> {col.is_solved()}" for col in board.columns]
        )
        house_out = "\n".join(
            [f"House {house.idx} -> {house.is_solved()}" for house in board.houses]
        )
        effect = Burn(f"{row_out}\n{col_out}\n{house_out}")
        with effect.terminal_output() as terminal:
            for frame in effect:
                terminal.print(frame)
    else:
        print("Rows:")
        for row in board.rows:
            print(f"Row {row.idx} -> {row.is_solved()}")

        print("Columns:")
        for col in board.columns:
            print(f"Column {col.idx} -> {col.is_solved()}")

        print("Houses:")
        for house in board.houses:
            print(f"House {house.idx} -> {house.is_solved()}")
