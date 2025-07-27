# Architecture

## Overview

The `pykd3300` package is structured to provide a flexible and extensible interface for laboratory power supplies, specifically the Korad KD3300 series.

## Class Structure

- **PowerSupply (base class)**
  - Defines the abstract interface for power supply devices (in `labdevices.powersupply`)
  - Handles channel, voltage, current, and power range management
  - Provides context management and imperative connect/disconnect

- **KD3305P (device implementation)**
  - Implements all required methods for the KD3300 series
  - Supports serial, USB, and UDP (Ethernet) communication
  - Adds device-specific features (network config, lock/unlock)

## Extensibility

- New devices can be supported by subclassing `PowerSupply` and implementing required methods.
- Device-specific features can be added as needed.

## Directory Layout

- `src/pykd3300/` — Main package code
- `examples/` — Example usage scripts
- `doc/` — Documentation

## Dependencies

- `pyserial` for serial/USB communication
- `pylabdevs-tspspi` for base interfaces 