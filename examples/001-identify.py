from pykd3300.kd3305d import KD3305P

from time import sleep

# This script identifies a serially connected device and outputs
# all communication messages to the standard output.

# The 'with' statement is used to ensure that the connection to the
# power supply unit is properly managed and closed after use.

# Create an instance of KD3305P with the specified port and enable
# debugging to see detailed communication logs.
with KD3305P(port = "/dev/ttyU1", debug = True) as psu:
    # Call the _idn() method to get the identification string of the device.
    # This typically includes the manufacturer, model, and serial number.
    print(psu._idn())

