import struct
from general import *
from networking.icmpv6 import ICMPv6
from networking.hop_by_hop import HopByHop
from networking.abstract_protocol import AbstractProtocol
from networking.udp import UDP

class IPv6(AbstractProtocol):

    def __init__(self, raw_data):
        super().__init__()
        self.version = raw_data[0] >> 4
        self.priority = ((raw_data[0] & 15 )<<4 ) + (raw_data[1] >> 4 )
        self.flow_label = ((raw_data[1] & 15)<<8 )+raw_data[2]
        self.flow_label = (self.flow_label << 8)+raw_data[3]
        self.pyload_legth, self.next_header, self.hop_limit = struct.unpack(
            '! H B B', raw_data[4:8])  
        self.source_address = get_ipv6_address(raw_data[8:24])
        self.destination_address = get_ipv6_address(raw_data[24:40])
        data = raw_data[40:]
        self.extension_header = self.__extract_extension_header(data)
        self.data = byteDataToString(data)

    def ipv6(self, addr):
        return '.'.join(map(str, addr))

    def __extract_extension_header(self, data):
        if self.next_header == 58:
            return ICMPv6(data)
        elif self.next_header == 0:
            return HopByHop(data)
        elif self.next_header == 17:
            return UDP(data)
        return None