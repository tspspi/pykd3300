# Examples Overview

This directory contains example scripts demonstrating the usage of the `pykd3300` library to interact with the KD3305P power supply unit. Each example showcases different functionalities and configurations.

## Example Files

### 001-identify.py

- **Purpose**: Identifies a serially connected KD3305P device and outputs its identification string.
- **Usage**: Run the script to see the device's manufacturer, model and serial number. You have to adjust the path of the serial port or the virtual serial port presented by the USB connector.

### 002-netconfig.py

- **Purpose**: Configures the network settings of a connected device by enabling DHCP and retrieves the network information.
- **Usage**: Run the script to enable DHCP and print the device's IP address, port, subnet mask, gateway, DHCP status and MAC address. You have to adjust the serial port name or the the virtual serial port name presented by the USB connector to execute this script.

### 003-nettest.py

- **Purpose**: Demonstrates key features of the KD3305P when connected via IP, including setting current and voltage and enabling/disabling channels.
- **Usage**: Run the script to configure and test the power supply's channels and observe the output voltages. Adjust the ip parameter to connect to the desired device.

## Running the Examples

To run any of the examples, ensure you have the `pykd3300` library installed and the KD3305P device connected to your system. Execute the scripts using Python:

```bash
python examples/001-identify.py
python examples/002-netconfig.py
python examples/003-nettest.py
```

## Dependencies

- Python 3.x
- `pykd3300-tspspi` library
- `pyserial` (pulled automatically when installing `pykd3300-tspspi`)

Ensure all dependencies are installed and the device is properly connected before running the examples.