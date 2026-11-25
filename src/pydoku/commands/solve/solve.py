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
@click.option(
    "-l",
    "--level",
    type=click.Choice(Level, case_sensitive=False),
    help="Level of the puzzle to retrieve.",
)
@click.option(
    "-p",
    "--puzzle",
    type=click.INT,
    help="Number of the puzzle to retrieve under each level's top-level key.",
)
@click.option(
    "-r",
    "--rounds",
    type=click.INT,
    default=3,
    help="Number of rounds to run the parser.",
)
def solve(level: Level, puzzle: int, rounds: int) -> list[list[int]]:
    solver: Solver = Solver.open(PUZZLES, level, puzzle)
    board = solver.board
    res = solver.solve(rounds)

    click.echo(res)
    click.echo(board.show())
