from pykd3300.kd3305d import KD3305P

from time import sleep

with KD3305P(port = "/dev/ttyU1", debug = True) as psu:
    print(psu._idn())

    psu._lock()
    sleep(5)
    psu.setVoltage(7, 1)
    sleep(5)
    print(f"Voltage on channel 1: {psu.getVoltage(1)}")
    psu.setVoltage(5, 1)
    sleep(5)
    print(f"Voltage on channel 1: {psu.getVoltage(1)}")
    sleep(5)
    psu._unlock()
    sleep(1)




#    psu.setChannelEnable(True, 1)
#    sleep(5)
#    psu.setChannelEnable(True, 2)
 #   sleep(5)
#    psu.setChannelEnable(False, 1)
#    sleep(5)
#    psu.setChannelEnable(False, 2)
   
