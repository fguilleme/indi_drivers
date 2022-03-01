#!/usr/bin/python3
import sys
from teletrak import *

logger.debug("%s", *sys.argv)
logger.setLevel(logging.INFO)
with init() as ser:
    if not is_alive(ser):
        sys.exit(1)

sys.exit(0)

