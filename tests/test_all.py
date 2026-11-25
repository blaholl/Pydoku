from collections.abc import Generator
from pathlib import Path

import pytest

from pydoku.objects import Board
from pydoku.solver import Solver

"""
Beginner - 100/100 Passed
Advanced - 99/100 Passed -> 71
Expert   - 38/100 Passed
"""


@pytest.fixture(params=["puzzle", "level"])
def get_boards_from_file(request: pytest.FixtureRequest) -> Generator[Board]:
    puzzle, level = request.param
    file_path: Path = Path("./tests/data/puzzles.json")

    board: Board = Board.from_puzzle(puzzle_path=file_path, level=level, num=puzzle)
    board.populate()
    yield board


@pytest.mark.skip("not yet implemented")
@pytest.mark.parametrize(
    "get_boards_from_file",
    [(i, "beginner") for i in range(1, 101)],
    indirect=True,
)
def test_beginner_puzzles(get_boards_from_file: Board) -> None:
    board = get_boards_from_file

    solver = Solver(board)

    solver.solve()
    assert board.verify() is True


@pytest.mark.skip("not yet implemented")
@pytest.mark.parametrize(
    "get_boards_from_file", [(i, "advanced") for i in range(1, 101)], indirect=True
)
def test_advanced_puzzles(get_boards_from_file: Board) -> None:
    board = get_boards_from_file

    solver = Solver(board)

    solver.solve()
    assert board.verify() is True


@pytest.mark.skip("not yet implemented")
@pytest.mark.parametrize(
    "get_boards_from_file", [(i, "expert") for i in range(1, 101)], indirect=True
)
def test_expert_puzzles(get_boards_from_file: Board) -> None:
    board = get_boards_from_file

    solver = Solver(board)

    solver.solve()
    assert board.verify() is True


@pytest.mark.skip("not yet implemented")
@pytest.mark.parametrize(
    "get_boards_from_file", [(i, "pro") for i in range(1, 101)], indirect=True
)
def test_pro_puzzles(get_boards_from_file: Board) -> None:
    board = get_boards_from_file

    solver = Solver(board)

    solver.solve()
    assert board.verify() is True


@pytest.mark.skip("not yet implemented")
@pytest.mark.parametrize(
    "get_boards_from_file", [(i, "impossible") for i in range(1, 31)], indirect=True
)
def test_impossible_puzzles(get_boards_from_file: Board) -> None:
    board = get_boards_from_file

    solver = Solver(board)

    solver.solve()
    assert board.verify() is True


@pytest.mark.skip("not yet implemented - NO TEST CASES")
@pytest.mark.parametrize(
    "get_boards_from_file", [(i, "extended") for i in range(1, 101)], indirect=True
)
def test_extended_puzzles(get_boards_from_file: Board) -> None:
    board = get_boards_from_file

    solver = Solver(board)

    solver.solve()
    assert board.verify() is True
