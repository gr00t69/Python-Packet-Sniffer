import textwrap
import struct


# Returns MAC as string from bytes (ie AA:BB:CC:DD:EE:FF)
def get_mac_addr(mac_raw):
    # need python 3
    byte_str = map('{:02x}'.format, mac_raw)
    mac_addr = ':'.join(byte_str).upper()
    return mac_addr

# Return an IPv6 address
def get_ipv6_address(raw_data):
    address = ":".join(
        map('{:04x}'.format, struct.unpack('! H H H H H H H H', raw_data)))
    return address.replace(":0000:","::" ).replace(":::", "::").replace(":::", "::")


# Formats multi-line data
def format_multi_line(prefix, string, size=80):
    size -= len(prefix)
    if isinstance(string, bytes):
        string = ''.join(r'\x{:02x}'.format(byte) for byte in string)
        if size % 2:
            size -= 1
    return '\n'.join([prefix + line for line in textwrap.wrap(string, size)])

icmp_typs = {
0:'Reserved',
1:'Destination Unreachable',
2:'Packet Too Big',
3:'Time Exceeded',
4:'Parameter Problem',
# 5-99	Unassigned	
100:'Private experimentation',
101:'Private experimentation',
# 102-126	Unassigned	
127:'Reserved for expansion of ICMPv6 error messages',
128:'Echo Request',
129:'Echo Reply',
130:'Multicast Listener Query',
131:'Multicast Listener Report',
132:'Multicast Listener Done',
133:'Router Solicitation',
134:'Router Advertisement',
135:'Neighbor Solicitation',
136:'Neighbor Advertisement',
137:'Redirect Message',
138:'Router Renumbering',
139:'ICMP Node Information Query',
140:'ICMP Node Information Response',
141:'Inverse Neighbor Discovery Solicitation Message',
142:'Inverse Neighbor Discovery Advertisement Message',
143:'Version 2 Multicast Listener Report',
144:'Home Agent Address Discovery Request Message',
145:'Home Agent Address Discovery Reply Message',
146:'Mobile Prefix Solicitation',
147:'Mobile Prefix Advertisement',
148:'Certification Path Solicitation Message',
149:'Certification Path Advertisement Message',
150:'ICMP messages utilized by experimental mobility protocols such as Seamoby',
151:'Multicast Router Advertisement',
152:'Multicast Router Solicitation',
153:'Multicast Router Termination',
154:'FMIPv6 Messages',
155:'RPL Control Message',
156:'ILNPv6 Locator Update Message',
157:'Duplicate Address Request',
158:'Duplicate Address Confirmation',
159:'MPL Control Message',
160:'Extended Echo Request',
161:'Extended Echo Reply',
# 162-199	Unassigned	
200:'Private experimentation',
201:'Private experimentation',
255:'Reserved for expansion of ICMPv6 informational messages'
}