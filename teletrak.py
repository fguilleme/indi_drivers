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

def f2b32(a, b):
    n = round(a * 0x1000000 / b)
    return bytes([round(n/ (256*256)), round(n / 256), n % 256, 0])

def b32_2f(a, b):
    print(a)
    a = unhex(a)
    print(a)
    if len(a) != 4:
        raise f"invalid byte array length {len(a)}"

    n = a[0] * 256 * 256 + a[1] * 256 + a[2]
    return n * b / 0x100000000

def f2b16(a, b):
    n = round(a * 0x10000 / b)
    return bytes([round(n / 256), n % 256])

def b16_2f(a, b):
    a = unhex(a)

    if len(a) > 2 or len(a) < 1:
        raise f"invalid byte array length {len(a)}"
    n = a[0] * 256 + a[1]
    return n * b / 0x10000

###################################################################

def command(dev, cmd, n=0):
    dev.write(cmd)
    if DEBUG:
        print('=>', cmd, cmd.hex())
    if n > 0:
        resp = dev.read(1)
    else:
        resp = dev.read_until(b'#')
    if DEBUG:
        print('<=', resp, resp.hex())
    return resp

def passthrough(cmd, target, data):
    if DEBUG:
        print('Passthu', [80, len(data), target, cmd])
    return bytes([80, len(data), target, cmd]) + data

#########################################################################
def goto_azm_alt(dev, az, alt):
    cmd = 'B' + f2b16(az, 24).hex() + ',' + f2b16(alt, 360).hex()
    resp = command(dev, cmd.encode('UTF-8'))
 
def goto_azm_alt_32(dev, azm, alt):
    cmd = 'b' + f2b32(az, 24).hex() + ',' + f2b32(alt, 360).hex()
    resp = command(dev, cmd.encode('UTF-8'))

def goto_ra_dec(dev, ra, dec):
    cmd = 'R' + f2b16(ra, 24).hex() + ',' + f2b16(dec, 360).hex()
    if DEBUG:
        print(ra, f2b16(ra, 24))
        print(dec, f2b16(dec, 24))
    resp = command(dev, cmd.encode('UTF-8'))

def goto_ra_dec_32(dev, ra, dec):
    cmd = 'r' + f2b32(ra, 24).hex() + ',' + f2b32(dec, 360).hex()
    resp = command(dev, cmd.encode('UTF-8'))

#########################################################################
def get_azm_alt(dev):
    resp = command(dev, b'Z')
    azm = b16_2f(resp[:4], 360)
    alt = b16_2f(resp[6:-1], 360)
    return azm, alt

def get_ra_dec(dev):
    resp = command(dev, b'E')
    ra = b16_2f(resp[:4], 24)
    dec = b16_2f(resp[6:-1], 360)
    return ra, dec

def get_azm_alt32(dev):
    resp = command(dev, b'z')
    azm = b32_2f(resp[:8], 360)
    alt = b32_2f(resp[9:-1], 360)
    return azm, alt

def get_ra_dec32(dev):
    resp = command(dev, b'e')
    ra = b32_2f(resp[:8], 24)
    dec = b32_2f(resp[9:-1], 360)
    return ra, dec

#########################################################################
def isalive(dev):
    if DEBUG:
        print("is alived?")
    resp = command(dev, b'Kx')
    return resp == b'x#'

def isgoto(dev):
    if DEBUG:
        print("is goto running?")
    resp = command(dev, b'L')
    return resp[0] == b'1'

def cancelgoto(dev):
    if DEBUG:
        print("cancel goto")
    resp = command(dev, b'M')

def isaligned(dev):
    if DEBUG:
        print("is aligned?")
    resp = command(dev, b'J')
    return resp == b'1#'

def control_tracking(dev, mode):
    if DEBUG:
        print("set tracking mode =", mode)
    resp = command(dev, b'T' + byte(mode))

def slow_goto_azm(az):
    return passthrough(SLOW_GOTO, AZM, f2b32(az, 360))

def slow_goto_alt(az):
    return passthrough(SLOW_GOTO, ALT, f2b32(az, 360))

def reset_goto_azm(az):
    return passthrough(RESET, AZM, f2b32(az, 360))

def reset_goto_alt(az):
    return passthrough(RESET, ALT, f2b32(az, 360))

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

    
