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
    [(1, "x_wing")],
    indirect=True,
)
def test_x_wing_1(get_board_from_file: Board) -> None:
    board: Board = get_board_from_file

    row_1, row_2 = board.rows[3], board.rows[7]
    col_1, col_2 = board.columns[3], board.columns[4]
    assert all(3 in row_1[i] for i in [3, 4])
    assert all(3 in row_2[i] for i in [3, 4])

    assert all(3 in col_1[i] for i in [1, 4, 5, 6])
    assert all(3 in col_2[i] for i in [1, 4, 5, 6, 9])

    board.show()
    res = board.check_x_wing()
    assert res is True

    assert all(3 in row_1[i] for i in [3, 4])
    assert all(3 in row_2[i] for i in [3, 4])

    assert all(3 not in col_1[i] for i in [1, 4, 5, 6])
    assert all(3 not in col_2[i] for i in [1, 4, 5, 6, 9])


@pytest.mark.parametrize(
    "get_board_from_file",
    [(2, "x_wing")],
    indirect=True,
)
def test_x_wing_2(get_board_from_file: Board) -> None:
    board: Board = get_board_from_file

    board.check_naked_double()
    board.check_hidden_double()
    col = board.columns[4]
    col[1].pop(5)
    col[6].pop(5)
    col[9].pop(5)
    board.check_locked_candidate()
    board.check_pointing_tuple()
    board.check_naked_double()
    board.check_pointing_tuple()

    row_1 = board.rows[6]
    row_2 = board.rows[8]

    assert all(4 in row_1[i] for i in [5, 8])
    assert all(4 in row_2[i] for i in [5, 8])

    res = board.check_x_wing()
    assert res is True

    col_1 = board.columns[5]
    col_2 = board.columns[8]

    assert all(4 in col_1[i] for i in [6, 8])
    assert all(4 in col_2[i] for i in [6, 8])

    assert all(4 not in col_1[i] for i in range(1, 10) if i not in [6, 8])
    assert all(4 not in col_2[i] for i in range(1, 10) if i not in [6, 8])


@pytest.mark.parametrize(
    "get_board_from_file",
    [(3, "x_wing")],
    indirect=True,
)
def test_x_wing_3(get_board_from_file: Board) -> None:
    board: Board = get_board_from_file

    col_1 = board.columns[6]
    col_2 = board.columns[9]
    assert all([(4 in col_1[i] for i in [1, 6]), (4 in col_2[i] for i in [1, 6])])
    row_1 = board.rows[1]
    row_2 = board.rows[6]
    assert all(
        [(4 in row_1[i] for i in [5, 6, 7, 9]), (4 in row_2[i] for i in [5, 6, 7, 9])]
    )
    res = board.check_x_wing()
    assert res is True

    assert all([(4 in col_1[i] for i in [1, 6]), (4 in col_2[i] for i in [1, 6])])
    assert all(
        [(4 not in row_1[i] for i in [5, 7]), (4 not in row_2[i] for i in [5, 7])]
    )


@pytest.mark.parametrize(
    "get_board_from_file",
    [(4, "x_wing")],
    indirect=True,
)
def test_x_wing_4(get_board_from_file: Board) -> None:
    board: Board = get_board_from_file

    row_1 = board.rows[5]
    row_2 = board.rows[9]
    assert all([(4 in row_1[i] for i in [6, 8]), (4 in row_2[i] for i in [6, 8])])
    col_1 = board.columns[6]
    col_2 = board.columns[8]
    assert all(
        [(4 in col_1[i] for i in [5, 6, 9]), (4 in col_2[i] for i in [1, 2, 5, 9])]
    )

    res = board.check_x_wing()
    assert res is True

    assert all([(4 in row_1[i] for i in [6, 8]), (4 in row_2[i] for i in [6, 8])])
    assert all([(4 not in col_1[i] for i in [6]), (4 not in col_2[i] for i in [1, 2])])


@pytest.mark.parametrize(
    "get_board_from_file",
    [(5, "x_wing")],
    indirect=True,
)
def test_x_wing_5(get_board_from_file: Board) -> None:
    board: Board = get_board_from_file

    row_1 = board.rows[1]
    row_2 = board.rows[7]
    x = [3, 8]
    assert all([(2 in row_1[i] for i in x), (2 in row_2[i] for i in x)])

    col_1 = board.columns[3]
    col_2 = board.columns[8]
    assert all([(2 in col_1[i] for i in x + [3, 8]), (2 in col_2[i] for i in x)])

    res = board.check_x_wing()
    assert res is True

    assert all([(2 in row_1[i] for i in x), (2 in row_2[i] for i in x)])
    assert all(2 not in col_1[i] for i in [3, 8])


@pytest.mark.parametrize(
    "get_board_from_file",
    [(6, "x_wing")],
    indirect=True,
)
def test_x_wing_6(get_board_from_file: Board) -> None:
    board: Board = get_board_from_file

    board.check_hidden_double()
    board.check_pointing_tuple()

    row_1 = board.rows[2]
    row_2 = board.rows[9]
    target = 7
    x = [5, 8]
    assert all([(target in row_1[i] for i in x), (target in row_2[i] for i in x)])

    col_1 = board.columns[5]
    col_2 = board.columns[8]
    assert all(
        [
            (target in col_1[i] for i in x + [3, 8]),
            (target in col_2[i] for i in x + [8]),
        ]
    )

    res = board.check_x_wing()
    assert res is True

    assert all([(target in row_1[i] for i in x), (target in row_2[i] for i in x)])
    assert all(
        [
            (target not in col_1[i] for i in [3, 8]),
            (target not in col_2[i] for i in [8]),
        ]
    )


@pytest.mark.parametrize(
    "get_board_from_file",
    [(1, "y_wing")],
    indirect=True,
)
def test_y_wing_1(get_board_from_file: Board) -> None:
    board: Board = get_board_from_file
    print()

    assert 6 in board.rows[9][6]

    # res = board.check_y_wing()
    # print(res)

    print("\n".join(f"{c.pos} - {len(c.strong_links)}" for c in board.bivals))

    # assert 6 not in board.rows[9][6]

    board.show()


@pytest.mark.parametrize(
    "get_board_from_file",
    [(2, "y_wing")],
    indirect=True,
)
def test_y_wing_2(get_board_from_file: Board) -> None:
    board: Board = get_board_from_file
    board.show()


@pytest.mark.parametrize(
    "get_board_from_file",
    [(3, "y_wing")],
    indirect=True,
)
def test_y_wing_3(get_board_from_file: Board) -> None:
    board: Board = get_board_from_file
    board.show()


@pytest.mark.parametrize(
    "get_board_from_file",
    [(4, "y_wing")],
    indirect=True,
)
def test_y_wing_4(get_board_from_file: Board) -> None:
    board: Board = get_board_from_file
    board.show()


@pytest.mark.parametrize(
    "get_board_from_file",
    [(5, "y_wing")],
    indirect=True,
)
def test_y_wing_5(get_board_from_file: Board) -> None:
    board: Board = get_board_from_file
    board.show()
