#!/usr/bin/python3
import sys
import serial
from struct import unpack

with serial.Serial( port='/dev/ttyUSB0', 
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1) as ser:
    ser.write(b'Kx')                        # echo
    resp = ser.read_until(b'#')[:-1]
    if resp != b'x':
        sys.exit(1)

    ser.write(b'T\0')                         # is GOTO in progress
    resp = ser.read(1)
    if resp != b'#':
        sys.exit(1)

    ser.write(b'M')
    resp = ser.read(1)

    ser.write(b'M')
    resp = ser.read(1)
    sys.exit(0)
sys.exit(1)
