# KD3305P Device Commands

This document summarizes the main commands and features supported by the KD3305P implementation in `pykd3300`.

## Channel Control

- Set voltage: `setVoltage(voltage, channel)`
- Set current: `setCurrent(current, channel)`
- Enable/disable output: `setChannelEnable(enable, channel)`
- Turn off all channels: `off()`

## Measurement

- Get measured voltage: `getVoltage(channel)`
- Get measured current: `getCurrent(channel)`
- Get limit mode (V/C/None): `getLimitMode(channel)`

## Network Configuration (Ethernet models)

- Get network settings: `get_network()`
- Set network settings: `set_network(ip=..., port=..., mask=..., gateway=..., dhcp=...)`

## Device Identification

- Query device info: `_idn()`

## Lock/Unlock Front Panel

- Lock: `lock()`
- Unlock: `unlock()`

## Notes

- All commands are available via the Python API. See `examples/` for usage.
- Not all features are available on all device models. 