#!/usr/bin/python3
import sys
from teletrak import *

logger.debug("%s %s %s", *sys.argv)
script, ra, dec = sys.argv

with init() as ser:
    if not is_alive(ser):
        sys.exit(1)

    if is_goto_running(ser):
        cancel_goto(ser)

    logger.debug("goto %s %s", ra, dec)
    resp = goto_ra_dec(ser, float(ra), float(dec))

sys.exit(1)
