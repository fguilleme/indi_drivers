#!/usr/bin/python3
import sys
import serial
import teletrak as T

script, ra, dec = sys.argv

with serial.Serial( port='/dev/ttyUSB0', 
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=30) as ser:
    if not T.isalive(ser):
        sys.exit(1)

    if T.isgoto(ser):
        T.cancelgoto(ser)

    print("goto", ra, dec)
    resp = T.goto_ra_dec(ser, float(ra), float(dec))

sys.exit(1)
