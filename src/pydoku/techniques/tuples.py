# import itertools as it
# from collections import Counter
from collections.abc import Generator
from typing import TYPE_CHECKING

# import more_itertools as mi
# from ..utils.policies import Policy
from ..utils.result import Result  # Excluded, NoOp, Result
from .technique import Technique

if TYPE_CHECKING:
    # from ..objects import Cell
    from ..objects.containers import Container


class LockedCandidate(Technique):
    def __init__(self, container: Container) -> None:
        super().__init__(container)
        self.container = container

    def __call__(self) -> Generator[Result]:
        pass


class PointingTuple(Technique):
    def __init__(self, container: Container) -> None:
        super().__init__(container)
        self.container = container

    def __call__(self) -> Generator[Result]:
        pass
