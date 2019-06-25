import socket
import struct
from general import *
from networking.ipv4 import IPv4
from networking.arp import ARP
from networking.ipv6 import IPv6
from networking.abstract_protocol import AbstractProtocol

class Ethernet(AbstractProtocol):

    def __init__(self, raw_data):
        super().__init__()
        dest, src, prototype = struct.unpack('! 6s 6s H', raw_data[:14])
        self.dest_mac = get_mac_addr(dest)
        self.src_mac = get_mac_addr(src)
        self.prototype = prototype
        self.proto = socket.htons(prototype)
        self.data = self.__extractNextProtocol(raw_data[14:])

    def __extractNextProtocol(self, data):
        if self.prototype == 2048 :
            return IPv4(data)
        elif self.prototype == 34525:
            return IPv6(data)
        elif self.prototype == 2054:
            return ARP(data)
        return format_multi_line('', data)


