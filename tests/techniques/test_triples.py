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


@pytest.fixture
def get_board_2nd_nt_from_file() -> Board:
    file_path: Path = Path("./tests/data/test-puzzles.json")
    level = "naked_triple"
    puz = 2

    board: Board = Board.from_puzzle(puzzle_path=file_path, level=level, num=puz)
    board.populate()
    return board


@pytest.fixture
def get_board_ht_from_file() -> Board:
    file_path: Path = Path("./tests/data/test-puzzles.json")
    level = "hidden_triple"
    puz = 1

    board: Board = Board.from_puzzle(puzzle_path=file_path, level=level, num=puz)
    board.populate()
    return board


def test_naked_triple(get_board_from_file: Board) -> None:
    board: Board = get_board_from_file
    board.populate()

    house = board.houses[2]
    assert all(2 in house[i] for i in [3, 6])

    result = board.check_naked_triple()

    assert result is True
    assert all(2 not in house[i] for i in [3, 6])


def test_second_naked_triple(get_board_2nd_nt_from_file: Board) -> None:
    board: Board = get_board_2nd_nt_from_file
    board.populate()

    house = board.houses[6]
    assert all(5 in house[i] for i in [3, 6, 8, 9])
    assert 8 in house[8]

    result = board.check_naked_triple()

    assert result is True
    assert all(5 not in house[i] for i in [3, 6, 8, 9])
    assert 8 not in house[8]


def test_hidden_triple(get_board_ht_from_file: Board) -> None:
    board: Board = get_board_ht_from_file
    board.populate()

    board.check_naked_double()

    house = board.houses[9]
    assert all(1 in house[i] for i in [4, 7, 9])
    assert all(3 in house[i] for i in [4, 7])
    assert all(9 in house[i] for i in [7, 9])
    assert all(6 in house[i] for i in [4, 7, 9])
    assert all(8 in house[i] for i in [7, 9])

    board.check_hidden_triple()
    assert all(1 in house[i] for i in [4, 7, 9])
    assert all(3 in house[i] for i in [4, 7])
    assert all(9 in house[i] for i in [7, 9])
    assert all(6 not in house[i] for i in [4, 7, 9])
    assert all(8 not in house[i] for i in [7, 9])
