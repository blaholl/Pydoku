# import itertools as it
from collections import defaultdict
from collections.abc import Generator
from typing import TYPE_CHECKING

import more_itertools as mi

from ..objects.containers import Column, Row
from ..utils.policies import Policy
from ..utils.result import Excluded, NoOp, Result
from .technique import Technique

if TYPE_CHECKING:
    from ..objects import Cell
    from ..objects.containers import Container


class LockedCandidate(Technique):
    def __init__(self, container: Container, intersects: list[Container]) -> None:
        super().__init__(container)
        self.house = container
        self.intersects = intersects

    def __call__(self) -> Generator[Result]:
        for container in self.intersects:
            counts = [k for k, v in self.house.get_counts().items() if v > 3]
            if not counts:
                continue

            for k in counts:
                groups: dict[int, list[Cell]] = defaultdict(list)
                cells = [cell for cell in container.open if k in cell]
                for cell in cells:
                    groups[cell.house].append(cell)

                if len(groups) != 1:
                    continue

                candidate_cells = groups.get(self.house.idx)
                if not candidate_cells or len(candidate_cells) not in [2, 3]:
                    continue

                to_exclude: set[int] = {k}
                exclusion_cells = [
                    cell for cell in self.house.open if cell not in candidate_cells
                ]

                yield Excluded(cells=exclusion_cells, to_exclude=to_exclude)

            yield NoOp()


class PointingTuple(Technique):
    def __init__(self, container: Container, intersects: list[Container]) -> None:
        super().__init__(container)
        self.house = container
        self.intersects = intersects

    def __call__(self) -> Generator[Result]:
        for container in self.intersects:
            candidate_cells: list[Cell] = []
            counts = {k: v for k, v in self.house.get_counts().items() if v in [2, 3]}

            if not counts:
                continue

            for k in counts:
                cells = [cell for cell in self.house.open if k in cell]
                if not cells:
                    continue

                one_row, one_col = self.get_container_ids(cells)
                if not (one_row or one_col):
                    continue

                if sum(self.set_groups(k, container.group_by_house())) <= 1:
                    continue

                con_counts = {
                    k: v
                    for k, v in container.get_counts().items()
                    if Policy.is_container_count_ge_house_count(k, v, counts)
                }

                if not con_counts:
                    continue

                if one_row and isinstance(container, Row):
                    candidate_cells = [
                        c for c in self.house if k in c and c.row == container.idx
                    ]
                if one_col and isinstance(container, Column):
                    candidate_cells = [
                        c for c in self.house if k in c and c.col == container.idx
                    ]

                if not candidate_cells:
                    continue

                to_exclude: set[int] = {k}
                exclusion_cells = [
                    cell
                    for cell in container.open
                    if cell not in candidate_cells and k in cell
                ]

                print(k, exclusion_cells)
                yield Excluded(exclusion_cells, to_exclude)

            yield NoOp()

    def get_container_ids(self, cells: list[Cell]) -> tuple[bool]:
        row_ids = [c.row for c in cells]
        col_ids = [c.col for c in cells]

        return mi.all_equal(row_ids), mi.all_equal(col_ids)

    def set_groups(self, k: int, groups: dict[int, list[Cell]]) -> list[bool]:
        sets: list[bool] = []
        for group in groups.values():
            sets.append(any(k in c for c in group))

        return sets
