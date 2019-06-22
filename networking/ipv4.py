import struct
from networking.abstract_protocol import AbstractProtocol
from networking.icmp import ICMP
from networking.tcp import TCP
from networking.udp import UDP
from networking.pcap import Pcap
from networking.http import HTTP
from general import format_multi_line

class IPv4(AbstractProtocol):

    def __init__(self, raw_data):
        super().__init__()
        version_header_length = raw_data[0]
        self.version = version_header_length >> 4
        self.header_length = (version_header_length & 15) * 4
        self.ttl, self.proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', raw_data[:20])
        self.src = self.ipv4(src)
        self.target = self.ipv4(target)
        self.data = self.__extract_data(raw_data[self.header_length:])

    # Returns properly formatted IPv4 address
    def ipv4(self, addr):
        return '.'.join(map(str, addr))

    def __extract_data(self, data):

        # ICMP
        if self.proto == 1:
            return ICMP(data)
        # TCP
        elif self.proto == 6:
            return TCP(data)
            
        # UDP
        elif self.proto == 17:
            return UDP(data)
        # Other IPv4
        else:
            format_multi_line('', data)