import itertools as it

# from collections import Counter
from collections.abc import Generator
from typing import TYPE_CHECKING

import more_itertools as mi

# from ..utils.policies import Policy
from .technique import Technique

if TYPE_CHECKING:
    from ..objects import Cell
    from ..objects.containers import Container


class NakedDouble(Technique):
    @staticmethod
    def check(container: Container) -> Generator[Cell]:
        candidate_cells: list[tuple[Cell]] = list(
            mi.flatten(it.product(cell for cell in container.open if cell.bival))
        )
        if len(candidate_cells) != 2 or not mi.all_equal(candidate_cells):
            pass
        else:
            to_exclude: set[int] = set(mi.flatten(c.can for c in candidate_cells))
            exclusion_cells = [
                cell for cell in container.open if cell not in candidate_cells
            ]
            for cell, num in it.product(exclusion_cells, to_exclude):
                cell.pop(num)

            yield len(exclusion_cells)


class HiddenDouble(Technique):
    @staticmethod
    def check(): ...
