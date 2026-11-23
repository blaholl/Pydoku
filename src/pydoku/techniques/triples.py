import itertools as it
from collections.abc import Generator
from functools import cache, reduce
from typing import TYPE_CHECKING

import more_itertools as mi

from ..utils.policies import Policy
from ..utils.result import Excluded, NoOp, Result
from .technique import Technique

if TYPE_CHECKING:
    from ..objects import Cell
    from ..objects.containers import Container


@cache
class NakedTriple(Technique):
    def __init__(self, container: Container) -> None:
        super().__init__(container)
        self.container = container

    def __call__(self) -> Generator[Result]:
        groups = [cell for cell in self.container.open if len(cell) in [2, 3]]
        candidate_cells: list[Cell] = []

        for combi in it.combinations(groups, 3):
            target = list(reduce(set.union, [set(c.can) for c in combi]))

            if len(target) != 3:
                continue

            for cell, triple in it.product(groups, [target]):
                if not Policy.is_triple_candidate(cell, triple):
                    continue

                candidate_cells.append(cell)

            if not candidate_cells:
                continue

            to_exclude: set[int] = set(mi.flatten(c.can for c in candidate_cells))
            exclusion_cells = [
                cell for cell in self.container.open if cell not in candidate_cells
            ]

            yield Excluded(exclusion_cells, to_exclude)


@cache
class HiddenTriple(Technique):
    def __init__(self, container: Container) -> None:
        super().__init__(container)
        self.container = container

    def __call__(self) -> Generator[Result]:
        candidates: list[int] = []
        counts = self.container.get_counts()

        for k, v in counts.items():
            if v not in [2, 3]:
                continue
            candidates.append(k)

        if not candidates or len(candidates) < 3:
            return NoOp()

        for combi in it.combinations(candidates, 3):
            candidate_cells: list[Cell] = []
            for cell in self.container.open:
                if not Policy.is_intersect_and_subset(combi, cell):
                    continue

                candidate_cells.append(cell)

            if len(candidate_cells) != 3:
                continue

            to_exclude: set[int] = set(
                mi.flatten(set(c.can) - set(combi) for c in candidate_cells)
            )

            yield Excluded(candidate_cells, to_exclude)
