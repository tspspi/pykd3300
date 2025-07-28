from pykd3300.kd3305d import KD3305P

from time import sleep

# This script demonstrates key features of the KD3305P power supply
# when connected via IP, including setting current and voltage, and
# enabling/disabling channels.

# Import the KD3305P class from the pykd3300.kd3305d module.
# This class is used to interact with the KD3305P power supply unit.

# The 'with' statement is used to ensure that the connection to the
# power supply unit is properly managed and closed after use.

with KD3305P(ip = "192.168.1.182", debug = True) as psu:
    # Call the _idn() method to get the identification string of the device.
    print(psu._idn())

    # Set the current for channel 1 and channel 2.
    psu.setCurrent(0.01, 1)
    psu.setCurrent(0.02, 2)

    # Set the voltage for channel 1 and channel 2.
    psu.setVoltage(10, 1)
    psu.setVoltage(20, 2)

    # Wait for 5 seconds to allow settings to take effect (or rather
    # allow the user to spot the changes on the device)
    sleep(5)

    # Enable both channels and wait for 5 seconds.
    psu.setChannelEnable(True, 1)
    psu.setChannelEnable(True, 2)
    sleep(5)

    # Print the current voltage of both channels.
    print(f"Channel 1 voltage: {psu.getVoltage(1)}")
    print(f"Channel 2 voltage: {psu.getVoltage(2)}")
    sleep(5)

    # Disable both channels with a delay between each.
    psu.setChannelEnable(False, 1)
    sleep(2)
    psu.setChannelEnable(False, 2)
    sleep(1)

    # Reset the voltage and current settings for both channels.
    psu.setVoltage(5, 1)
    psu.setVoltage(5, 2)
    psu.setCurrent(1, 1)
    psu.setCurrent(1, 2)
