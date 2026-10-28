import itertools as it

# from collections import Counter
from collections.abc import Generator
from typing import TYPE_CHECKING

import more_itertools as mi

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
        self.container = container

    def __call__(self) -> Generator[Result]:
        """Searches for Naked Double :class:`Cell` objects and removes those values from other cells in their shared :class:`Container`.

        Yields:
            Generator[Result]: Number of :class:`Cell` objects from which the naked double values were removed.
        """
        candidate_cells: list[tuple[Cell]] = list(
            mi.flatten(it.product(cell for cell in self.container.open if cell.bival))
        )
        if len(candidate_cells) != 2 or not mi.all_equal(candidate_cells):
            yield NoOp()
        else:
            to_exclude: set[int] = set(mi.flatten(c.can for c in candidate_cells))
            exclusion_cells = [
                cell for cell in self.container.open if cell not in candidate_cells
            ]

            yield Excluded(exclusion_cells, to_exclude)


class HiddenDouble(Technique):
    def __init__(self, container: Container) -> None:
        self.container = container

    def __call__(self) -> Generator[Result]: ...
