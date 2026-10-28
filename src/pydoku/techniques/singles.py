import itertools as it
from collections import Counter
from collections.abc import Generator
from typing import TYPE_CHECKING

import more_itertools as mi

from ..utils.policies import Policy
from ..utils.result import NoOp, Result, Solved
from .technique import Technique

if TYPE_CHECKING:
    from ..objects.containers import Container


class NakedSingle(Technique):
    def __init__(self, container: Container) -> None:
        self.container = container

    def __call__(self) -> Generator[Result]:
        for cell in self.container:
            if len(cell) != 1:
                continue
            cell.solve(mi.only(cell.can))
            yield Solved(cell)


class HiddenSingle(Technique):
    def __init__(self, container: Container) -> None:
        self.container = container

    def __call__(self) -> Generator[Result]:
        counts: Counter = self.container.get_counts()
        if 1 not in counts.values():
            return NoOp()
        for (k, v), cell in it.product(counts.items(), self.container.open):
            if Policy.is_not_hidden_single(k, v, cell, self.container.known):
                continue

            cell.solve(k)
            yield Solved(cell)
