import itertools as it
from collections import Counter
from collections.abc import Generator
from typing import TYPE_CHECKING

import more_itertools as mi

from ..utils.policies import Policy
from .technique import Technique

if TYPE_CHECKING:
    from ..objects import Cell
    from ..objects.containers import Container


class NakedSingle(Technique):
    @staticmethod
    def check(container: Container) -> Generator[Cell]:
        for cell in container.open:
            if len(cell) != 1:
                continue
            cell.solve(mi.only(cell.can))
            yield cell


class HiddenSingle(Technique):
    @staticmethod
    def check(container: Container) -> Generator[Cell]:
        counts: Counter = container.get_counts()
        if 1 not in counts.values():
            pass
        for (k, v), cell in it.product(counts.items(), container.open):
            if Policy.is_not_hidden_single(k, v, cell, container.known):
                continue

            cell.solve(k)
            yield cell
