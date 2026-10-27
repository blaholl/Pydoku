import itertools as it
import json
from collections.abc import ValuesView
from pathlib import Path
from typing import TYPE_CHECKING

import more_itertools as mi

from .exceptions import PuzzleNotFoundError

if TYPE_CHECKING:
    from ..objects import Board, Cell


def construct_cells() -> Board:
    all_cells = list(it.product(range(1, 10), repeat=2))

    a = (
        list(zip(*it.repeat(list(range(1, 4)), 3))) * 3
        + list(zip(*it.repeat(list(range(4, 7)), 3))) * 3
        + list(zip(*it.repeat(list(range(7, 10)), 3))) * 3
    )

    houses = ((r, c, h) for (r, c), h in list(zip(all_cells, mi.flatten(a))))

    return houses


def load_puzzle(
    file_path: Path, level: str, puzzle: int | None = None, all: bool = False
) -> list[int]:
    if not file_path.exists():
        raise PuzzleNotFoundError(f"Path `{file_path} does not exist.")

    with open(file_path, "r") as fp:
        if puzzle is not None:
            data: list[list[int]] = json.load(fp).get(level).get(str(puzzle))

            return list(mi.flatten(data))


def set_board(values: ValuesView[Cell], puzzle: list[int]) -> None:
    zipped = zip(values, puzzle)

    cell: Cell
    for cell, ans in zipped:
        if ans != 0:
            cell.solve(ans)
            cell.initial = True
