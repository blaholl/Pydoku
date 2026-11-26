import itertools as it
from collections import Counter, UserList, defaultdict
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from typing import Generic

import more_itertools as mi

from .cell import Cell

type T = Generic[T]
type C = Generic[C]


@dataclass
class Sightline:
    row: Row
    col: Column
    house: House
    idx: int = None

    _open: Iterator[Cell] = field(default_factory=list)
    _solved: Iterator[Cell] = field(default_factory=list)

    @property
    def open(self) -> Iterator[Cell]:
        return mi.flatten([self.row.open, self.col.open, self.house.open])

    @open.setter
    def open(self) -> Iterator[Cell]:
        self._open = mi.flatten([self.row.open, self.col.open, self.house.open])

    @property
    def solved(self) -> Iterator[Cell]:
        return mi.flatten([self.row.open, self.col.open, self.house.open])

    @solved.setter
    def solved(self) -> Iterator[Cell]:
        self._solved = mi.flatten([self.row.open, self.col.open, self.house.open])

    def propogate(self, ans: int) -> None:
        for cell in self.open:
            cell.pop(ans)


@dataclass
class StrongLink:
    link: int
    cell_1: Cell
    cell_2: Cell

    row: bool | None = None
    col: bool | None = None
    house: bool | None = None
    diagonal: bool | None = None

    def __post_init__(self) -> None:
        self.row = self.cell_1.row == self.cell_2.row
        self.col = self.cell_1.col == self.cell_2.col
        self.house = self.cell_1.house == self.cell_2.house
        self.diagonal = all([self.house is True, self.row is False, self.col is False])

    def __eq__(self, other: StrongLink) -> bool:
        return self.cell_1 == other.cell_1 and self.cell_2 == other.cell_2

    def __hash__(self) -> int:
        return hash(self)

    def get_cells(self) -> tuple[Cell, Cell]:
        return self.cell_1, self.cell_2


class Container[T](UserList):
    def __init__(self, idx: int, cells: Iterable[Cell]) -> None:
        self.idx: int = idx
        assert len(cells) == 9
        self.data: list[Cell] = cells
        self._cells: list[Cell] = self.data

        self._open: list[Cell] = [cell for cell in self.data if not cell.solved]
        self._closed: list[Cell] = [cell for cell in self.data if cell.solved]

        self._known: list[int] = []
        self._unknown: list[int] = []

        self._solved: bool = False

        self.cache: dict[dict[str, list[Cell]]] = defaultdict(None, defaultdict(list))

        self._strong_links: list[StrongLink] = []

    @property
    def solved(self) -> bool:
        return self._solved

    @solved.setter
    def solved(self) -> bool:
        self._solved = self.is_solved()

    @property
    def cells(self) -> list[Cell]:
        return self.data

    @property
    def open(self) -> list[Cell]:
        return [cell for cell in self.data if not cell.solved]

    @open.setter
    def open(self) -> list[Cell]:
        self._open = [cell for cell in self.data if not cell.solved]

    @property
    def closed(self) -> list[Cell]:
        return [cell for cell in self.data if cell.solved]

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

    @property
    def strong_links(self) -> list[StrongLink]:
        return self.get_strong_links()

    @strong_links.setter
    def strong_links(self) -> None:
        self._strong_links = self.get_strong_links()

    def __hash__(self) -> int:
        return hash((self.idx, *self.cells))

    def __eq__(self, other: Container) -> bool:
        return all([self.idx == other.idx, self.cells == other.cells])

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
        return all(
            [
                len(self.closed) == 9,
                all(c.solved for c in self._cells),
                len({c.solution for c in self._cells}) == 9,
            ]
        )

    def _check_open_cells(self) -> list[Cell]:
        self._known = [cell.solution for cell in self.closed]
        self._unknown = sorted(set(range(1, 10)) - set(self.known))

        return [cell for cell in self.cells if not cell.solved]

    def get_counts(self) -> Counter:
        return Counter(it.chain.from_iterable(cell.can for cell in self._open))

    def get_strong_links(self) -> list[StrongLink]:
        for k, v in self.get_counts().items():
            if v != 2:
                continue
            pairs: list[Cell] = []
            for cell in self._open:
                if k in cell:
                    pairs.append(cell)
            if len(pairs) != 2:
                continue

            s_link = StrongLink(link=k, cell_1=pairs[0], cell_2=pairs[1])
            self._strong_links.append(s_link)
        return self._strong_links

    def group_by_house(self) -> dict[int, list[Cell]]:
        groups: dict[int, list[Cell]] = defaultdict(list)

        for cell in self.open:
            groups[cell.house].append(cell)

        return groups


