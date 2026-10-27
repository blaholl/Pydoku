# import itertools as it
# from collections import Counter
# from collections.abc import Generator
# from typing import TYPE_CHECKING

# import more_itertools as mi

# from ..utils.policies import Policy
from .technique import Technique

# if TYPE_CHECKING:
#     from ..objects import Cell
#     from ..objects.containers import Container


class NakedQuadruple(Technique):
    @staticmethod
    def check(): ...


class HiddenQuadruple(Technique):
    @staticmethod
    def check(): ...
