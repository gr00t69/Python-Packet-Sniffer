import struct
import time


class Pcap:

    def __init__(self, filename, modRead=False, link_type=1):
        self.pcap_file = None
        self.modRead = modRead
        if modRead:
            self.pcap_file = open(filename, 'rb')
            p1, p2, p3,p4,p5,p6, link_type = struct.unpack('@ I H H i I I I', self.pcap_file.read(24))
            print('{} {} {} {} {} {} {}'.format(p1, p2, p3,p4,p5,p6, link_type))
        else:
            self.pcap_file = open(filename, 'wb')
            self.pcap_file.write(struct.pack('@ I H H i I I I', 0xa1b2c3d4, 2, 4, 0, 0, 65535, link_type))

    def write(self, data):
        ts_sec, ts_usec = map(int, str(time.time()).split('.'))
        length = len(data)
        self.pcap_file.write(struct.pack('@ I I I I', ts_sec, ts_usec, length, length))
        self.pcap_file.write(data)

    def read(self):
        raw_data = self.pcap_file.read(16)
        if len(raw_data) == 0:
            return None
        ts_sec, ts_usec, length, length2 = struct.unpack('@ I I I I', raw_data )
        data = self.pcap_file.read(length)
        return {"ts_sec":ts_sec, "ts_usec":ts_usec , "length": length, "data": data}

    def close(self):
        self.pcap_file.close()