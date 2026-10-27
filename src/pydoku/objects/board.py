import itertools as it
from collections.abc import Iterable
from functools import singledispatchmethod
from pathlib import Path
from types import NoneType

import more_itertools as mi

from ..techniques import *
from ..utils.construct_board import construct_cells, load_puzzle, set_board
from ..utils.display import display_board, display_verify
from ..utils.result import Excluded, NoOp, Solved
from .cell import Cell
from .containers import Column, Columns, Container, House, Houses, Row, Rows, Sightline

type Puzzle = list[int]

type Containers = Rows | Columns | Houses


class Board:
    def __init__(self) -> None:
        self.populated: bool = False
        self.cells: list[Cell] = [
            Cell(idx=i, coords=c) for i, c in enumerate(construct_cells(), 1)
        ]

        assert len(self.cells) == 81

        self.index: dict[int, Cell] = {c.idx: c for c in self.cells}

        assert len(self.index) == 81

        self.rows: Rows = Rows(
            Row(idx=i, cells=list(cells))
            for i, cells in enumerate(
                it.batched(sorted(self.cells, key=lambda x: x.row), 9), 1
            )
        )
        assert len(self.rows) == 9

        self.columns: Columns = Columns(
            Column(idx=i, cells=list(cells))
            for i, cells in enumerate(
                it.batched(sorted(self.cells, key=lambda x: x.col), 9),
                1,
            )
        )

        assert len(self.columns) == 9

        self.houses: Houses = Houses(
            House(idx=i, cells=list(cells))
            for i, cells in enumerate(
                it.batched(sorted(self.cells, key=lambda x: x.house), 9),
                1,
            )
        )

        assert len(self.houses) == 9

        self.containers: list[Container] = list(
            mi.flatten([self.rows, self.columns, self.houses])
        )

        self.files: list[Rows] = None
        self.ranks: list[Columns] = None

    def set_puzzle(self, puzzle_path: str, level: str, num: int) -> None:
        puzzle: Puzzle = load_puzzle(Path(puzzle_path), level=level, puzzle=num)
        set_board(self.index.values(), puzzle)

    @classmethod
    def from_puzzle(cls, puzzle_path: str, level: str, num: int) -> None:
        puzzle: Puzzle = load_puzzle(Path(puzzle_path), level=level, puzzle=num)
        board = cls()
        set_board(board.index.values(), puzzle)
        return board

    @singledispatchmethod
    def get_cell_sightline(self, cell: Cell, open: bool = False) -> Sightline:
        if open:
            return Sightline(
                idx=cell.idx,
                row=self.rows[cell.row].open,
                col=self.columns[cell.col].open,
                house=self.houses[cell.house].open,
            )
        return Sightline(
            idx=cell.idx,
            row=self.rows[cell.row],
            col=self.columns[cell.col],
            house=self.houses[cell.house],
        )

    @get_cell_sightline.register(NoneType)
    def _(self, _: NoneType, __: bool = False) -> Iterable[Sightline]:
        return (
            Sightline(
                idx=c.idx,
                row=self.rows[c.row],
                col=self.columns[c.col],
                house=self.houses[c.house],
            )
            for c in self.cells
        )

    def populate(self) -> None:
        cell_sls: Iterable[Sightline] = self.get_cell_sightline(None)

        sl: Sightline
        for sl in cell_sls:
            cell: Cell = self.index[sl.idx]
            if cell.solved:
                continue
            known: set[int] = {
                c.solution
                for c in mi.flatten([sl.row.cells, sl.col.cells, sl.house.cells])
                if c.solution is not None
            }

            cell.exc = known
            cell.can = set(range(1, 10)) - known

    @singledispatchmethod
    def evaluate_result(self, result: NoOp) -> None:
        _ = result

    @evaluate_result.register(Solved)
    def _(self, result: Solved) -> int:
        count = 0
        for cell in result.cells:
            sl: Sightline = self.get_cell_sightline(cell, open=True)
            c: Cell
            for c in mi.flatten((sl.row, sl.col, sl.house)):
                c.pop(cell.solution)
                count += 1

        return count

    @evaluate_result.register(Excluded)
    def _(self, result: Excluded) -> None:
        _ = result

    def verify(self) -> bool:
        return all(con.is_solved() for con in self.containers)

    def show(self, verify: bool = False, *, print_verify: bool = False) -> None:
        if verify:
            print(self.verify())

        if print_verify:
            display_verify(self)

        display_board(self)

    def _gather_open_containers(self) -> Iterable[Container]:
        return mi.flatten([self.rows.open, self.columns.open, self.houses.open])

    def check_naked_single(self) -> int:
        solved: list[Cell] = [list(NakedSingle.check(row)) for row in self.rows.open]
        if not solved:
            return NoOp()

        count: int = self.evaluate_result(
            Solved(cells=sorted(mi.flatten(solved), key=lambda x: x.idx))
        )

        return count

    def check_hidden_single(self) -> int:
        solved: list[Cell] = [
            list(HiddenSingle.check(container))
            for container in self._gather_open_containers()
        ]
        if not solved:
            return NoOp()

        count: int = self.evaluate_result(
            Solved(cells=sorted(mi.flatten(solved), key=lambda x: x.idx))
        )

        return count

    def check_naked_double(self) -> int:
        solved: list[tuple[Cell]] = [
            list(NakedDouble.check(container))
            for container in self.rows.open + self.columns.open + self.houses.open
        ]
        counts = sum(mi.flatten(solved))
        if not counts or counts == 0:
            return NoOp()

        # deduped: list[tuple[Cell]] = [item for item in solved if item]
        # count: int = self.evaluate_result(
        #     Excluded(cells=sorted(mi.flatten(solved), key=lambda x: x.idx))
        # )

        return counts
