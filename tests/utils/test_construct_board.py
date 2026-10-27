from pathlib import Path

import pytest

from pydoku.objects import Board
from pydoku.utils.construct_board import load_puzzle, set_board
from pydoku.utils.exceptions import PuzzleNotFoundError


@pytest.fixture
def get_cells() -> Board:
    board = Board()
    return board


@pytest.fixture
def get_puzzle() -> list[int]:
    file_path: Path = Path("./tests/data/puzzles.json")
    level = "beginner"
    puz = 1

    return load_puzzle(file_path=file_path, level=level, puzzle=puz)


def test_load_puzzle() -> None:
    file_path: Path = Path("./tests/data/puzzles.json")
    level = "beginner"
    puz = 1

    puzzle = load_puzzle(file_path=file_path, level=level, puzzle=puz)

    assert isinstance(puzzle, list)
    assert all(isinstance(item, int) for item in puzzle) is True


def test_load_puzzle_bad_path() -> None:
    file_path: Path = Path("./data/puzzles.json")
    level = "beginner"
    puz = 1

    with pytest.raises(PuzzleNotFoundError):
        load_puzzle(file_path=file_path, level=level, puzzle=puz)


def test_set_board(get_cells: Board, get_puzzle: list[int]) -> None:
    board: Board = get_cells
    puzzle: list[int] = get_puzzle

    set_board(board.index.values(), puzzle)

    assert board.rows[1][7].solved is True
    assert board.rows[1][7].solution == 5
    assert board.rows[1][7].initial is True

    assert board.columns[1][9].solved is True
    assert board.columns[1][9].solution == 9
    assert board.columns[1][9].initial is True

    assert board.houses[1][4].solved is False
    assert board.houses[1][4].solution is None
    assert board.houses[1][4].initial is False
