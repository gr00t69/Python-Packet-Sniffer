## To Do

- Added support for IPV6, HopByHop, ICMPv6 and ARP
- Added WEB interface via web socket
- Changed structure for packaging Protocols by level of hierarchy
- Added filter per IP protocol version
- Added reading per file
-----------------------

Comnado filter:
>sniffer.py --filter [arp, ipv4, ipv6]<br>
This command tells the program which packets to fetch. If no filter
the captured packets will be IPv4.

erver command:
>sniffer.py --server<br>
This command initializes the local server, thus allowing the view in the browser
captured packet information. This information is displayed in real time and displays all available information from the filtered packet. To access the preview page,
if you type in the address bar of the localhost browser: 8081.

Command file:<br>
>sniffer.py --file filename<br>
This command loads the ".pcap" file. The path of the file should be
is in the same directory as the sniffer.py file.
