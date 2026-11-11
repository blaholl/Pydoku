from collections.abc import Iterable
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from ..objects import Cell


class Result(Protocol): ...


class Solved(Result):
    def __init__(self, cell: Cell) -> None:
        self.cell = cell


class Excluded(Result):
    def __init__(
        self,
        cells: Iterable[Cell],
        to_exclude: Iterable[int],
    ) -> None:
        self.cells: Iterable[Cell] = cells
        self.to_exclude: Iterable[int] = to_exclude


class NoOp(Result):
    def __init__(self) -> None:
        pass
