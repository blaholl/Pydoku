from enum import StrEnum
from pathlib import Path

import click

from pydoku.solver import Solver

from ...utils.logger import logger


class Level(StrEnum):
    BEGINNER = "beginner"
    ADVANCED = "advanced"
    EXPERT = "expert"
    PRO = "pro"
    IMPOSSIBLE = "impossible"
    EXTENDED = "extended"


class LogLevel(StrEnum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


PUZZLES: Path = Path("./tests/data/puzzles.json")
CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


@click.command(context_settings=CONTEXT_SETTINGS)
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
    show_default=True,
)
@click.option(
    "-v",
    "--print-verify",
    is_flag=True,
    default=False,
    help="Flag to display container-level verification at end of run.",
)
@click.option(
    "--log-level",
    default=LogLevel.INFO,
    type=click.Choice(LogLevel, case_sensitive=False),
    show_default=True,
    help="Log level.",
)
def solve(
    level: Level, puzzle: int, rounds: int, log_level: str, print_verify: bool
) -> list[list[int]]:
    """

    \b
     _____  __   __ ______   _____  _     _ _     _
    |_____]   \_/   |     \ |     | |____/  |     |
    |          |    |_____/ |_____| |    \_ |_____|
    """  # noqa: W605
    logger.setLevel(log_level.upper())
    solver: Solver = Solver.open(PUZZLES, level, puzzle)
    board = solver.board
    solver.solve(rounds)

    board.show(print_verify=print_verify)
