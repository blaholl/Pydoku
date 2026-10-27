from typing import TYPE_CHECKING

from rich.console import Console
from rich.table import Table

if TYPE_CHECKING:
    from ..objects import Board

console = Console()


def display_board(board: Board) -> Table:
    """Builds textual display for the board

    Returns
        Table: :class:`rich.Table` representation of the :class:`Board`.
    """
    output: Table = Table(show_lines=True, show_header=False)
    for i in range(1, 10):
        output.add_column(str(i), justify="center")

    for row in board.rows:
        output.add_row(
            str(row[1]),
            str(row[2]),
            str(row[3]),
            str(row[4]),
            str(row[5]),
            str(row[6]),
            str(row[7]),
            str(row[8]),
            str(row[9]),
        )

    console.print(output)
