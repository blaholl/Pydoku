from collections.abc import Generator
from typing import TYPE_CHECKING

import more_itertools as mi

from ..objects.containers import Column, Row
from ..utils.logger import logger
from ..utils.policies import Policy
from ..utils.result import Excluded, NoOp, Result
from .technique import Technique

if TYPE_CHECKING:
    from ..objects import Cell
    from ..objects.containers import Columns, Container, House, Houses, Rows


class LockedCandidate(Technique):
    def __init__(self, containers: Columns | Rows, houses: Houses) -> None:
        super().__init__(containers)
        self.containers = containers
        self.houses = houses

    def __call__(self) -> Generator[Result, None, NoOp]:
        for container in self.containers:
            counts = {k: v for k, v in container.get_counts().items() if v >= 2}
            if not counts:
                continue

            for k, v in counts.items():
                candidate_cells = [cell for cell in container.open if k in cell]
                if not candidate_cells:
                    continue

                h: list[int] = [c.house for c in candidate_cells]
                if not mi.all_equal(h):
                    continue
                house: House = self.houses[mi.only(set(h))]
                h_counts = {
                    h_k: h_v for h_k, h_v in house.get_counts().items() if h_v >= 3
                }

                if h_counts.get(k, 0) <= v:
                    continue

                to_exclude: set[int] = {k}
                exclusion_cells: list[Cell] = [
                    c for c in house.open if c not in candidate_cells
                ]

                logger.debug("Locked Candidate")
                logger.debug(f"{container.__class__.__name__} {container.idx}")
                logger.debug(f"House {house.idx}")
                logger.debug(to_exclude)
                logger.debug(f"{'\n'.join(repr(c) for c in exclusion_cells)}")

                yield Excluded(cells=exclusion_cells, to_exclude=to_exclude)

            yield NoOp()


class PointingTuple(Technique):
    def __init__(self, container: Container, intersects: list[Container]) -> None:
        super().__init__(container)
        self.house = container
        self.intersects = intersects

    def __call__(self) -> Generator[Result]:
        for container in self.intersects:
            counts = {k: v for k, v in self.house.get_counts().items() if v in [2, 3]}

            if not counts:
                continue

            for k, v in counts.items():
                candidate_cells: list[Cell] = []
                cells = [cell for cell in self.house.open if k in cell]
                if not cells:
                    continue

                one_row, one_col = self.get_container_ids(cells)
                if not (one_row or one_col) or mi.all_equal((one_row, one_col)):
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
                        c for c in self.house.open if k in c and c.row == container.idx
                    ]
                elif one_col and isinstance(container, Column):
                    candidate_cells = [
                        c for c in self.house.open if k in c and c.col == container.idx
                    ]

                if (
                    not candidate_cells
                    or len(candidate_cells) not in [2, 3]
                    or v > len(candidate_cells)
                ):
                    continue

                to_exclude: set[int] = {k}
                exclusion_cells = [
                    cell
                    for cell in container.open
                    if cell not in candidate_cells and k in cell
                ]

                if not exclusion_cells:
                    continue

                logger.debug("Pointing tuple")
                logger.debug(f"House {self.house.idx}")
                logger.debug(f"{container.__class__.__name__} {container.idx}")
                logger.debug(to_exclude)
                logger.debug(f"{'\n'.join(repr(c) for c in exclusion_cells)}")

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
