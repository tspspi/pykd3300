from pykd3300.kd3305d import KD3305P

from time import sleep

# A quick demonstration of some of the important features
# when connecting via IP (assuming the default port) and
# dumping all messages on stdout

with KD3305P(ip = "192.168.1.182", debug = True) as psu:
    print(psu._idn())

    psu.setCurrent(0.01, 1)
    psu.setCurrent(0.02, 2)

    psu.setVoltage(10, 1)
    psu.setVoltage(20, 2)

    sleep(5)

    psu.setChannelEnable(True, 1)
    psu.setChannelEnable(True, 2)
    sleep(5)
    print(f"Channel 1 voltage: {psu.getVoltage(1)}")
    print(f"Channel 2 voltage: {psu.getVoltage(2)}")
    sleep(5)
    psu.setChannelEnable(False, 1)
    sleep(2)
    psu.setChannelEnable(False, 2)
    sleep(1)

    psu.setVoltage(5, 1)
    psu.setVoltage(5, 2)
    psu.setCurrent(1, 1)
    psu.setCurrent(1, 2)
