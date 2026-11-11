from collections.abc import Iterable
from typing import TYPE_CHECKING

import more_itertools as mi

if TYPE_CHECKING:
    from ..objects import Cell


class Policy:
    @staticmethod
    def is_not_hidden_single(k: int, v: int, cell: Cell, solutions: list[int]) -> bool:
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
