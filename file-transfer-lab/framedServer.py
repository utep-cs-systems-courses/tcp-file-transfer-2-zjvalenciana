#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params
from os.path import exists

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", True), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

sock, addr = lsock.accept()

print("connection rec'd from", addr)


from framedSock import framedSend, framedReceive

while True:
    payload = framedReceive(sock, debug)
    if debug: print("rec'd: ", payload)
    if not payload:
        break
              # make emphatic!
    #framedSend(sock, payload, debug)
    payload = payload.decode()
    

    if exists(payload):
        framedSend(sock, b"True", debug)
    else:
        framedSend(sock, b"False", debug)
        payload2 = framedReceive(sock, debug)
        if debug: print("rec'd: ", payload2)
        if not payload2:
            break
        payload2 += b"!"             # make emphatic!
        framedSend(sock, payload2, debug)
        #payload = payload.decode()
        output = open(payload, 'wb')
        output.write(payload2)
        '''overw = input("want overwrite the filed you entered? ")
        if overw == 'yes':
            output = open(output_file, 'wb')
            #payload = payload.decode('utf8')
            output.write(payload)
        else:
            pass
    else:
        output = open(output_file, 'wb')
        #payload = payload.decode('utf8')
        output.write(payload) '''