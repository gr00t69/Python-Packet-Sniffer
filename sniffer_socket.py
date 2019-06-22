#!/usr/bin/env python

# WS server that sends messages at random intervals

import asyncio
import datetime
import random
# pip install websockets
import websockets
import socket
from networking.pcap import Pcap
from networking.ethernet import Ethernet
import sys
import json
import time
import asyncio
import threading

fila = []

def read():
    pcap = Pcap('capture.pcap')
    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    global fila
    while True:
        raw_data, addr = conn.recvfrom(65535)
        pcap.write(raw_data)
        eth = Ethernet(raw_data)

        fila.append(eth)  
        print("[r] fila:{}".format(len(fila)))  
        time.sleep( 0.3)

    pcap.close()

async def show(websocket, path):
    filter = ['ipv4', 'ipv6', 'other']
    idx = 0
    if len(sys.argv)>1:
        filter = sys.argv[1:]
    print("[s] Filter: {}".format(filter))
    global fila
    while True:
        print("[s] {} {}".format(idx, len(fila)))  
        if idx >= len(fila):
            time.sleep( 0.5 )
            continue
        eth = fila[idx]
        idx = idx+1

        await websocket.send(eth.toJSON())
        await asyncio.sleep(0.2)

x = threading.Thread(target=read)
x.start()

start_server = websockets.serve(show, '127.0.0.1', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()