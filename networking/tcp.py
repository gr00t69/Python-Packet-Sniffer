import struct
from networking.abstract_protocol import AbstractProtocol


class TCP(AbstractProtocol):

    def __init__(self, raw_data):
        super().__init__()
        (self.src_port, self.dest_port, self.sequence, self.acknowledgment, offset_reserved_flags) = struct.unpack(
            '! H H L L H', raw_data[:14])
        offset = (offset_reserved_flags >> 12) * 4
        self.flag_urg = (offset_reserved_flags & 32) >> 5
        self.flag_ack = (offset_reserved_flags & 16) >> 4
        self.flag_psh = (offset_reserved_flags & 8) >> 3
        self.flag_rst = (offset_reserved_flags & 4) >> 2
        self.flag_syn = (offset_reserved_flags & 2) >> 1
        self.flag_fin = offset_reserved_flags & 1
        self.data = raw_data[offset:]
        self.__extract_next()

    def __extract_next(self):
        if len(self.data) > 0:
            # HTTP
            if self.src_port == 80 or self.dest_port == 80:
                try:                   
                    self.data  = HTTP(self.data)
                except:
                    self.data = self.data