import struct
from networking.abstract_protocol import AbstractProtocol
from general import byteDataToString


class TCP(AbstractProtocol):

    def __init__(self, raw_data):
        super().__init__()
        (self.src_port, self.dest_port, self.sequence, self.acknowledgment, offset_reserved_flags,
            self.window_size, self.checksum) = struct.unpack('! H H L L H H H', raw_data[:18])
        offset = (offset_reserved_flags >> 12) * 4
        self.flag_urg = (offset_reserved_flags & 32) >> 5
        self.flag_ack = (offset_reserved_flags & 16) >> 4
        self.flag_psh = (offset_reserved_flags & 8) >> 3
        self.flag_rst = (offset_reserved_flags & 4) >> 2
        self.flag_syn = (offset_reserved_flags & 2) >> 1
        self.flag_fin = offset_reserved_flags & 1
        self.data = self.__extract_next( raw_data[offset:])

    def __extract_next(self, raw_data):
        if len(raw_data) > 0:
            # HTTP
            if self.src_port == 80 or self.dest_port == 80:
                try:                   
                    return HTTP(self.data)
                except:
                    return byteDataToString(raw_data)

        return byteDataToString(raw_data)