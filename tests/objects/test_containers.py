from pathlib import Path

import more_itertools as mi
import pytest

from pydoku.objects import Board, Cell, Column, House, Row
from pydoku.objects.containers import Columns, Houses, PhistomefelRing, Rows, StrongLink


@pytest.fixture
def get_board() -> Board:
    board: Board = Board()

    return board


@pytest.fixture
def get_populated_board() -> Board:
    file_path: Path = Path("./tests/data/puzzles.json")
    level = "beginner"
    puz = 1

    board: Board = Board.from_puzzle(puzzle_path=file_path, level=level, num=puz)
    return board


@pytest.fixture
def get_stronglink_board() -> Board:
    file_path: Path = Path("./tests/data/test-puzzles.json")
    level = "locked_candidate"
    puz = 1

    board: Board = Board.from_puzzle(puzzle_path=file_path, level=level, num=puz)
    board.populate()
    return board


def test_row_index(get_board: Board) -> None:
    board: Board = get_board

    rows: Rows = board.rows

    assert all(isinstance(row, Row) for row in rows) is True
    assert all(len(r.cells) == 9 for r in rows) is True

    row: Row = rows[1]
    assert row.idx == 1
    assert row[1] == mi.first(row)
    assert row[-1] == mi.last(row)

    assert row[1].pos == (1, 1, 1)


def test_col_index(get_board: Board) -> None:
    board: Board = get_board

    cols: Columns = board.columns

    assert all(isinstance(col, Column) for col in cols) is True
    assert all(len(c.cells) == 9 for c in cols) is True

    col: Column = cols[1]
    assert col.idx == 1
    assert col[1] == mi.first(col)
    assert col[-1] == mi.last(col)

    assert col[1].pos == (1, 1, 1)


def test_house_index(get_board: Board) -> None:
    board: Board = get_board

    houses: Houses = board.houses

    assert all(isinstance(house, House) for house in houses) is True
    assert all(len(h.cells) == 9 for h in houses) is True

    house: House = houses[1]
    assert house.idx == 1
    assert house[1] == mi.first(house)
    assert house[-1] == mi.last(house)

    assert house[1].pos == (1, 1, 1)
    assert house[9].pos == (3, 3, 1)


def test_set_cell_solved(get_board: Board) -> None:
    board: Board = get_board
    row: Row = board.rows[1]

    for i in range(1, 10):
        row[i].solve(i)

    assert row.is_solved() is True
    assert len(row.closed) == 9

    assert board.columns[6][1].solved is True
    assert board.columns[6][1].solution == 6

    assert board.houses[3][2].solved is True
    assert board.houses[3][2].solution == 8


def test_container_open(get_populated_board: Board) -> None:
    board: Board = get_populated_board
    row = board.rows[1]

    c_open: list[Cell] = row.open
    c_closed: list[Cell] = row.closed

    assert isinstance(c_open, list)
    assert isinstance(c_closed, list)

    c_known: list[int] = row.known
    c_unknown: list[int] = row.unknown

    assert isinstance(c_known, list)
    assert isinstance(c_unknown, list)

    assert len(c_known) + len(c_unknown) == 9
    assert len(set(c_known) ^ set(c_unknown)) == 9
    assert len(set(c_known) & set(c_unknown)) == 0


def test_containers_open(get_populated_board: Board) -> None:
    board: Board = get_populated_board

    solved_rows = board.rows.closed
    solved_cols = board.columns.closed
    solved_houses = board.houses.closed
    assert len(solved_rows) == 0
    assert len(solved_cols) == 0
    assert len(solved_houses) == 0

    unsolved_rows = board.rows.open
    unsolved_cols = board.columns.open
    unsolved_houses = board.houses.open
    assert len(unsolved_rows) == 9
    assert len(unsolved_cols) == 9
    assert len(unsolved_houses) == 9


def test_house_intersections(get_populated_board: Board) -> None:
    board: Board = get_populated_board

    house: House = board.houses[2]
    rows = house.row_intersections
    cols = house.col_intersections

    assert rows == [1, 2, 3]
    assert cols == [4, 5, 6]

    row: Row = board.rows[1]
    assert row.intersections == [1, 2, 3]

    col: Column = board.columns[1]
    assert col.intersections == [1, 4, 7]


def test_strong_link(get_stronglink_board: Board) -> None:
    board: Board = get_stronglink_board

    house = board.houses[7]
    links = house.get_strong_links()

    assert isinstance(links[0], StrongLink)
    for link in links:
        if link.link == 6:
            assert link.house is True
            assert link.diagonal is True
            assert link.row is False
            assert link.col is False
        if link.link == 5:
            assert link.house is True
            assert link.diagonal is False
            assert link.row is True
            assert link.col is False

    column = board.columns[5]
    c_links = column.get_strong_links()

    link = c_links[0]
    assert isinstance(link, StrongLink)
    assert link.house is False
    assert link.diagonal is False
    assert link.row is False
    assert link.col is True


def test_phisto_ring() -> None:
    inner = [9, 8, 6, 3, 4, 8, 7, 5, 3, 5, 8, 4, 6, 3, 2, 7]
    outer = [3, 6, 8, 4, 8, 7, 3, 6, 7, 9, 5, 3, 4, 5, 2, 8]

    ring = PhistomefelRing(outer=outer, inner=inner)

    assert isinstance(ring, PhistomefelRing)
    assert ring.compare() is True
    assert ring.diff() == 0
    assert ring.inner_count == ring.outer_count


def test_phisto_ring_incomplete() -> None:
    inner = [9, 8, 6, 3, 4, 8, 7, 5, 3, 5, 8, 4, 6]
    outer = [3, 6, 8, 4, 8, 7, 3, 6, 7, 9, 5, 3, 4, 5, 2, 8]

    ring = PhistomefelRing(outer=outer, inner=inner)

    assert isinstance(ring, PhistomefelRing)
    assert ring.compare() is False
    assert ring.diff() == 3
    assert ring.inner_count != ring.outer_count


def test_set_phisto_ring(get_populated_board: Board) -> None:
    board: Board = get_populated_board
    board.populate()

    phisto: PhistomefelRing = board.phistomefel_ring
    assert phisto.compare() is False
    assert phisto.diff() == 2
    assert len(phisto.count_diff()) == 2

    board.check_naked_single()
    board.check_hidden_single()

    phisto: PhistomefelRing = board.phistomefel_ring
    assert phisto.compare() is True
    assert phisto.diff() == 0
    assert len(phisto.count_diff()) == 0

    assert board.verify() is True
