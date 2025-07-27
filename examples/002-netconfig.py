from pykd3300.kd3305d import KD3305P

from time import sleep

# Set the DHCP enable on the attached device, wait for
# 30 seconds and then dump the network information of
# the attached device

with KD3305P(port = "/dev/ttyU0", debug = True) as psu:
    print(psu._idn())

    # Enable DHCP
    psu.set_network(dhcp = True)

    sleep(30)

    # Query IP and port interface
    ip, port, mask, gw, dhcp, mac = psu.get_ip_address()

    print(f"IP:           {ip}")
    print(f"Port:         {port}")
    print(f"Subnet mask:  {mask}")
    print(f"Gateway:      {gw}")
    print(f"DHCP enabled: {dhcp}")
    print(f"MAC:          {mac}")
