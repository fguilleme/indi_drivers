#!/usr/bin/python3
import sys
import serial
import teletrak as T

with serial.Serial( port='/dev/ttyUSB0', 
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=30) as ser:
    if not T.isalive(ser):
        sys.exit(1)

    print("send slow goto az")
    cmd = T.slow_goto_azm(0)
    res = T.command(ser, cmd, 1)

    print("send slow goto alt")
    cmd = T.slow_goto_alt(0)
    res = T.command(ser, cmd, 1)

sys.exit(1)
