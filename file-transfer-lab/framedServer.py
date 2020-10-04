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

#sock, addr = lsock.accept()

#print("connection rec'd from", addr)


from framedSock import framedSend, framedReceive

while True:

    sock, addr = lsock.accept()
    print("connection rec'd from", addr)
    if not os.fork():
        while True:
            payload = framedReceive(sock, debug)
            #if debug: print("rec'd: ", payload)
            if not payload:
                break
                    # make emphatic!
            #framedSend(sock, payload, debug)
            payload = payload.decode()
            

            if exists(payload):
                framedSend(sock, b"True", debug)
            else:
                framedSend(sock, b"False", debug)
                try:
                    payload2 = framedReceive(sock, debug)
                except:
                    print("connection lost while recieving.")
                    sys.exit(0)
                #if debug: print("rec'd: ", payload2)
                if not payload2:
                    break
                payload2 += b"!"             # make emphatic!
                try:
                    framedSend(sock, payload2, debug)
                except:
                    print("------------------------------")
                    print("connection lost while sending.")
                    print("------------------------------")
                    #sys.exit(0)
                #payload = payload.decode()
                output = open(payload, 'wb')
                output.write(payload2)
                sys.exit(0)
        sock.close()
        f#ork.close()