#!/usr/bin/python3
import sys
import serial
with serial.Serial( port='/dev/ttyUSB0', 
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1) as ser:
    ser.write(b'Kx')
    resp = ser.read(2)
    if resp == b'x#':
        sys.exit(0)

sys.exit(1)

