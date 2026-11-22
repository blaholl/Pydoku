import itertools as it

# from collections import Counter
from collections.abc import Generator
from functools import reduce
from typing import TYPE_CHECKING

import more_itertools as mi

from ..utils.policies import Policy
from ..utils.result import Excluded, NoOp, Result
from .technique import Technique

if TYPE_CHECKING:
    from ..objects import Cell
    from ..objects.containers import Container


class NakedTriple(Technique):
    def __init__(self, container: Container) -> None:
        super().__init__(container)
        self.container = container

    def __call__(self) -> Generator[Result]:
        groups = [cell for cell in self.container.open if len(cell) in [2, 3]]
        triples: list[int] = []
        candidate_cells: list[Cell] = []

        combis = it.combinations(groups, 3)
        for i, combi in enumerate(combis):
            target = list(reduce(set.union, [set(c.can) for c in combi]))

            if len(target) != 3:
                continue

            triples.append(target)

            for cell, triple in it.product(groups, triples):
                if not Policy.is_triple_candidate(cell, triple):
                    continue

                candidate_cells.append(cell)

            if not candidate_cells:
                return NoOp()

            to_exclude: set[int] = set(mi.flatten(c.can for c in candidate_cells))
            exclusion_cells = [
                cell for cell in self.container.open if cell not in candidate_cells
            ]

            yield Excluded(exclusion_cells, to_exclude)


class HiddenTriple(Technique):
    def __init__(self, container: Container) -> None:
        super().__init__(container)
        self.container = container

    def __call__(self) -> Generator[Result]:
        pass
