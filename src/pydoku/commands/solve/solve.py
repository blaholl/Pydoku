from enum import StrEnum
from pathlib import Path

import click

from pydoku.solver import Solver


class Level(StrEnum):
    BEGINNER = "beginner"
    ADVANCED = "advanced"
    EXPERT = "expert"
    PRO = "pro"
    IMPOSSIBLE = "impossible"
    EXTENDED = "extended"


PUZZLES: Path = Path("./tests/data/puzzles.json")


@click.command()
@click.option("-l", "--level", type=click.Choice(Level, case_sensitive=False))
@click.option("-p", "--puzzle", type=click.INT)
def solve(level: Level, puzzle: int) -> list[list[int]]:
    solver: Solver = Solver.open(PUZZLES, level, puzzle)
    board = solver.board
    solver.solve()

    click.echo(board.show())