class Row[T](Container):
    def __init__(self, idx: int, cells: Iterable[Cell]) -> None:
        super().__init__(idx, cells)
        assert mi.all_equal(cell.row for cell in cells) is True
        self.intersections: list[int] = self._get_intersections()

    def _get_intersections(self) -> list[int]:
        return sorted({c.house for c in self.cells})


class Column[T](Container):
    def __init__(self, idx: int, cells: Iterable[Cell]) -> None:
        super().__init__(idx, cells)
        assert mi.all_equal(cell.col for cell in cells) is True
        self.intersections: list[int] = self._get_intersections()

    def _get_intersections(self) -> list[int]:
        return sorted({c.house for c in self.cells})


class House[T](Container):
    def __init__(self, idx: int, cells: Iterable[Cell]) -> None:
        super().__init__(idx, cells)
        assert mi.all_equal(cell.house for cell in cells) is True
        self.row_intersections: list[int] = self._get_row_intersections()
        self.col_intersections: list[int] = self._get_col_intersections()

    def _get_row_intersections(self) -> list[int]:
        return sorted({c.row for c in self.cells})

    def _get_col_intersections(self) -> list[int]:
        return sorted({c.col for c in self.cells})


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


@dataclass
class PhistomefelRing:
    outer: list[int]
    inner: list[int]

    outer_count: Counter | None = None
    inner_count: Counter | None = None

    def __post_init__(self) -> None:
        self.outer_count = Counter(self.outer)
        self.inner_count = Counter(self.inner)

    def compare(self) -> bool:
        return all(
            [
                len(self.inner) == len(self.outer),
                sorted(self.inner) == sorted(self.outer),
            ]
        )

    def diff(self) -> int:
        return abs(len(self.outer) - len(self.inner))

    def count_diff(self) -> dict[int, int]:
        diffs: dict[int, int] = {}

        for k, v in self.outer_count.items():
            if k not in self.inner_count:
                diffs[k] = v

            elif self.inner_count[k] != v:
                diffs[k] = v - self.inner_count[k]

        return diffs


@dataclass
class NumCounts:
    total: int
    open: int
    closed: int
    rows: int
    cols: int
    houses: int


class Number:
    def __init__(self, value: int) -> None:
        self.value = value
        self._open: list[Cell] = []
        self._closed: list[Cell] = []
        self._solved: bool = False
        self._counts: NumCounts = None
        self._strong_links: list[StrongLink] = []
        self._doubles: list[Container]

    @property
    def open(self) -> list[Cell]:
        return self._open

    @open.setter
    def open(self, containers: list[Container]) -> None:
        for con in containers:
            for c in con:
                if not c.solved and self.value in c:
                    self._open.append(c)

    @property
    def closed(self) -> list[Cell]:
        return self._closed

    @closed.setter
    def closed(self, containers: list[Container]) -> None:
        for con in containers:
            for c in con:
                if c.solved and self.value == c.solution:
                    self._closed.append(c)

    @property
    def solved(self) -> bool:
        return len(self.closed) == 9

    @property
    def strong_links(self) -> list[StrongLink]:
        return self._strong_links

    @strong_links.setter
    def strong_links(self, containers: list[Container]) -> None:
        for con in containers:
            if not con.strong_links:
                continue
            for sl in con.strong_links:
                if self.value == sl.link:
                    self._strong_links.append(sl)
