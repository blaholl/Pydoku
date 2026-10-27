from collections.abc import Iterable
from dataclasses import dataclass
from functools import singledispatchmethod

from ..utils import EmptyCellError, IllegalAnswerError


@dataclass
class Loc:
    r: int
    c: int
    h: int

    def __eq__(self, other: tuple[int]) -> bool:
        return (self.r, self.c, self.h) == other


class Cell:
    def __init__(
        self,
        idx: int,
        coords: tuple[int],
        solved: bool = False,
        solution: int | None = None,
    ) -> None:
        self.idx: int = idx
        self.pos: Loc = Loc(*coords)
        self.row: int = self.pos.r
        self.col: int = self.pos.c
        self.house: int = self.pos.h

        self.initial: bool = False

        self.solved: bool = solved
        self.solution: int | None = solution

        self._exc: set[int] = set()
        self._can: set[int] = set()
        self._bival: bool = False

    @property
    def exc(self) -> list[int]:
        if not self.solved:
            return sorted(self._exc)
        return []

    @exc.setter
    def exc(self, other: int | set[int]) -> set[int]:
        if not self.solved:
            if isinstance(other, int):
                self._exc = self._exc.add(other)
            elif isinstance(other, set):
                self._exc |= other

    @property
    def can(self) -> list[int] | int:
        if not self.solved:
            return sorted(self._can)
        return []

    @can.setter
    def can(self, other: int | set[int]) -> set[int]:
        if not self.solved:
            if isinstance(other, int):
                self._can = self._can.add(other)
            elif isinstance(other, set):
                self._can |= other

    @property
    def bival(self) -> bool:
        return len(self._can) == 2

    @bival.setter
    def bival(self) -> bool:
        self._bival = self.bival

    def __repr__(self) -> str:
        base: str = f"{self.__class__.__name__}(idx={self.idx}, row={self.pos.r}, column={self.pos.c}, house={self.pos.h}, can={self.can}, exc={self.exc}"
        if self.initial:
            return (
                base
                + f", solved={self.solved}, solution={self.solution}, initial={self.initial})"
            )
        elif self.solved:
            return base + f", solved={self.solved}, solution={self.solution})"
        elif self.bival:
            return base + f", bival={self.bival})"
        else:
            return base + ")"

    def __str__(self) -> str:
        if self.solved:
            return str(self.solution)
        return f"[{','.join(str(c) for c in self.can)}] / [{','.join(str(e) for e in self.exc)}]"

    def __eq__(self, other: Cell) -> bool:
        return self.can == other.can

    def __contains__(self, i: int) -> bool:
        return i in self.can

    def __len__(self) -> int:
        return len(self.can)

    @singledispatchmethod
    def pop(self, can: int) -> None:
        if not self._can:
            raise EmptyCellError(f"Cell {self.pos!r} is empty")

        if can in self._can:
            self._can.remove(can)
            self._exc.add(can)

    @pop.register(Iterable)
    def _(self, can: Iterable[int]) -> None:
        for c in can:
            if not self._can:
                raise EmptyCellError(f"Cell {self.pos!r} is empty")

            if c in self._can:
                self._can.remove(c)
                self._exc.add(c)

    def solve(self, answer: int | None) -> None:
        """Sets :attr:`self.solution` and :attr:`self.solved` if the passed ``answer`` argument is not in :attr:`self.exc`.

        Otherwise, raises :exc:`IllegalAnswerError`.

        Zeroes out :attr:`self.exc` and :attr:`self.can`.

        Args:
            answer (int): :type:`int` representing the solution to the :class:`Cell`.

        Raises:
            IllegalAnswerError: Raises when ``answer`` is found in :attr:`self.exc`.
        """
        if answer == 0:
            pass
        elif answer not in self._exc:
            self.solution = answer
            self.solved = True
            self._can = set()
            self._exc = set()
        else:
            raise IllegalAnswerError(
                f"{answer} is in Cell({self.pos!s})'s exclusion list"
            )

    def sees(self, other: Cell) -> bool:
        return any(
            [self.row == other.row, self.col == other.col, self.house == other.house]
        )

    def shares_row(self, other: Cell) -> bool:
        return self.row == other.row

    def shares_col(self, other: Cell) -> bool:
        return self.col == other.col

    def shares_house(self, other: Cell) -> bool:
        return self.house == other.house
