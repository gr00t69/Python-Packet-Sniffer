import struct
from networking.icmpv6 import ICMPv6
from networking.udp import UDP
from general import *
from networking.abstract_protocol import AbstractProtocol

class HopByHop(AbstractProtocol):

    def __init__(self, raw_data):
        super().__init__()
        self.next_header, self.heLength = struct.unpack('! B B', raw_data[:2])
        self.data = self.__extract_extension_header(raw_data[2:])  

    def __extract_extension_header(self, data):
        if self.next_header == 58:
            return ICMPv6(data)
        elif self.next_header == 17:
            return UDP(data)
        return byteDataToString(data)        