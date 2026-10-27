import itertools as it
from collections import Counter, UserList
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import Generic

import more_itertools as mi

from .cell import Cell

type T = Generic[T]
type C = Generic[C]


@dataclass
class Sightline:
    idx: int
    row: Row
    col: Column
    house: House


class Container[T](UserList):
    def __init__(self, idx: int, cells: Iterable[Cell]) -> None:
        self.idx = idx
        assert len(cells) == 9
        self.data: list[Cell] = cells
        self._cells: list[Cell] = self.data

        self._open: list[Cell] = [cell for cell in self.data if not cell.solved]
        self._closed: list[Cell] = [cell for cell in self.data if cell.solved]

        self._known: list[int] = []
        self._unknown: list[int] = []

        self._solved: bool = False

    @property
    def solved(self) -> bool:
        return self._solved

    @solved.setter
    def solved(self) -> bool:
        return self.is_solved()

    @property
    def cells(self) -> list[Cell]:
        return self.data

    @cells.setter
    def cells(self) -> list[Cell]:
        self._cells = self.data

    @property
    def open(self) -> list[Cell]:
        return [cell for cell in self.data if not cell.solved]

    @open.setter
    def open(self) -> list[Cell]:
        self._open = [cell for cell in self.data if not cell.solved]

    @property
    def closed(self) -> list[Cell]:
        return [cell for cell in self.data if cell.solved]

    @closed.setter
    def closed(self) -> list[Cell]:
        self._closed = [cell for cell in self.data if cell.solved]

    @property
    def known(self) -> list[int]:
        return [c.solution for c in self.closed]

    @known.setter
    def known(self) -> list[int]:
        if self.closed:
            self._known = [c.solution for c in self.closed]

    @property
    def unknown(self) -> list[int]:
        return sorted(set(range(1, 10)) - set(self.known))

    @unknown.setter
    def unknown(self) -> list[int]:
        self._unknown = sorted(set(range(1, 10)) - set(self.known))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(repr(c) for c in self.data)})"

    def __getitem__(self, i: int) -> Cell:
        if i > 0:
            return self.data[i - 1]
        else:
            return self.data[i]

    def __iter__(self) -> Iterator[Cell]:
        yield from self.cells

    def is_solved(self) -> bool:
        return all([len(self.closed) == 9, all(c.solved for c in self._cells)])

    def _check_open_cells(self) -> list[Cell]:
        self._known = [cell.solution for cell in self.closed]
        self._unknown = sorted(set(range(1, 10)) - set(self.known))

        return [cell for cell in self.cells if not cell.solved]

    def get_counts(self) -> Counter:
        return Counter(it.chain.from_iterable(cell.can for cell in self._open))


class Row[T](Container):
    def __init__(self, idx: int, cells: Iterable[Cell]) -> None:
        super().__init__(idx, cells)
        assert mi.all_equal(cell.row for cell in cells) is True


class Column[T](Container):
    def __init__(self, idx: int, cells: Iterable[Cell]) -> None:
        super().__init__(idx, cells)
        assert mi.all_equal(cell.col for cell in cells) is True


class House[T](Container):
    def __init__(self, idx: int, cells: Iterable[Cell]):
        super().__init__(idx, cells)
        assert mi.all_equal(cell.house for cell in cells) is True


class Containers[C](UserList):
    def __init__(self, containers: list[Container]) -> None:
        self.data: list[Container] = list(containers)
        self._open: list[Container] = []
        self._closed: list[Container] = []

        assert len(self.data) == 9

    def __getitem__(self, i: int) -> Container:
        if i > 0:
            return self.data[i - 1]
        else:
            return self.data[i]

    def __iter__(self) -> Iterator[Container]:
        yield from self.data

    @property
    def open(self) -> list[Container]:
        return [container for container in self if not container.solved]

    @open.setter
    def open(self) -> list[Container]:
        self._open = [container for container in self if not container.solved]

    @property
    def closed(self) -> list[Container]:
        return [container for container in self if container.solved]

    @closed.setter
    def closed(self) -> list[Container]:
        self._closed = [container for container in self if container.solved]


class Rows[C](Containers):
    def __init__(self, rows: list[Row]) -> None:
        super().__init__(rows)


class Columns[C](Containers):
    def __init__(self, columns: list[Column]) -> None:
        super().__init__(columns)


class Houses[C](Containers):
    def __init__(self, houses: list[House]) -> None:
        super().__init__(houses)
