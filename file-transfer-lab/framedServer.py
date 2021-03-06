#! /usr/bin/env python3

import sys, os
sys.path.append("../lib")       # for params
import re, socket, params
from os.path import exists

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
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

from framedSock import framedSend, framedReceive

while True:

    sock, addr = lsock.accept()
    print("connection rec'd from", addr)
    if not os.fork(): #if youre a child do following 
        while True:
            payload = framedReceive(sock, debug) #recieve file name to be saved 

            if not payload:
                break

            payload = payload.decode() #recieve byte array and convert to string 
            

            if exists(payload):
                framedSend(sock, b"True", debug)
            else:
                framedSend(sock, b"False", debug) #recieving file data 
                try:
                    payload2 = framedReceive(sock, debug)
                except:
                    print("connection lost while recieving.")
                    sys.exit(0)

                if not payload2:
                    break
                payload2 += b"!"             # make emphatic!
                try:
                    framedSend(sock, payload2, debug)
                except:
                    print("------------------------------")
                    print("connection lost while sending.")
                    print("------------------------------")

                output = open(payload, 'wb') #open and set to write byte array
                output.write(payload2) #writing to file 
                output.close()
                sock.close() 