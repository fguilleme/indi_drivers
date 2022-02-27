#!/usr/bin/python3
import sys
import serial

import teletrak as T

script, path = sys.argv

with serial.Serial( port='/dev/ttyUSB0', 
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1) as ser:
    if not T.isalive(ser):
        sys.exit(1)

    if T.isgoto(ser):
        T.cancelgoto(ser)

    ra, dec = T.get_ra_dec(ser)
    print(f'RA = {ra}, DEC = {dec}')

    ra, dec = T.get_ra_dec32(ser)
    print(f'RA = {ra}, DEC = {dec}')
    print(f'0 {ra} {dec}', file=open(path, "w"))
    sys.exit(0)
sys.exit(1)
