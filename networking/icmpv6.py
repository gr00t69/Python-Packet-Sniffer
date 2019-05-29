import struct
from networking.icmp import ICMP

class ICMPv6(ICMP):

    def __init__(self, raw_data):
        super().__init__(raw_data)
        