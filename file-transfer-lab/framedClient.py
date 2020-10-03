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

if exists(file_to_send):
    file_copy = open(file_to_send, 'rb') #open file
    file_data = file_copy.read()    #save contents of file
    if len(file_data) == 0:
        print("cannot send empty file")
        sys.exit(0)
    else:
        file_name = input("give us file name ")
        framedSend(s, file_name.encode(), debug)
        file_exists = framedReceive(s, debug)
        file_exists = file_exists.decode()
        if file_exists == 'True':
            print("file already exists in server")
            sys.exit(0)
        else:            
            framedSend(s, file_data, debug)
            print("received:", framedReceive(s, debug))

else:
    print("file does not exist.")
    sys.exit(0)
