import sys

from loguru import logger

logger.add(sys.stderr, format="{time} {message} -> {level}", filter="pydoku")
