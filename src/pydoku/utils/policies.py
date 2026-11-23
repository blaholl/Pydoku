from collections.abc import Iterable
from typing import TYPE_CHECKING

import more_itertools as mi

if TYPE_CHECKING:
    from ..objects import Cell


class Policy:
    @staticmethod
    def is_not_hidden_single(
        k: int = 0, v: int = 0, cell: Cell = None, solutions: list[int] | None = None
    ) -> bool:
        return any([v != 1, k not in cell.can, k in solutions])

    @staticmethod
    def shares_any(c: Iterable[Cell]) -> bool:
        return any(
            [
                mi.all_equal(c, lambda x: x.row),
                mi.all_equal(c, lambda x: x.col),
                mi.all_equal(c, lambda x: x.house),
            ]
        )

    @staticmethod
    def is_triple_candidate(cell: Cell, triple: list[int]) -> bool:
        return len(set(cell.can) | set(triple)) in [2, 3] and set(triple) >= set(
            cell.can
        )

    @staticmethod
    def is_not_intersect_or_subset(combi: list[int], cell: Cell) -> bool:
        intersect = set(combi) & set(cell.can)
        return all(
            [
                len(intersect) >= 1,
                intersect <= set(combi),
            ]
        )
