#! /usr/bin/env python3

# Echo client program
import socket, sys, re

from os.path import exists

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive



switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

s = socket.socket(addrFamily, socktype)

if s is None:
    print('could not open socket')
    sys.exit(1)

s.connect(addrPort)

file_to_send = input("type file to send : ")

def utf8len(s):
    return len(s.encode('utf-8'))

if exists(file_to_send):
    file_copy = open(file_to_send, 'r') #open file
    file_data = file_copy.read()    #save contents of file
    if utf8len(file_data) == 0:
        print("cannot send empty file")
        sys.exit(0)
    else:
        framedSend(s, file_data.encode(), debug)
        print("received:", framedReceive(s, debug))

else:
    print("file does not exist.")
    sys.exit(0)
