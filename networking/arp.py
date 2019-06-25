import struct
from general import *
from general import get_mac_addr
from networking.icmpv6 import ICMPv6
from networking.tcp import TCP
from networking.hop_by_hop import HopByHop
from networking.abstract_protocol import AbstractProtocol
from networking.udp import UDP

class ARP(AbstractProtocol):

    def __init__(self, raw_data):
        super().__init__()
        (self.hardware_type, self.protocol_type,self.h_addres_length, self.p_addres_length,
            self.opcod )= struct.unpack('! H H B B H', raw_data[:8])
        print(len(raw_data[8:28]))
        (self.sender_h_addres, self.sender_p_addres, self.target_h_addres,
            self.target_p_addres) = struct.unpack(
            '! 6s 4s 6s 4s', raw_data[8:28])
        
        self.sender_h_addres = get_mac_addr(self.sender_h_addres)
        self.target_h_addres = get_mac_addr(self.target_h_addres)