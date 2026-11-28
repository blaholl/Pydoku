import itertools as it
import logging
from collections.abc import Callable, Iterable
from functools import singledispatchmethod
from pathlib import Path
from types import NoneType
from typing import Self

import more_itertools as mi

from ..techniques import *
from ..utils import set_cells, set_excluded, set_log
from ..utils.construct_board import construct_cells, load_puzzle, set_board
from ..utils.display import display_board, display_verify
from ..utils.result import Excluded, NoOp, Solved
from .cell import Cell
from .containers import (
    Column,
    Columns,
    Container,
    House,
    Houses,
    PhistomefelRing,
    Row,
    Rows,
    Sightline,
)

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

        self.files: list[Rows] = None
        self.ranks: list[Columns] = None

        self.containers: list[Container] = list(
            mi.flatten([self.rows, self.columns, self.houses])
        )

        self._open: Iterable[Container] = (
            self.rows.open + self.columns.open + self.houses.open
        )

        self._phistomefel_ring: PhistomefelRing = None
        self._bivals: set[Cell] = set()
        self._get_all_bival_cells()

    @property
    def open(self) -> Iterable[Container]:
        return list(self._open)

    @open.setter
    def open(self) -> Iterable[Container]:
        self._open = mi.flatten(self.rows.open + self.columns.open + self.houses.open)

    @property
    def phistomefel_ring(self) -> PhistomefelRing:
        return self._set_phistomefel_ring()

    @property
    def bivals(self) -> list[Cell]:
        return sorted(
            self._get_all_bival_cells(), key=lambda c: (c.row, c.col, c.house)
        )

    def set_puzzle(self, puzzle_path: str, level: str, num: int) -> None:
        puzzle: Puzzle = load_puzzle(Path(puzzle_path), level=level, puzzle=num)
        set_board(self.index.values(), puzzle)

    @classmethod
    def from_puzzle(cls, puzzle_path: str, level: str, num: int) -> Self:
        puzzle: Puzzle = load_puzzle(Path(puzzle_path), level=level, puzzle=num)
        board = cls()
        set_board(board.index.values(), puzzle)
        return board

    def _set_phistomefel_ring(self) -> PhistomefelRing:
        col_1, col_2, col_8, col_9 = (
            self.columns[1],
            self.columns[2],
            self.columns[8],
            self.columns[9],
        )
        outer_range = [1, 2, 8, 9]
        outer_cells = (
            [col_1[i] for i in outer_range]
            + [col_2[i] for i in outer_range]
            + [col_8[i] for i in outer_range]
            + [col_9[i] for i in outer_range]
        )
        row_3, row_7, house_4, house_6 = (
            self.rows[3],
            self.rows[7],
            self.houses[4],
            self.houses[6],
        )
        row_range = range(3, 8)
        inner_cells = (
            [row_3[i] for i in row_range]
            + [row_7[i] for i in row_range]
            + [house_4[i] for i in [3, 6, 9]]
            + [house_6[i] for i in [1, 4, 7]]
        )

        return PhistomefelRing(
            outer=[c.solution for c in outer_cells if c.solved],
            inner=[c.solution for c in inner_cells if c.solved],
        )

        # return phistomefel_ring

    @singledispatchmethod
    def get_cell_sightline(self, cell: Cell, open: bool = False) -> Sightline:
        if not open:
            sightline = Sightline(
                idx=cell.idx,
                row=self.rows[cell.row],
                col=self.columns[cell.col],
                house=self.houses[cell.house],
            )
            cell.sightline = sightline
            return sightline
        return Sightline(
            idx=cell.idx,
            row=self.rows[cell.row].open,
            col=self.columns[cell.col].open,
            house=self.houses[cell.house].open,
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

        for cell in self.cells:
            cell.sightline = self.get_cell_sightline(cell)

    def _get_all_bival_cells(self) -> list[Cell]:
        for con in self.open:
            con.get_strong_links()

        for c in self.index.values():
            if c.bival and not c.solved:
                self._bivals.add(c)

        return self._bivals

    def gather_stats(self) -> None:
        pass

    @singledispatchmethod
    def evaluate_result(self, _: NoOp) -> None:
        pass

    @evaluate_result.register(Solved)
    def _(self, result: Solved) -> None:
        set_log(
            msg=f"Setting solution `{result.cell.solution}` in Cell({result.cell.pos})",
            level=logging.DEBUG,
            fn="evaluate_result",
        )
        if result.cell.sightline.propagate(result.cell.solution):
            self.check_hidden_single()
            self.check_naked_single()

    @evaluate_result.register(Excluded)
    def _(self, result: Excluded) -> None:
        for cell, num in it.product(result.cells, result.to_exclude):
            set_log(
                msg=f"Removing `{num}` from Cell({cell.pos})",
                level=logging.DEBUG,
                fn="evaluate_result",
            )
            cell.pop(num)

    def verify(self) -> bool:
        return all(
            [(con.solved for con in self.containers), self.phistomefel_ring.compare()]
        )

    def show(self, verify: bool = True, *, print_verify: bool = False) -> None:
        if print_verify:
            display_verify(self)

        if verify:
            print(self.verify())

        display_board(self)

    def cleanup(func: Callable[...]) -> None:
        def wrapper(self) -> Callable[[None], bool]:
            set_log(msg=f"Entering {func.__name__}", level=logging.DEBUG, fn="cleanup")
            res: bool = func(self)
            set_log(msg=f"Exiting {func.__name__}", level=logging.DEBUG, fn="cleanup")
            if res is True:
                self._get_all_bival_cells()
            return res

        return wrapper

    def check_naked_single(self) -> bool:
        result: bool = False

        for container in self.open:
            for ns in NakedSingle(container):
                self.evaluate_result(ns)
                if not isinstance(ns, NoOp):
                    result = True

        return result

    @cleanup
    def check_hidden_single(self) -> bool:
        result: bool = False
        for container in self.open:
            for hs in HiddenSingle(container):
                hs: Solved
                self.evaluate_result(hs)
                if not isinstance(hs, NoOp):
                    result = True

        return result

    @cleanup
    def check_naked_double(self) -> bool:
        result: bool = False

        for container in self.open:
            if len(container.open) < 4:
                continue
            for nd in NakedDouble(container):
                nd: Excluded
                self.evaluate_result(nd)
                if not isinstance(nd, NoOp):
                    set_log(
                        msg=f"Excluded {set_excluded(nd.to_exclude)} from:{set_cells(nd.cells)}",
                        level=logging.DEBUG,
                        fn="check_naked_double",
                    )
                    result = True

        return result

    @cleanup
    def check_hidden_double(self) -> bool:
        result: bool = False

        for container in self.open:
            if len(container.open) < 4:
                continue
            for hd in HiddenDouble(container):
                hd: Excluded
                self.evaluate_result(hd)
                if not isinstance(hd, NoOp):
                    set_log(
                        msg=f"Excluded {set_excluded(hd.to_exclude)} from:{set_cells(hd.cells)}",
                        level=logging.DEBUG,
                        fn="check_hidden_double",
                    )
                    result = True

        return result

    @cleanup
    def check_naked_triple(self) -> bool:
        result: bool = False

        for container in self.open:
            if len(container.open) <= 4:
                continue
            for nt in NakedTriple(container):
                nt: Excluded
                self.evaluate_result(nt)
                if not isinstance(nt, NoOp):
                    set_log(
                        msg=f"Excluded {set_excluded(nt.to_exclude)} from:{set_cells(nt.cells)}",
                        level=logging.DEBUG,
                        fn="check_naked_triple",
                    )
                    result = True

        return result

    @cleanup
    def check_hidden_triple(self) -> bool:
        result: bool = False

        for container in self.open:
            if len(container.open) <= 5:
                continue
            for ht in HiddenTriple(container):
                ht: Excluded
                self.evaluate_result(ht)
                if not isinstance(ht, NoOp):
                    set_log(
                        msg=f"Excluded {set_excluded(ht.to_exclude)} from:{set_cells(ht.cells)}",
                        level=logging.DEBUG,
                        fn="check_hidden_triple",
                    )
                    result = True

        return result

    @cleanup
    def check_pointing_tuple(self) -> bool:
        result: bool = False

        houses: list[House] = [house for house in self.houses if not house.solved]
        for house in houses:
            rows = [
                self.rows[i]
                for i in house.row_intersections
                if not self.rows[i].solved and len(self.rows[i]) >= 3
            ]
            for pt in PointingTuple(house, rows):
                pt: Excluded
                self.evaluate_result(pt)
                if not isinstance(pt, NoOp):
                    set_log(
                        msg=f"Excluded {set_excluded(pt.to_exclude)} from:{set_cells(pt.cells)}",
                        level=logging.DEBUG,
                        fn="check_pointing_tuple",
                    )
                    result = True

            cols = [
                self.columns[i]
                for i in house.col_intersections
                if not self.columns[i].solved and len(self.columns[i]) >= 3
            ]
            for pt in PointingTuple(house, cols):
                pt: Excluded
                self.evaluate_result(pt)
                if not isinstance(pt, NoOp):
                    set_log(
                        msg=f"Excluded {set_excluded(pt.to_exclude)} from:{set_cells(pt.cells)}",
                        level=logging.DEBUG,
                        fn="check_pointing_tuple",
                    )
                    result = True

        return result

    @cleanup
    def check_locked_candidate(self) -> bool:
        result: bool = False

        containers = self.rows.open + self.columns.open
        for lc in LockedCandidate(containers, self.houses):
            lc: Excluded
            self.evaluate_result(lc)
            if not isinstance(lc, NoOp):
                set_log(
                    msg=f"Excluded {set_excluded(lc.to_exclude)} from:{set_cells(lc.cells)}",
                    level=logging.DEBUG,
                    fn="check_locked_candidate",
                )
                result = True

        return result

    @cleanup
    def check_x_wing(self) -> bool:
        result = False
        self._get_all_bival_cells()

        rows: list[Row] = [row for row in self.rows if not row.solved]
        cols: list[Column] = [col for col in self.columns if not col.solved]

        for xw in XWing(rows, "row"):
            xw: Excluded
            self.evaluate_result(xw)
            if not isinstance(xw, NoOp):
                set_log(
                    msg=f"Excluded {set_excluded(xw.to_exclude)} from:{set_cells(xw.cells)}",
                    level=logging.DEBUG,
                    fn="check_x_wing",
                )
                result = True

        for xw in XWing(cols, "col"):
            xw: Excluded
            self.evaluate_result(xw)
            if not isinstance(xw, NoOp):
                set_log(
                    msg=f"Excluded {set_excluded(xw.to_exclude)} from:{set_cells(xw.cells)}",
                    level=logging.DEBUG,
                    fn="check_x_wing",
                )
                result = True

        return result

    def check_y_wing(self) -> bool:
        result = False

        for yw in YWing(
            self.rows.open, self.columns.open, self.houses.open, self.bivals
        ):
            yw: Excluded
            self.evaluate_result(yw)
            if not isinstance(yw, NoOp):
                set_log(
                    sg=f"Excluded {set_excluded(yw.to_exclude)} from:{set_cells(yw.cells)}",
                    level=logging.DEBUG,
                    fn="check_y_wing",
                )
                result = True

        return result
