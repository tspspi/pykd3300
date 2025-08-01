import serial
import atexit
import math
import socket

from time import sleep
from labdevices import powersupply

class KD3305P(powersupply.PowerSupply):
    def __init__(
            self,
            port = 18190,   # For IP mode this is the UDP port, else the path to the device file for the serial device
            ip = None,      # If IP is set to none we are serial/USB mode
#            baud = 115200,  # For serial mode this is the BAUD rate
            baud = 19200,

            debug = False,

            timeoutRetry = 3,
            readbackRetry = 3,
            serialCommandDelay = 0.1
    ):
        super().__init__(
            nChannels = 2, # The device has 3 channels but only 1 and 2 are controllable via the interface
            vrange = (0, 30, 0.01),
            arange = (0, 5, 0.01),
            prange = (0, 150, 0.01),
            capableVLimit = True,
            capableALimit = True,
            capableMeasureV = True,
            capableMeasureA = True,
            capableOnOff = True
        )

        self._debug = debug
        self._timeoutRetry = timeoutRetry
        self._readbackRetry = readbackRetry
        self._serialCommandDelay = serialCommandDelay
        self._baud = baud

        if ip is None:
            # Serial port mode
            if isinstance(port, serial.Serial):
                self._port = port
                self._portName = None
                self._ip = None
                self._socket = None
                self.__initialRequests()
            else:
                self._portName = port
                self._port = None
                self._ip = None
                self._socket = None
        else:
            self._portName = None
            self._port = port
            self._ip = ip
            self._socket = None

        atexit.register(self.__close)

    def _isConnected(self):
        if self._ip is None:
            if self._port is not None:
                return True
        else:
            if self._socket is not None:
                return True

        return False

    def __initialRequests(self):
        pass # ToDo

    ## Context management

    def __enter__(self):
        if self._usedConnect:
            raise ValueError("Cannot use context management on a connected port")

        if self._ip is None:
            # Serial port mode
            if (self._port is None) and (self._portName is not None):
                self._port = serial.Serial(
                    self._portName,
                    baudrate = self._baud,
                    bytesize = serial.EIGHTBITS,
                    parity = serial.PARITY_NONE,
                    stopbits = serial.STOPBITS_ONE,
                    timeout = 1
                )
                self.__initialRequests()
            # In the other case the port was already open and written into self._port

            self._usesContext = True
        else:
            if self._socket is None:
                # For debugging we set REUSEADDR and REUSEPORT to avoid being locked out during
                # application start when not closing the socket propery
                self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self._socket.settimeout(1)
                self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                try:
                    self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                except AttributeError:
                    pass
                # Bind to all IPs and our port that we send also requests on
                self._socket.bind(('', self._port))

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__close()
        self._usesContext = False

    def __close(self):
        atexit.unregister(self.__close)
        if self._ip is None:
            if (self._port is not None) and (self._portName is not None):
                self._off()
                self._port.close()
                self._port = None
        else:
            if self._socket is not None:
                self._socket.close()
                self._socket = None

    def _connect(self):
        if self._ip is None:
            if (self._port is None) and (self._portName is not None):
                self._port = serial.Serial(
                    self._portName,
                    baudrate = self._baud,
                    bytesize = serial.EIGHTBITS,
                    parity = serial.PARITY_NONE,
                    stopbits = serial.STOPBITS_ONE,
                    timeout = 1
                )
                self.__initialRequests()
        else:
            if self._socket is None:
                # For debugging we set REUSEADDR and REUSEPORT to avoid being locked out during
                # application start when not closing the socket propery
                self._socket = socket.socket(socket.AF_INET, socket.SOCK_DRAM)
                self._socket.settimeout(1)
                self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                try:
                    self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                except AttributeError:
                    pass
                # Bind to all IPs and our port that we send also requests on
                self._socket.bind(('', self._port))

        return True

    def _disconnect(self):
        if self._ip is None:
            if self._port is not None:
                self.__close()
        else:
            if self._socket is not None:
                self.__close()

    # Utility functions

    def _sendCommand(self, cmd):
        if self._debug:
            print(f"PSU> {cmd}")

        if self._ip is None:
            sleep(self._serialCommandDelay)
            self._port.write(f"{cmd}\n".encode('ascii'))
        else:
            if self._socket is None:
                raise IOError("Socket is not connected")

            self._socket.sendto(f"{cmd}\n".encode('ascii'), (self._ip, self._port))

    def _sendCommandReply(self, cmd, replyLen = None, binary = False):
        retries = self._timeoutRetry

        if self._debug:
            print(f"PSU> {cmd}")

        if self._ip is None:
            sleep(self._serialCommandDelay)
            self._port.write(f"{cmd}\n".encode('ascii'))

            res = []
            while True:
                if not binary:
                    c = self._port.read(1).decode('ascii')
                else:
                    c = self._port.read(1)

                if len(c) <= 0:
                    if (replyLen is not None) and (replyLen < 0):
                        break

                    if self._debug:
                        print(f"PSU Timeout, received {res} until now")
                    if (retries is not None):
                        if retries > 0:
                            retries = retries - 1
                            continue
                        else:
                            raise IOError("Serial port timeout")
                if (ord(c) == 0) or (ord(c) == 10):
                    break

                res.append(c)
                if replyLen is not None:
                    if len(res) == replyLen:
                        break

            if not binary:
                reply = "".join(res)
            else:
                reply = res
        else:
            if self._socket is None:
                raise IOError("Socket is not connected")

            self._socket.sendto(f"{cmd}\n".encode('ascii'), (self._ip, self._port))

            res = []
            while True:
                try:
                    data, _ = self._socket.recvfrom(4096)
                    if not binary:
                        c = data.decode('ascii')
                    else:
                        c = data

                    if len(c) <= 0:
                        if (replyLen is not None) and (replyLen < 0):
                            break

                        if self._debug:
                            print(f"PSU Timeout, received {res} until now")
                        if (retries is not None):
                            if retries > 0:
                                retries = retries - 1
                                continue
                            else:
                                raise IOError("UDP socket timeout")
                    if len(c) == 1:
                        if (not binary and (ord(c) == 0 or ord(c) == 10)) or (binary and c == b'\x00'):
                            break
                    else:
                        if (not binary and (ord(c[-1]) == 0 or ord(c[-1]) == 10)) or (binary and c[-1] == b'\x00'):
                            if len(c) > 1:
                                res.append(c[:-1])
                            break

                    if isinstance(c, (bytes, bytearray)):
                        for b in c:
                            res.append(bytes([b,]))
                    else:
                        res.append(c)

                    if replyLen is not None:
                        if len(res) == replyLen:
                            break
                except Exception as e:
                    if (retries is not None) and retries > 0:
                        retries = retries - 1
                        continue
                    else:
                        raise IOError(f"UDP socket error: {e}")

        if not binary:
            reply = "".join(res)
        else:
            reply = res


        if self._debug:
            print(f"PSU< {reply}")

        return reply

    # Communication functions

    def _idn(self, initialQuery = False):
        retries = 2
        while retries > 0:
            repl = self._sendCommandReply("*IDN?", replyLen = -1)
            if len(repl) > 0:
                break
            elif retries > 0:
                retries = retries - 1
            else:
                raise IOError("Device not responding")

        parts = repl.split(" ")

        if (parts[0] != "KORAD") or (parts[1] != "KD3305P"):
            if not initialQuery:
                raise ValueError(f"Unsupported device: {repl}")
            else:
                return False

        version = parts[2][1:].split(".")
        version = (int(version[0]), int(version[1]))
        serial = parts[3][3:-1]

        return {
            "idn" : repl,
            "version" : version,
            "serial" : serial
        }

    def _get_status(self):
        retries = self._readbackRetry

        repl = self._sendCommandReply("STATUS?", replyLen = 2, binary = True)
        if len(repl) == 2:
            repl = int.from_bytes(repl[0], "little")

            # Interpret ...
            res = {
                'enabled' : [ False, False ],
                'channel_mode' : [ 0, 0 ],
                'tracking' : 0
            }

            if (repl & 0x01) != 0:
                res['channel_mode'][0] = 1
            if (repl & 0x02) != 0:
                res['channel_mode'][1] = 1
            res['tracking'] = ((repl >> 2) & 0x03)
            if (repl & 0x40) != 0:
                res['enabled'][0] = True
            if (repl & 0x80) != 0:
                res['enabled'][1] = True

            return res
        
        raise IOError("Device fails to respond")

    def _setChannelEnable(self, enable, channel):
        if channel not in [1, 2]:
            raise ValueError(f"Channel {channel} is invalid")

        retries = self._readbackRetry

        while True:
            if enable:
                self._sendCommand(f"OUT{channel}:1")
            else:
                self._sendCommand(f"OUT{channel}:0")

            state = self._get_status()
            if state['enabled'][channel-1] == enable:
                return True

            if self._debug:
                print("PSU: Readback failed")

            if retries > 0:
                retries = retries - 1
                if retries == 0:
                    raise IOError("Failed to set output status and read back correct state")

    def _setVoltage(self, voltage, channel):
        retries = self._readbackRetry

        while True:
            self._sendCommand(f"VSET{channel}:{voltage:05.2f}")

            repl = self._sendCommandReply(f"VSET{channel}?")
            try:
                repl = float(repl)
            except:
                repl = None

            if repl is not None:
                if math.fabs(repl - voltage) < 0.01:
                    return True
                else:
                    if self._debug:
                        print("Set voltage {repl} deviates from requested set voltage {voltage}")

            if retries > 0:
                retries = retries - 1
                if retries == 0:
                    raise IOError("Failed to read back set voltage. Device in unknown state")

    def _setCurrent(self, voltage, channel):
        retries = self._readbackRetry

        while True:
            self._sendCommand(f"ISET{channel}:{voltage:05.2f}")

            repl = self._sendCommandReply(f"ISET{channel}?")
            try:
                repl = float(repl)
            except:
                repl = None

            if repl is not None:
                if math.fabs(repl - voltage) < 0.01:
                    return True
                else:
                    if self._debug:
                        print("Set current {repl} deviates from requested set current {voltage}")

            if retries > 0:
                retries = retries - 1
                if retries == 0:
                    raise IOError("Failed to read back set current. Device in unknown state")

    def _getVoltage(self, channel):
        retries =  self._readbackRetry

        while True:
            repl = self._sendCommandReply(f"VOUT{channel}?")
            try:
                return float(repl)
            except:
                pass

            if retries > 0:
                retries = retries - 1
                if retries == 0:
                    raise IOError("Failed to query output voltage")

    def _getCurrent(self, channel):
        retries =  self._readbackRetry

        while True:
            repl = self._sendCommandReply(f"IOUT{channel}?")
            try:
                return float(repl)
            except:
                pass

            if retries > 0:
                retries = retries - 1
                if retries == 0:
                    raise IOError("Failed to query output current")

    def _off(self):
        self._setChannelEnable(False, 1)
        self._setChannelEnable(False, 2)
        return True

    def _getLimitMode(self, channel):
        state = self._get_status()
        if not state['enabled'][channel - 1]:
            return powersupply.PowerSupplyLimit.NONE
        elif state['channel_mode'][channel - 1] == 1:
            return powersupply.PowerSupplyLimit.VOLTAGE
        else:
            return powersupply.PowerSupplyLimit.CURRENT

    # Non standard functions

    def _lock(self):
        self._sendCommand("LOCK1")

    def _unlock(self):
        self._sendCommand("LOCK0")

    def get_network(self):
       ip = self._sendCommandReply(":SYST:IPAD?") 
       mask = self._sendCommandReply(":SYST:SMASK?")
       gw = self._sendCommandReply(":SYST:GATE?")
       dhcp = self._sendCommandReply(":SYST:DHCP?")
       mac = self._sendCommandReply(":SYST:MAC?")
       port = self._sendCommandReply(":SYST:PORT?")

       return (ip, port, mask, gw, dhcp, mac)

    def set_network(
        self,
        ip = None,
        port = None,
        mask = None,
        gateway = None,
        dhcp = None
    ):
        if ip is not None:
            self._sendCommand(f":SYST:IPAD {ip}")
        if port is not None:
            self._sendCommand(f":SYST:PORT {port}")
        if mask is not None:
            self._sendCommand(f":SYST:SMASK {mask}")
        if gateway is not None:
            self._sendCommand(f":SYST:GATE {gateway}")
        if dhcp is not None:
            if dhcp:
                self._sendCommand(f":SYST:DHCP 1")
            else:
                self._sendCommand(f":SYST:DHCP 0")

        ## ToDo: Add readback and check if everything is set correctly 

        return True