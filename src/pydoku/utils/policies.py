from collections.abc import Iterable
from typing import TYPE_CHECKING

import more_itertools as mi

if TYPE_CHECKING:
    from ..objects import Cell
    from ..objects.containers import StrongLink


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
    def is_intersect_and_subset(combi: list[int], cell: Cell) -> bool:
        intersect = set(combi) & set(cell.can)
        return all(
            [
                len(intersect) >= 1,
                intersect <= set(combi),
            ]
        )

    @staticmethod
    def is_container_count_ge_house_count(
        k: int, v: int, counts: dict[int, int]
    ) -> bool:
        if k not in counts:
            return
        return v >= 3 and v >= counts.get(k)

    @staticmethod
    def is_x_wing_candidate(
        link_1: StrongLink, link_2: StrongLink, container_type: str
    ) -> bool:
        l_cell_1, l_cell_2 = link_1.get_cells()
        r_cell_1, r_cell_2 = link_2.get_cells()

        match container_type:
            case "row":
                con_1, con_2 = (
                    (l_cell_1.col, r_cell_1.col),
                    (l_cell_2.col, r_cell_2.col),
                )
            case "col":
                con_1, con_2 = (
                    (l_cell_1.row, r_cell_1.row),
                    (l_cell_2.row, r_cell_2.row),
                )

        return all(
            [
                mi.all_equal(con_1),
                mi.all_equal(con_2),
                mi.all_unique(
                    [l_cell_1.house, l_cell_2.house, r_cell_1.house, r_cell_2.house]
                ),
            ]
        )
