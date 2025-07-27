from pykd3300.kd3305d import KD3305P

from time import sleep

# Identify the serially connected device, dump
# all messages to stdout

with KD3305P(port = "/dev/ttyU1", debug = True) as psu:
    print(psu._idn())

