import struct


class IPv6:

    def __init__(self, raw_data):
        self.version = raw_data[0] >> 4
        self.priority = ((raw_data[0] & 15 )<<4 ) + (raw_data[1] >> 4 )
        self.flow_label = ((raw_data[1] & 15)<<8 )+raw_data[2]
        self.flow_label = (self.flow_label << 8)+raw_data[3]
        self.pyload_legth = (raw_data[4]<<8)+raw_data[5]
        self.next_header = raw_data[6]
        self.hop_limit = raw_data[7]

        self.source_addres =0
        self.destination_addres =0
        for i in range(8, 11):
            self.source_addres = self.source_addres <<8 + raw_data[i]
            self.destination_addres = self.destination_addres << 8 +raw_data[i+4]
            
        


        # self.ttl, self.proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', raw_data[:20])
        # self.src = self.ipv6(src)
        # self.target = self.ipv6(target)
        # self.data = raw_data[self.header_length:]

    # Returns properly formatted IPv4 address
    def ipv6(self, addr):
        return '.'.join(map(str, addr))