import struct
from general import byteDataToString
from networking.abstract_protocol import AbstractProtocol


class ICMP(AbstractProtocol):

    def __init__(self, raw_data):
        super().__init__()
        self.type, self.code, self.checksum = struct.unpack('! B B H', raw_data[:4])
        self.data = byteDataToString(raw_data[4:])
