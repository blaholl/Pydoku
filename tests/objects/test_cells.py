import pytest

from pydoku.objects import Cell
from pydoku.utils import EmptyCellError, IllegalAnswerError


@pytest.fixture
def create_cell() -> Cell:
    row: int = 1
    col: int = 7
    house: int = 3
    return Cell(idx=1, coords=(row, col, house))


def test_create_cell(create_cell: Cell) -> None:
    row, col, house = 1, 7, 3
    cell: Cell = create_cell

    assert cell.pos.r == row
    assert isinstance(cell.pos.r, type(row))
    assert cell.row == cell.pos.r
    assert cell.pos.c == col
    assert isinstance(cell.pos.c, type(col))
    assert cell.col == cell.pos.c
    assert cell.pos.h == house
    assert isinstance(cell.pos.h, type(house))
    assert cell.house == cell.pos.h


def test_cell_eq(create_cell: Cell) -> None:
    cell_1: Cell = create_cell
    cell_1.can = {1, 2, 4, 5}

    cell_2 = Cell(2, (1, 8, 3))
    cell_2.can = {1, 2, 4, 5}

    assert cell_1 == cell_2


def test_cell_contains(create_cell: Cell) -> None:
    cell: Cell = create_cell
    cell.can = {1, 2, 4, 5}

    assert 2 in cell
    assert 9 not in cell


def test_pop_int_from_cell(create_cell: Cell) -> None:
    cell: Cell = create_cell
    cell.can = {1, 2, 4, 5}

    cell.pop(2)

    assert 2 not in cell
    assert 2 in cell.exc


def test_pop_empty_cell(create_cell: Cell) -> None:
    cell: Cell = create_cell

    with pytest.raises(EmptyCellError):
        cell.pop(2)


def test_pop_list_from_cell(create_cell: Cell) -> None:
    cell: Cell = create_cell
    cell.can = {1, 2, 4, 5}

    cell.pop([2, 3])

    assert 2 not in cell
    assert 2 in cell.exc


def test_pop_list_empty_cell(create_cell: Cell) -> None:
    cell: Cell = create_cell

    with pytest.raises(EmptyCellError):
        cell.pop([2, 5])


def test_pop_tuple_from_cell(create_cell: Cell) -> None:
    cell: Cell = create_cell
    cell.can = {1, 2, 4, 5}

    cell.pop((2, 3))

    assert 2 not in cell
    assert 2 in cell.exc


def test_cell_sees(create_cell: Cell) -> None:
    cell_1: Cell = create_cell

    cell_2 = Cell(2, (1, 8, 3))

    cell_3 = Cell(3, (4, 3, 4))

    assert cell_1.sees(cell_2) is True
    assert cell_1.sees(cell_3) is False


def test_cell_shares_row(create_cell: Cell) -> None:
    cell_1: Cell = create_cell

    cell_2 = Cell(2, (1, 8, 3))
    cell_3 = Cell(3, (4, 3, 4))

    assert cell_1.shares_row(cell_2) is True
    assert cell_1.shares_row(cell_3) is False


def test_cell_shares_col(create_cell: Cell) -> None:
    cell_1: Cell = create_cell

    cell_2 = Cell(2, (2, 7, 3))

    cell_3 = Cell(3, (4, 3, 4))

    assert cell_1.shares_col(cell_2) is True
    assert cell_1.shares_col(cell_3) is False


def test_cell_shares_house(create_cell: Cell) -> None:
    cell_1: Cell = create_cell

    cell_2 = Cell(2, (2, 7, 3))

    cell_3 = Cell(3, (4, 3, 4))

    assert cell_1.shares_house(cell_2) is True
    assert cell_1.shares_house(cell_3) is False


def test_solve_cell(create_cell: Cell) -> None:
    cell: Cell = create_cell
    cell.can = {1, 2, 4, 5}
    assert 4 in cell

    assert cell.solved is False
    assert isinstance(cell.can, list)
    assert isinstance(cell.exc, list)

    cell.solve(4)
    assert cell.solution == 4
    assert cell.solution is not None
    assert cell.solved is True

    assert len(cell.can) == 0
    assert len(cell.exc) == 0


def test_solve_cell_zero(create_cell: Cell) -> None:
    cell: Cell = create_cell
    cell.can = {1, 2, 4, 5}

    assert cell.solved is False

    cell.solve(0)

    assert cell.solved is False
    assert cell.solution is None


def test_illegal_solve_cell(create_cell: Cell) -> None:
    cell: Cell = create_cell
    cell.can = {1, 2, 4, 5}
    assert 4 in cell

    cell.pop(4)

    with pytest.raises(IllegalAnswerError):
        cell.solve(4)
