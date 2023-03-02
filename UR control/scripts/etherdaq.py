import struct
import socket
import dataclasses
import threading
import numpy as np
import collections


# F/T reading (received via UDP)
@dataclasses.dataclass
class HSURecord:
    hs_seq: int  # The sequence number of the current HS UDP record
    ft_seq: int  # The internal sample counter of the DAQ
    status: int  # Status word of the sensor and DAQ
    fx: int      # X-axis force in 32 bit counts*
    fy: int
    fz: int
    tx: int      # X-axis torque in 32 bit counts* (0 if not available)
    ty: int
    tz: int


# F/T conversion parameters (response to command via TCP)
@dataclasses.dataclass
class FTConvParams:
    header: int
    force_unit: int
    torque_unit: int
    counts_per_force: int
    counts_per_torque: int
    scaling_fx: int
    scaling_fy: int
    scaling_fz: int
    scaling_tx: int
    scaling_ty: int
    scaling_tz: int


# F/T reading (response to command via TCP)
@dataclasses.dataclass
class FTReading:
    header: int
    status: int
    fx: int
    fy: int
    fz: int
    tx: int
    ty: int
    tz: int


class EtherDAQ:
    def __init__(self, ip):
        self._ip = ip
        self._port_tcp = 49151
        self._port_udp = 49152
        self.records = collections.deque(maxlen=10)
        self.wrench_offset = np.zeros(6)

        # Get conversion parameters via TCP request
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self._ip, self._port_tcp))
            cmd = struct.pack('!20b', 0x01, *[0x00]*19)  # Get conversion parameters
            sock.sendall(cmd)
            data = sock.recv(24)
            self._conf = FTConvParams(*struct.unpack('!HbbII6H', data))
            assert(self._conf.header == 0x1234)

            # cmd = struct.pack('!20b', 0x00, *[0x00]*19)  # Get latest F/T reading
            # sock.sendall(cmd)
            # data = sock.recv(16)
            # rec = FTReading(*struct.unpack('!HH6h', data))
            # wrench = np.array([rec.fx, rec.fy, rec.fz, rec.tx, rec.ty, rec.tz], dtype=float)
            # wrench[0] *= self._conf.scaling_fx / self._conf.counts_per_force
            # wrench[1] *= self._conf.scaling_fy / self._conf.counts_per_force
            # wrench[2] *= self._conf.scaling_fz / self._conf.counts_per_force
            # wrench[3] *= self._conf.scaling_tx / self._conf.counts_per_torque
            # wrench[4] *= self._conf.scaling_ty / self._conf.counts_per_torque
            # wrench[5] *= self._conf.scaling_tz / self._conf.counts_per_torque

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind(('', self._port_udp))
        self._stop = threading.Event()

    def get_wrench(self):
        if self.records:
            return self.records[-1]

    def run_read_loop(self):
        cmd = struct.pack('!HHI', 0x1234, 0x0002, 0)  # Start sending data from sensor
        self._sock.sendto(cmd, (self._ip, self._port_udp))

        while not self._stop.is_set():
            data, addr = self._sock.recvfrom(36)

            if addr != (self._ip, self._port_udp):
                continue

            assert(len(data) == 36)
            rec = HSURecord(*struct.unpack('!IIIiiiiii', data))  # F/T data are signed values (though manual says unsigned)
            wrench = np.array([rec.fx, rec.fy, rec.fz, rec.tx, rec.ty, rec.tz], dtype=float)
            wrench[:3] /= self._conf.counts_per_force
            wrench[3:] /= self._conf.counts_per_torque
            wrench -= self.wrench_offset
            self.records.append(wrench)

        cmd = struct.pack('!HHI', 0x1234, 0x0000, 0)  # Stop sending data from sensor
        self._sock.sendto(cmd, (self._ip, self._port_udp))

    def stop_loop(self):
        self._stop.set()

    def enable_internal_bias(self, enable_bias=True):
        # Effectively "zeros" the F/T sensor
        value = 255 if enable_bias else 0
        cmd = struct.pack('!HHI', 0x1234, 0x0042, value)
        self._sock.sendto(cmd, (self._ip, self._port_udp))

    def set_internal_filter_cutoff_frequency(self, cutoff_frequency_hz):
        val = {
            None: 0,  # no filter
            0: 0,     # also no filter
            500: 1,
            150: 2,
            50: 3,
            15: 4,
            5: 5,
            1.5: 6,
        }

        cmd = struct.pack('!HHI', 0x1234, 0x0081, val[cutoff_frequency_hz])
        self._sock.sendto(cmd, (self._ip, self._port_udp))

    def set_readout_rate(self, rate_hz):
        if not 4 <= rate_hz <= 1000:
            raise ValueError

        period_ms = int(1 / rate_hz * 1000)
        cmd = struct.pack('!HHI', 0x1234, 0x0082, period_ms)
        self._sock.sendto(cmd, (self._ip, self._port_udp))

    def zero(self):
        if self.records:
            self.wrench_offset = np.mean(self.records, axis=0)
