import logging
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="[%(filename)s - %(funcName)s] %(message)s",
)
