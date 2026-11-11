from pathlib import Path

import pytest

from pydoku.objects import Board


@pytest.fixture
def get_board_from_file() -> Board:
    file_path: Path = Path("./tests/data/puzzles.json")
    level = "beginner"
    puz = 2

    board: Board = Board.from_puzzle(puzzle_path=file_path, level=level, num=puz)
    board.populate()
    return board


@pytest.fixture
def get_board_hd_from_file() -> Board:
    file_path: Path = Path("./tests/data/test-puzzles.json")
    level = "hidden_pair"
    puz = 1

    board: Board = Board.from_puzzle(puzzle_path=file_path, level=level, num=puz)
    board.populate()
    return board


def test_naked_double(get_board_from_file: Board) -> None:
    board: Board = get_board_from_file

    assert 7 in board.index.get(20)

    result: bool = board.check_naked_double()
    assert result is True
    assert 4 not in board.index.get(20)
    assert 7 not in board.index.get(20)
    assert 4 not in board.index.get(25)
    assert 7 not in board.index.get(25)
    assert 4 not in board.index.get(26)
    assert 7 not in board.index.get(26)

    assert 4 in board.index.get(23)
    assert 7 in board.index.get(23)
    assert 4 in board.index.get(24)
    assert 7 in board.index.get(24)


def test_hidden_double(get_board_hd_from_file: Board) -> None:
    board: Board = get_board_hd_from_file

    assert 1 in board.index.get(49)
    assert 3 in board.index.get(49)
    assert 1 in board.index.get(51)
    assert 3 in board.index.get(51)
    assert 4 in board.index.get(51)

    result: bool = board.check_hidden_double()
    assert result is True
    board.check_naked_double()

    assert 5 in board.index.get(49)
    assert 5 in board.index.get(51)
    assert 8 in board.index.get(49)
    assert 8 in board.index.get(51)

    assert 1 not in board.index.get(49)
    assert 3 not in board.index.get(49)
    assert 1 not in board.index.get(51)
    assert 3 not in board.index.get(51)
    assert 4 not in board.index.get(51)

    assert 5 not in board.index.get(46)
    assert 5 not in board.index.get(47)
    assert 5 not in board.index.get(48)
    assert 5 not in board.index.get(50)
    assert 5 not in board.index.get(52)
    assert 5 not in board.index.get(53)
    assert 5 not in board.index.get(54)

    assert 8 not in board.index.get(46)
    assert 8 not in board.index.get(47)
    assert 8 not in board.index.get(48)
    assert 8 not in board.index.get(50)
    assert 8 not in board.index.get(52)
    assert 8 not in board.index.get(53)
    assert 8 not in board.index.get(54)
