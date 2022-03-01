#!/usr/bin/python3
import sys
from teletrak import *

script, path = sys.argv

logger.setLevel(logging.INFO)
logger.debug("%s %s", *sys.argv)

with init() as ser:
    if not is_alive(ser):
        sys.exit(1)

    if is_goto_running(ser):
        cancel_goto(ser)

    ra, dec = get_ra_dec(ser)
    logger.debug(f'RA = {ra}, DEC = {dec}')

    ra, dec = get_ra_dec32(ser)
    logger.debug(f'RA = {ra}, DEC = {dec}')

    print(f'0 {ra} {dec}', file=open(path, "w"))
    sys.exit(0)

sys.exit(1)
