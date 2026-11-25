from pathlib import Path

import pytest

from pydoku.objects import Board


@pytest.fixture(params=["puzzle", "level"])
def get_board_from_file(request: pytest.FixtureRequest) -> Board:
    puzzle, level = request.param
    file_path: Path = Path("./tests/data/test-puzzles.json")

    board: Board = Board.from_puzzle(puzzle_path=file_path, level=level, num=puzzle)
    board.populate()
    return board


@pytest.mark.parametrize(
    "get_board_from_file",
    [(1, "locked_candidate")],
    indirect=True,
)
def test_locked_candidate(get_board_from_file: Board) -> None:
    board: Board = get_board_from_file

    board.check_naked_double()
    house_6 = board.houses[6]
    house_9 = board.houses[9]
    assert all(2 in house_6[i] for i in [2, 4, 5, 7, 8])
    assert all(3 in house_9[i] for i in [1, 3, 5, 7, 8, 9])

    res = board.check_locked_candidate()
    assert res is True

    assert all(2 in house_6[i] for i in [4, 7])
    assert all(2 not in house_6[i] for i in [2, 5, 8])
    assert all(3 in house_9[i] for i in [1, 7])
    assert all(3 not in house_9[i] for i in [3, 5, 8, 9])


@pytest.mark.parametrize(
    "get_board_from_file",
    [(2, "locked_candidate")],
    indirect=True,
)
def test_2nd_locked_candidate(get_board_from_file: Board) -> None:
    board: Board = get_board_from_file

    house = board.houses[4]
    house_7 = board.houses[7]
    assert all(5 in house[i] for i in [5, 6, 8, 9])
    assert all(7 in house_7[i] for i in [1, 3, 5, 7, 8, 9])

    res = board.check_locked_candidate()
    assert res is True

    assert all(5 in house[i] for i in [6, 9])
    assert all(5 not in house[i] for i in [5, 8])
    assert all(7 in house_7[i] for i in [3, 9])
    assert all(7 not in house_7[i] for i in [1, 5, 7, 8])


@pytest.mark.parametrize(
    "get_board_from_file",
    [(2, "pointing_tuple")],
    indirect=True,
)
def test_pointing_tuple(get_board_from_file: Board) -> None:
    board: Board = get_board_from_file

    col = board.columns[2]
    assert all(1 in col[i] for i in [3, 5, 6])
    res = board.check_pointing_tuple()
    assert res is True

    assert all(1 in col[i] for i in [5, 6])
    assert 1 not in col[3]


@pytest.mark.parametrize("get_board_from_file", [(3, "pointing_tuple")], indirect=True)
def test_3rd_pointing_tuple(get_board_from_file: Board) -> None:
    board: Board = get_board_from_file

    board.rows[1][4].pop(5)
    board.rows[2][8].pop(5)
    board.rows[3][9].pop(5)

    for i in [2, 5, 8]:
        board.columns[2][i].pop(5)
    for i in [1, 5, 7, 8]:
        board.houses[7][i].pop(7)

    col = board.columns[5]
    assert all(4 in col[i] for i in [4, 6, 8])

    res = board.check_pointing_tuple()
    assert res is True

    assert all(4 in col[i] for i in [4, 6])
    assert 4 not in col[8]


@pytest.mark.parametrize(
    "get_board_from_file",
    [(1, "pointing_tuple")],
    indirect=True,
)
def test_2nd_pointing_tuple(get_board_from_file: Board) -> None:
    board: Board = get_board_from_file

    res = board.check_pointing_tuple()
    assert res is False
