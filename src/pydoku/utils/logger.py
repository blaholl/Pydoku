import logging
import sys
from collections.abc import Iterable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..objects import Cell

logger = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="[{generic_func}:{lineno}] - {message}",
    style="{",
)


def set_log(msg: str, level: str = logging.DEBUG, fn: str | None = None) -> None:
    if not fn:
        fn = "funcName"
    logger.log(level=level, msg=msg, extra={"generic_func": fn})


def set_excluded(nums: Iterable[int]) -> str:
    return f"{', '.join(str(i) for i in nums)}"


def set_cells(cells: Iterable[Cell]) -> str:
    return f"\n\t{'\n\t'.join(repr(c) for c in cells)}"
