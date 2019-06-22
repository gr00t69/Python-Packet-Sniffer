import struct
from networking.icmpv6 import ICMPv6
from general import *

class HopByHop():

    def __init__(self, raw_data):
        self.next_header, self.heLength = struct.unpack('! B B', raw_data[:2])
        if( self.next_header == 58):
            self.data = ICMPv6(raw_data[2:])  
        else:
            self.data = byteDataToString(raw_data)
        