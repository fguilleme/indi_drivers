#!/usr/bin/python3
import sys
from teletrak import *

logger.debug("%s", *sys.argv)

with init() as ser:
    if not is_alive(ser):
        sys.exit(1)

    if is_goto_running(ser):
        cancel_goto(ser)

    logger.debug("send reset az")
    cmd = reset_goto_azm(0)
    res = command(ser, cmd, 1)

    logger.debug("send reset alt")
    cmd = reset_goto_alt(0)
    res = command(ser, cmd, 1)

    logger.debug("send slow goto az")
    cmd = slow_goto_azm(0)
    res = command(ser, cmd, 1)

    logger.debug("send slow goto alt")
    cmd = slow_goto_alt(0)
    res = command(ser, cmd, 1)

sys.exit(1)
