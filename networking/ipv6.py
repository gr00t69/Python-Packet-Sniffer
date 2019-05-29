import struct
from general import *

class IPv6:

    def __init__(self, raw_data):
        self.version = raw_data[0] >> 4
        self.priority = ((raw_data[0] & 15 )<<4 ) + (raw_data[1] >> 4 )
        self.flow_label = ((raw_data[1] & 15)<<8 )+raw_data[2]
        self.flow_label = (self.flow_label << 8)+raw_data[3]
        
        self.pyload_legth, self.next_header, self.hop_limit = struct.unpack('! H B B', raw_data[4:8])  
        self.source_address = get_ipv6_address(raw_data[8:24])
        self.destination_address2 = get_ipv6_address(raw_data[24:40])
        
    def ipv6(self, addr):
        return '.'.join(map(str, addr))