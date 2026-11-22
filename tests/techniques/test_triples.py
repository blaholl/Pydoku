# import itertools as it
from pathlib import Path

import pytest

from pydoku.objects import Board

# from pydoku.utils.policies import Policy


@pytest.fixture
def get_board_from_file() -> Board:
    file_path: Path = Path("./tests/data/test-puzzles.json")
    level = "naked_triple"
    puz = 1

    board: Board = Board.from_puzzle(puzzle_path=file_path, level=level, num=puz)
    board.populate()
    return board


def test_naked_triple(get_board_from_file: Board) -> None:
    board: Board = get_board_from_file
    board.populate()

    assert 2 in board.cells[5]
    assert 2 in board.cells[14]

    result = board.check_naked_triple()

    assert result is True
    assert 2 not in board.cells[5]
    assert 2 not in board.cells[14]
