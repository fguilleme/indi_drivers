import serial

import logging
import logging.handlers

DEBUG = True

AZM = 16
ALT = 17

NEGATIVE = 7
POSITIVE = 6
SLOW_GOTO = 23
RESET = 4

def unhex(a):
    if len(a) % 2:
        a = b'0'+a
    return bytes.fromhex(a.decode('ASCII'))

def float_to_bin32(a, b):
    n = round(a * 0x1000000 / b)
    return bytes([round(n/ (256*256)), round(n / 256), n % 256, 0])

def bin32_to_float(a, b):
    a = unhex(a)
    if len(a) != 4:
        raise f"invalid byte array length {len(a)}"

    n = a[0] * 256 * 256 + a[1] * 256 + a[2]
    return n * b / 0x100000000

def float_to_bin16(a, b):
    n = round(a * 0x10000 / b)
    return bytes([round(n / 256), n % 256])

def bin16_to_float(a, b):
    a = unhex(a)

    if len(a) > 2 or len(a) < 1:
        raise f"invalid byte array length {len(a)}"

    n = a[0] * 256 + a[1]
    return n * b / 0x10000

###################################################################
def command(dev, cmd, n=0):
    dev.write(cmd)
    if DEBUG:
        logger.debug('=> %s %s', cmd, cmd.hex())
    if n > 0:
        resp = dev.read(1)
    else:
        resp = dev.read_until(b'#')
    if DEBUG:
        logger.debug('<= %s %s', resp, resp.hex())
    return resp

def passthrough(cmd, target, data):
    if DEBUG:
        logger.debug('Passthu %s', [80, len(data), target, cmd])
    return bytes([80, len(data), target, cmd]) + data

#########################################################################
def goto_azm_alt(dev, az, alt):
    cmd = 'B' + float_to_bin16(az, 24).hex() + ',' + float_to_bin16(alt, 360).hex()
    resp = command(dev, cmd.encode('UTF-8'))
 
def goto_azm_alt_32(dev, azm, alt):
    cmd = 'b' + float_to_bin32(az, 24).hex() + ',' + float_to_bin32(alt, 360).hex()
    resp = command(dev, cmd.encode('UTF-8'))

def goto_ra_dec(dev, ra, dec):
    cmd = 'R' + float_to_bin16(ra, 24).hex() + ',' + float_to_bin16(dec, 360).hex()
    if DEBUG:
        logger.debug("%s %s", ra, float_to_bin16(ra, 24))
        logger.debug("%s %s", dec, float_to_bin16(dec, 24))
    resp = command(dev, cmd.encode('UTF-8'))

def goto_ra_dec_32(dev, ra, dec):
    cmd = 'r' + float_to_bin32(ra, 24).hex() + ',' + float_to_bin32(dec, 360).hex()
    resp = command(dev, cmd.encode('UTF-8'))

#########################################################################
def get_azm_alt(dev):
    resp = command(dev, b'Z')
    azm = bin16_to_float(resp[:4], 360)
    alt = bin16_to_float(resp[6:-1], 360)
    return azm, alt

def get_ra_dec(dev):
    resp = command(dev, b'E')
    ra = bin16_to_float(resp[:4], 24)
    dec = bin16_to_float(resp[6:-1], 360)
    return ra, dec

def get_azm_alt32(dev):
    resp = command(dev, b'z')
    azm = bin32_to_float(resp[:8], 360)
    alt = bin32_to_float(resp[9:-1], 360)
    return azm, alt

def get_ra_dec32(dev):
    resp = command(dev, b'e')
    ra = bin32_to_float(resp[:8], 24)
    dec = bin32_to_float(resp[9:-1], 360)
    return ra, dec

#########################################################################
def is_alive(dev):
    if DEBUG:
        logger.debug("is alive?")
    resp = command(dev, b'Kx')
    return resp == b'x#'

def is_goto_running(dev):
    if DEBUG:
        logger.debug("is goto running?")
    resp = command(dev, b'L')
    return resp[0] == b'1'

def cancel_goto(dev):
    if DEBUG:
        logger.debug("cancel goto")
    resp = command(dev, b'M')

def is_aligned(dev):
    if DEBUG:
        logger.debug("is aligned?")
    resp = command(dev, b'J')
    return resp == b'1#'

def control_tracking(dev, mode):
    if logger.debug:
        print("set tracking mode =", mode)
    resp = command(dev, b'T' + byte(mode))

def slow_goto_azm(az):
    return passthrough(SLOW_GOTO, AZM, float_to_bin32(az, 360))

def slow_goto_alt(az):
    return passthrough(SLOW_GOTO, ALT, float_to_bin32(az, 360))

def reset_goto_azm(az):
    return passthrough(RESET, AZM, float_to_bin32(az, 360))

def reset_goto_alt(az):
    return passthrough(RESET, ALT, float_to_bin32(az, 360))

def pos_azm_track_rate(rate):
    rate = rate * 4
    buf = bytes([round(rate/256), round(rate) % 256, 0, 0])
    return passthrough(POSITIVE, AZM, buf)

def neg_azm_track_rate(rate):
    rate = rate * 4
    buf = bytes([round(rate/256), round(rate) % 256, 0, 0])
    return passthrough(NEGATIVE, AZM, buf)

def pos_alt_track_rate(rate):
    rate = rate * 4
    buf = bytes([round(rate/256), round(rate) % 256, 0, 0])
    return passthrough(POSITIVE, ALT, buf)

def neg_alt_track_rate(rate):
    rate = rate * 4
    buf = bytes([round(rate/256), round(rate) % 256, 0, 0])
    return passthrough(NEGATIVE, ALT, buf)

def init(): 
    return serial.Serial( port='/dev/ttyUSB0', 
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1)

logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger('scope')
logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(
            '/var/log/indi/driver.log',
            maxBytes=5_000_000, backupCount=5)
logger.addHandler(handler)

