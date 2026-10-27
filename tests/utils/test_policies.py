import itertools as it
from pathlib import Path

import pytest

from pydoku.objects import Board
from pydoku.utils.policies import Policy


@pytest.fixture
def get_board_from_file() -> Board:
    file_path: Path = Path("./tests/data/puzzles.json")
    level = "beginner"
    puz = 2

    board: Board = Board.from_puzzle(puzzle_path=file_path, level=level, num=puz)
    board.populate()
    return board


def test_hidden_single_policy(get_board_from_file: Board) -> None:
    board: Board = get_board_from_file

    container = board.rows[1]
    counts = container.get_counts()

    products = list(it.product(counts.items(), container.open))

    c, cell = products[0]

    assert Policy.is_not_hidden_single(c[0], c[1], cell, container.known) is True

    c, cell = products[5]

    assert Policy.is_not_hidden_single(c[0], c[1], cell, container.known) is False
