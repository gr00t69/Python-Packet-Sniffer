import socket
from general import *
from networking.ethernet import Ethernet
from networking.ipv4 import IPv4
from networking.ipv6 import IPv6
from networking.icmp import ICMP
from networking.tcp import TCP
from networking.udp import UDP
from networking.pcap import Pcap
from networking.http import HTTP
# pip install websockets
import websockets
import argparse
import sys
import json
import time
import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
from multiprocessing import Process, Pool
import threading

idShow = 0
thRead = None
TAB_1 = '\t - '
fila = []

def show():
    filter = ['ipv4', 'ipv6', 'other']
    idx = 0
    if args.filter != None:
        filter = args.filter
    print("[s] Filter: {}".format(filter))
    global fila
    while True:
        if idx >= len(fila):
            time.sleep( 0.5 )
            continue
        eth = fila[idx]
        idx = idx+1
        # IPv4
        if eth.prototype == 2048 and 'ipv4' in filter:
            print(TAB_1 + 'IPv4 Packet:')
            print( eth.toJSON())
        elif eth.prototype == 34525 and 'ipv6' in filter:
            print(TAB_1 + 'IPv6 Packet:')
            print( eth.toJSON())
        elif  'other' in filter:
            if  eth.prototype == 2054:
                print("ARP protocol:")  
            print("Prototype: {}".format(eth.prototype))
            print( eth.toJSON())

        time.sleep( 0.1)

def read():
    conn = None
    if args.file != None:
        pcap = Pcap(args.file, True,1)
    else:
        pcap = Pcap('capture.pcap')
        conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

    global fila
    while True:
        if conn!= None:
            raw_data, addr = conn.recvfrom(65535)
            pcap.write(raw_data)
        else:
            line = pcap.read()
            if(line==None):
                return
            raw_data = line['data']
        
        eth = Ethernet(raw_data)

        fila.append(eth)
        time.sleep( 0.3)

    pcap.close()

async def showSocket(websocket, path):
    global idShow
    midShow = idShow
    idShow = idShow+1
    filter = ['ipv4', 'ipv6', 'other']
    idx = 0
    if len(sys.argv)>1:
        filter = sys.argv[1:]
    print("[s] Filter: {}".format(filter))
    global fila
    while True:
        print("[s-{}] {} {}".format(midShow, idx, len(fila)))  
        if idx >= len(fila):
            time.sleep( 0.5 )
            continue
        eth = fila[idx]
        idx = idx+1

        await websocket.send(eth.toJSON())
        await asyncio.sleep(0.2)

# HTTPRequestHandler class
class SnifferHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    def startRead(self):
        global thRead
        if(thRead == None):
            thRead = threading.Thread(target=read)
            thRead.start()

    def startServer(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        start_server = websockets.serve(showSocket, '127.0.0.1', 5678)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    # GET
    def do_GET(self):
        print(self.path)
        self.startRead()
        thRead = threading.Thread(target=self.startServer)
        thRead.start()
        content = self.handle_http()
        self.wfile.write(content)

    def handle_http(self):
        response_content = ""
        response_content = open("index.html")
        response_content = response_content.read()

        self.send_response(200)
        self.send_header('Content-type', "text/html")
        self.end_headers()
        return bytes(response_content, "UTF-8")

def runServer():
  print('starting server...')

  server_address = ('127.0.0.1', 8081)
  httpd = HTTPServer(server_address, SnifferHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()

def normalMode():  
    global fila
    x = threading.Thread(target=read)
    x.start()

    y = threading.Thread(target=show)
    y.start()

def socketMode():
    thServer = threading.Thread(target=runServer)
    thServer.start()    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', help="filename", type= str)
    parser.add_argument('--filter', '-s', help="filter: ipv4, ipv6", type= str)
    parser.add_argument('--server', '-w', help="mode server", action='store_true', default=False)
    args = parser.parse_args()
    if args.server: 
        socketMode()
    else:
        normalMode()
