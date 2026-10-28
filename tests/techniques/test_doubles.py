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


def test_naked_double(get_board_from_file: Board) -> None:
    board: Board = get_board_from_file

    assert 7 in board.index.get(20)

    count: int = board.check_naked_double()
    assert count >= 1
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


@pytest.mark.skip("Not Implemented")
def test_hidden_single(get_board_from_file: Board) -> None:
    board: Board = get_board_from_file

    init_count = len([cell for cell in board.cells if cell.solved])
    board.check_naked_single()
    count: int = board.check_hidden_single()

    assert isinstance(count, int)
    assert count >= 1

    updated_count = len([cell for cell in board.cells if cell.solved])
    assert init_count != updated_count
    assert updated_count > init_count
