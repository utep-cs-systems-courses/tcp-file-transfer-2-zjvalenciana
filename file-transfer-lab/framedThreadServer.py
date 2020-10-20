#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params, os
from os.path import exists
from threading import Thread, enumerate, Lock 
from time import time, sleep 

global dictionary
global dictLock
dictLock = Lock()
dictionary = dict()

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

from threading import Thread;
from encapFramedSock import EncapFramedSock

class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.fsock = EncapFramedSock(sockAddr)
    def run(self):
        global dictionary, dictLock
        print("new thread handling connection from", self.addr)
        while True:
            payload = self.fsock.receive(debug) #recieve file name to be saved
            if debug: print("rec'd: ", payload)
            if not payload:     # done
                if debug: print(f"thread connected to {addr} done")
                self.fsock.close() #possible error
                return          # exit
            payload = payload.decode() #recieve byte array and convert to string 
            #self.fsock.send(payload, debug)
            if exists(payload):
                self.fsock.send(b"True", debug)
            else:
                print("1")
                dictLock.acquire()
                print('2')
                #payloadString = str(payload) 
                currentCheck = dictionary.get(payload)
                print(dictionary)
                if currentCheck == 'running':
                    self.fsock.send(b"True", debug)
                    print('3')
                    dictLock.release()
                    print('4')
                    print("the file is currently being transfered, exiting now")
                else:
                    print('5')
                    dictionary[payload] = "running"
                    dictLock.release()
                    sleep(100)
                    print('6')
                    self.fsock.send(b"False", debug) #recieving file data 
                    try:
                        payload2 = self.fsock.receive(debug)
                    except:
                        print("connection lost while recieving.")
                        sys.exit(0)

                    if not payload2:
                        break
                    payload2 += b"!"             # make emphatic!
                    try:
                        self.fsock.send(payload2, debug)
                    except:
                        print("------------------------------")
                        print("connection lost while sending.")
                        print("------------------------------")

                    output = open(payload, 'wb') #open and set to write byte array
                    output.write(payload2) #writing to file 
                    print('7')
                    dictLock.acquire()
                    del dictionary[payload]
                    print('8')
                    dictLock.release()
                    print('9')
                    output.close()
        self.fsock.close()
        

while True:
    sockAddr = lsock.accept()
    server = Server(sockAddr)
    server.start()