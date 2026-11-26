import itertools as it
from collections.abc import Generator
from typing import TYPE_CHECKING

import more_itertools as mi

from ..utils.policies import Policy
from ..utils.result import Excluded, NoOp, Result
from .technique import Technique

if TYPE_CHECKING:
    from ..objects import Cell
    from ..objects.containers import Container, StrongLink


class XWing(Technique):
    def __init__(self, containers: list[Container], container_type: str) -> None:
        super().__init__(containers)
        self.containers = containers
        self.container_type = container_type

    def __call__(self) -> Generator[Result]:
        links: list[StrongLink] = list(
            mi.flatten(con.strong_links for con in self.containers)
        )
        if not links:
            return NoOp()

        for link_1, link_2 in it.product(links, repeat=2):
            if link_1.link != link_2.link or link_1 == link_2:
                continue

            if not Policy.is_x_wing_candidate(link_1, link_2, self.container_type):
                continue

            to_exclude: set[int] = {link_1.link}
            exclusion_cells: list[Cell] = []

            cell_1, cell_2 = link_1.get_cells()
            cell_3, cell_4 = link_2.get_cells()
            candidates: list[Cell] = [cell_1, cell_2, cell_3, cell_4]
            match self.container_type:
                case "row":
                    for cell in candidates:
                        exclusion_cells.extend(
                            [c for c in cell.sightline.col.open if link_1.link in c]
                        )
                case "col":
                    for cell in candidates:
                        exclusion_cells.extend(
                            [c for c in cell.sightline.row.open if link_1.link in c]
                        )

            exclusions: set[Cell] = set(exclusion_cells) - set(candidates)
            if not exclusions:
                continue

            yield Excluded(exclusions, to_exclude)

        yield NoOp()
