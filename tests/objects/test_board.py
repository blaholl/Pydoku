from pathlib import Path

import pytest

from pydoku.objects import Board, Cell, Column, House, Row
from pydoku.objects.containers import Columns, Houses, Rows, Sightline


@pytest.fixture
def get_cells() -> Board:
    board = Board()
    return board


@pytest.fixture
def get_board_from_file() -> Board:
    file_path: Path = Path("./tests/data/puzzles.json")
    level = "beginner"
    puz = 2

    board: Board = Board.from_puzzle(puzzle_path=file_path, level=level, num=puz)
    return board


def test_set_board() -> None:
    board: Board = Board()
    file_path: Path = Path("./tests/data/puzzles.json")
    level = "beginner"
    puz = 1

    board.set_puzzle(puzzle_path=file_path, level=level, num=puz)

    assert board.rows[1][7].solved is True
    assert board.rows[1][7].solution == 5
    assert board.rows[1][7].initial is True

    assert board.columns[1][9].solved is True
    assert board.columns[1][9].solution == 9
    assert board.columns[1][9].initial is True

    assert board.houses[1][4].solved is False
    assert board.houses[1][4].solution is None
    assert board.houses[1][4].initial is False


def test_construct_cells(get_cells: Board) -> None:
    board = get_cells

    assert isinstance(board, Board)
    assert all(isinstance(c, Cell) for c in board.cells) is True
    assert len(board.cells) == 81


def test_construct_rows(get_cells: Board) -> None:
    board: Board = get_cells

    assert isinstance(board.rows, Rows)
    assert all(isinstance(r, Row) for r in board.rows) is True


def test_construct_cols(get_cells: Board) -> None:
    board: Board = get_cells

    assert isinstance(board.columns, Columns)
    assert all(isinstance(c, Column) for c in board.columns) is True


def test_construct_houses(get_cells: Board) -> None:
    board: Board = get_cells

    assert isinstance(board.houses, Houses)
    assert all(isinstance(h, House) for h in board.houses) is True


def test_cells(get_cells: Board) -> None:
    board: Board = get_cells

    assert all(
        [
            board.rows[1][1] is board.columns[1][1],
            board.rows[1][1] is board.houses[1][1],
            board.columns[1][1] is board.houses[1][1],
        ]
    )

    assert all(
        [
            board.rows[2][5] is board.columns[5][2],
            board.rows[2][5] is board.houses[2][5],
            board.columns[5][2] is board.houses[2][5],
        ]
    )

    assert all(
        [
            board.rows[6][4] is board.columns[4][6],
            board.rows[6][4] is board.houses[5][7],
            board.columns[4][6] is board.houses[5][7],
        ]
    )


def test_new_board_from_puzzle() -> None:
    file_path: Path = Path("./tests/data/puzzles.json")
    level = "beginner"
    puz = 1

    board: Board = Board.from_puzzle(puzzle_path=file_path, level=level, num=puz)
    assert isinstance(board, Board)

    assert board.rows[1][7].solved is True
    assert board.rows[1][7].solution == 5
    assert board.rows[1][7].initial is True

    assert board.columns[1][9].solved is True
    assert board.columns[1][9].solution == 9
    assert board.columns[1][9].initial is True

    assert board.houses[1][4].solved is False
    assert board.houses[1][4].solution is None
    assert board.houses[1][4].initial is False


def test_set_cell_sightline(get_board_from_file: Board) -> None:
    board: Board = get_board_from_file

    cell_1 = board.index.get(1)

    sl: Sightline = board.get_cell_sightline(cell_1)

    assert isinstance(sl, Sightline)
    assert sl.idx == cell_1.idx
    assert sl.row.idx == cell_1.row == 1
    assert sl.col.idx == cell_1.col == 1
    assert sl.house.idx == cell_1.house == 1

    cell_2 = board.index.get(50)

    sl: Sightline = board.get_cell_sightline(cell_2)

    assert isinstance(sl, Sightline)
    assert sl.idx == cell_2.idx
    assert sl.row.idx == 6
    assert sl.col.idx == 5
    assert sl.house.idx == 5


def test_get_all_sightlines(get_board_from_file: Board, subtests) -> None:
    board: Board = get_board_from_file

    board.populate()

    assert len(board.rows) == 9
    assert len(board.columns) == 9
    assert len(board.houses) == 9

    for c in board.cells:
        with subtests.test(msg=f"{c.idx}", i=c.idx):
            if not c.solved:
                assert len(c.can) >= 1
                assert len(c.exc) >= 1
            else:
                assert c.solved is True
                assert c.initial is True


def test_gather_open_containers(get_board_from_file: Board) -> None:
    board: Board = get_board_from_file

    board.populate()

    containers = list(board._gather_open_containers())
    row_count: int = len(board.rows.open)
    col_count: int = len(board.columns.open)
    house_count: int = len(board.houses.open)

    assert len(containers) == row_count + col_count + house_count
    assert all(con.solved is False for con in containers) is True


def test_print_verify(get_board_from_file: Board) -> None:
    board: Board = get_board_from_file

    board.populate()

    board.check_naked_single()
    board.check_hidden_single()

    board.verify()
