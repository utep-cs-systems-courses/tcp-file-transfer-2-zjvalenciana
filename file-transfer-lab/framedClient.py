#! /usr/bin/env python3

# Echo client program
import socket, sys, re

sys.path.append("../lib")       # for params
import params
from os.path import exists
from encapFramedSock import EncapFramedSock


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

sock = socket.socket(addrFamily, socktype)

if sock is None:
    print('could not open socket')
    sys.exit(1)

sock.connect(addrPort)

fsock = EncapFramedSock((sock, addrPort))

file_to_send = input("type file to send : ")



if exists(file_to_send):
    file_copy = open(file_to_send, 'rb') #open file
    file_data = file_copy.read()    #save contents of file
    file_copy.close()
    if len(file_data) == 0:
        print("cannot send empty file")
        sys.exit(0)
    else:
        file_name = input("give us file name : ") #prompt for file name to be saved on server
        fsock.send(file_name.encode(), debug) #encode to convert to byte array
        file_exists = fsock.receive(debug) #server will return true or false
        file_exists = file_exists.decode()
        if file_exists == 'True':
            print("file already exists in server")
            sys.exit(0)
        else:            
            try:
                fsock.send(file_data, debug)
            except:
                print("------------------------------")
                print("connection lost while sending.")
                print("------------------------------")
                sys.exit(0)
            try:
                fsock.receive(debug)
            except:
                print("------------------------------")
                print("connection lost while receiving.")
                print("------------------------------")
                sys.exit(0)

else:
    print("file does not exist.")
    sys.exit(0)