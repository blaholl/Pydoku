import json
from pathlib import Path

import click

from . import add_puzzle as ap

TEST_PUZZLES: str = "./tests/data/test-puzzles.json"
CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument(
    "filepath",
    type=click.Path(exists=True),
    default=TEST_PUZZLES,
    help="Path of the file to import.",
)
@click.option(
    "-l",
    "--level",
    type=click.STRING,
    required=False,
    help="Top-level key to which to add the puzzle. Should be snake_case.",
)
@click.option(
    "-n",
    "--new",
    type=click.STRING,
    required=False,
    help="Creates a new top-level key. Should be snake_case.",
)
def add(filepath: str, level: str, new: str) -> None:
    """

    \b
     _____  __   __ ______   _____  _     _ _     _
    |_____]   \_/   |     \ |     | |____/  |     |
    |          |    |_____/ |_____| |    \_ |_____|
    """  # noqa: W605
    while True:
        set_input_and_file(filepath, level, new)


def set_input_and_file(
    filepath: str, level: str | None = None, new: str | None = None
) -> None:
    all_rows: list[list[int]] = []
    for i in range(1, 10):
        row = ap.input_row(i)
        all_rows.append(row)

    puzzles = open_file(filename=filepath)
    key: str = get_key(puzzles, level, new)
    if new:
        level = new

    puzzles[level][key] = all_rows

    set_file(filepath, puzzles)

    click.echo(f"Puzzle {key} added to {level}.")


def open_file(filename: Path) -> dict[int, list[list[int]]]:
    with open(filename, "r") as fh:
        puzzles = json.load(fh)

    return puzzles


def set_file(filename: Path, data: dict) -> None:
    with open(filename, "w") as fh:
        json.dump(data, fh, indent=2)


def get_key(
    puzzles: dict[str, list[list[int]]],
    level: str | None = None,
    new: str | None = None,
) -> str:
    if new:
        puzzles[new] = {}
        return "1"

    keys = puzzles.get(level).keys()
    if not keys:
        return "1"

    sorted_keys = sorted([int(i) for i in keys])
    return str(max(sorted_keys) + 1)
