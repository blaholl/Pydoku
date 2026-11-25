# import itertools as it
from collections import defaultdict
from collections.abc import Generator
from typing import TYPE_CHECKING

# import more_itertools as mi
# from pydoku.objects.cell import Cell
# from ..utils.policies import Policy
# from ..objects.containers import Column, Row
from ..utils.result import Excluded, NoOp, Result
from .technique import Technique

if TYPE_CHECKING:
    from ..objects import Cell
    from ..objects.containers import Container, House


class PointingTuple(Technique):
    def __init__(self, container: Container, houses: list[House]) -> None:
        super().__init__(container)
        self.container = container
        self.house = houses

    def __call__(self) -> Generator[Result]:
        pass


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
