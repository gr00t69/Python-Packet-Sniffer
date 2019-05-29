import struct


class IPv6:

    def __init__(self, raw_data):
        self.version = raw_data[0] >> 4
        self.priority = ((raw_data[0] & 15 )<<4 ) + (raw_data[1] >> 4 )
        self.flow_label = ((raw_data[1] & 15)<<8 )+raw_data[2]
        self.flow_label = (self.flow_label << 8)+raw_data[3]
        
        self.pyload_legth, self.next_header, self.hop_limit = struct.unpack('! H B B', raw_data[4:8])
        
        self.source_address = ""
        self.destination_address = ""
        for i in range(8, 24):
            self.source_address =self.source_address +("{:02x}".format(raw_data[i]))
            self.destination_address =self.destination_address +("{:02x}".format(raw_data[i+16]))
            if(i%2!=0):
                self.source_address = self.source_address+":"
                self.destination_address = self.destination_address+":"

    def ipv6(self, addr):
        return '.'.join(map(str, addr))