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


def test_naked_single(get_board_from_file: Board) -> None:
    board: Board = get_board_from_file

    init_count = len([cell for cell in board.cells if cell.solved])
    result: bool = board.check_naked_single()

    assert isinstance(result, bool)
    assert result is True

    updated_count = len([cell for cell in board.cells if cell.solved])
    assert init_count != updated_count
    assert updated_count > init_count


def test_hidden_single(get_board_from_file: Board) -> None:
    board: Board = get_board_from_file

    init_count = len([cell for cell in board.cells if cell.solved])
    board.check_naked_single()
    result: bool = board.check_hidden_single()

    assert isinstance(result, bool)
    assert result is True

    updated_count = len([cell for cell in board.cells if cell.solved])
    assert init_count != updated_count
    assert updated_count > init_count
