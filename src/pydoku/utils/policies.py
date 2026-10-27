from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..objects import Cell


class Policy:
    @staticmethod
    def is_not_hidden_single(k: int, v: int, cell: Cell, solutions: list[int]) -> bool:
        return any([v != 1, k not in cell.can, k in solutions])
