import struct
from networking.abstract_protocol import AbstractProtocol

class UDP(AbstractProtocol):

    def __init__(self, raw_data):
        super().__init__()
        self.src_port, self.dest_port, self.size = struct.unpack('! H H 2x H', raw_data[:8])
        self.data = raw_data[8:]
