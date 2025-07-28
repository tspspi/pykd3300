from pykd3300.kd3305d import KD3305P

from time import sleep

# This script configures the network settings of a connected device
# by enabling DHCP and then retrieves the network information.

# Create an instance of KD3305P with the specified port and enable
# debugging to see detailed communication logs.
with KD3305P(port = "/dev/ttyU0", debug = True) as psu:
    # Call the _idn() method to get the identification string of the device.
    print(psu._idn())

    # Enable DHCP on the device to automatically obtain network settings.
    psu.set_network(dhcp = True)

    # Wait for 30 seconds to allow the device to obtain network settings.
    sleep(30)

    # Retrieve and print the network configuration details.
    ip, port, mask, gw, dhcp, mac = psu.get_ip_address()

    print(f"IP:           {ip}")
    print(f"Port:         {port}")
    print(f"Subnet mask:  {mask}")
    print(f"Gateway:      {gw}")
    print(f"DHCP enabled: {dhcp}")
    print(f"MAC:          {mac}")
