import itertools as it
from collections import Counter
from collections.abc import Generator
from typing import TYPE_CHECKING

import more_itertools as mi

from ..utils import set_excluded, set_log
from ..utils.result import Excluded, NoOp, Result
from .technique import Technique

if TYPE_CHECKING:
    from ..objects import Cell
    from ..objects.containers import Container


class NakedDouble(Technique):
    """Callable object to find Naked Doubles in a :class:`Container`.

    Args:
        container (Container): :class:`Container` to search for Naked Doubles.
    """

    def __init__(self, container: Container) -> None:
        super().__init__(container)
        self.container = container

    def __call__(self) -> Generator[Result]:
        """Searches for Naked Double :class:`Cell` objects and removes those values from other cells in their shared :class:`Container`.

        Yields:
            Generator[Result]: Number of :class:`Cell` objects from which the naked double values were removed.
        """
        candidate_cells: list[Cell] = list(
            mi.flatten(it.product(cell for cell in self.container.open if cell.bival))
        )
        if len(candidate_cells) < 2:
            yield NoOp()

        if len(candidate_cells) > 2:
            for g in it.combinations(candidate_cells, r=2):
                if not mi.all_equal(g):
                    continue
                candidate_cells = list(g)

        if len(candidate_cells) != 2 or not mi.all_equal(candidate_cells):
            yield NoOp()
        else:
            to_exclude: set[int] = set(mi.flatten(c.can for c in candidate_cells))
            exclusion_cells = [
                cell for cell in self.container.open if cell not in candidate_cells
            ]

            set_log(
                msg=f"{self.container.__class__.__name__} {self.container.idx} | {set_excluded(to_exclude)}",
                fn="naked_double",
            )

            yield Excluded(exclusion_cells, to_exclude)


class HiddenDouble(Technique):
    def __init__(self, container: Container) -> None:
        super().__init__(container)
        self.container = container

    def __call__(self) -> Generator[Result]:
        counts: Counter = {
            k: v for k, v in self.container.get_counts().items() if v == 2
        }
        if len(counts) < 2:
            return NoOp()

        combis: list[tuple[int]] = it.combinations(counts.keys(), 2)

        if not combis:
            return NoOp()

        for combi in combis:
            candidate_cells: list[Cell] = [
                c for c in self.container.open if set(combi) <= set(c.can)
            ]
            if len(candidate_cells) != 2:
                continue

            to_exclude: set[int] = set(
                mi.flatten(set(c.can) - set(combi) for c in candidate_cells)
            )

            set_log(
                msg=f"{self.container.__class__.__name__} {self.container.idx} | {set_excluded(combi)}",
                fn="hidden_double",
            )

            yield Excluded(candidate_cells, to_exclude)
