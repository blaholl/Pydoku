from .doubles import HiddenDouble as HiddenDouble
from .doubles import NakedDouble as NakedDouble
from .quadruples import HiddenQuadruple as HiddenQuadruple
from .quadruples import NakedQuadruple as NakedQuadruple
from .singles import HiddenSingle as HiddenSingle
from .singles import NakedSingle as NakedSingle
from .triples import HiddenTriple as HiddenTriple
from .triples import NakedTriple as NakedTriple
from .tuples import LockedCandidate as LockedCandidate
from .tuples import PointingTuple as PointingTuple
from .wings import XWing as XWing
from .wings import YWing as YWing

__all__ = [
    "HiddenDouble",
    "HiddenQuadruple",
    "HiddenSingle",
    "HiddenTriple",
    "LockedCandidate",
    "NakedDouble",
    "NakedQuadruple",
    "NakedSingle",
    "NakedTriple",
    "PointingTuple",
    "XWing",
    "YWing",
]
