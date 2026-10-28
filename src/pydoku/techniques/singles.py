import itertools as it
from collections import Counter
from collections.abc import Callable, Generator
from typing import TYPE_CHECKING

import more_itertools as mi

from ..utils.policies import Policy
from .technique import Technique

if TYPE_CHECKING:
    from ..objects import Cell
    from ..objects.containers import Container


class NakedSingle(Technique):
    def __init__(self, container: Container) -> None:
        self.container = container

    def __call__(self) -> Generator[Cell]:
        for cell in self.container:
            if len(cell) != 1:
                continue
            cell.solve(mi.only(cell.can))
            yield cell

    def __iter__(self) -> Generator[Callable[..., Cell]]:
        yield from self.__call__()


class HiddenSingle(Technique):
    def __init__(self, container: Container) -> None:
        self.container = container

    def __call__(self) -> Generator[Cell]:
        counts: Counter = self.container.get_counts()
        if 1 not in counts.values():
            return None
        for (k, v), cell in it.product(counts.items(), self.container.open):
            if Policy.is_not_hidden_single(k, v, cell, self.container.known):
                continue

            cell.solve(k)
            yield cell

    def __iter__(self) -> Generator[Callable[..., Cell | None]]:
        yield from self.__call__()
