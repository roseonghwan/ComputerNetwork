# Student ID: 20171615
# Name: Seonghwan Noh

import socket
import select
import sys

BUFSIZE = 1024


def display():
    print('Student ID : 20171615')
    print('Name : Seonghwan Noh')


if len(sys.argv) != 2:
    print('Usage: {} <tcpport> \n'.format(sys.argv[0]))
    exit(1)

display()

portNum = int(sys.argv[1])
ip = '127.0.0.1'

# set serverSocket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    serverSocket.bind((ip, portNum))
    serverSocket.listen(8)
    inputList = [serverSocket]

except OSError:
    print('Address already in use!')
    exit()

while True:
    rlist, wlist, xlist = select.select(inputList, [], [])
    for sock in rlist:
        # client new connected
        if sock == serverSocket:
            clientSocket, clientAddr = serverSocket.accept()
            inputList.append(clientSocket)
            print('Connection from host {}, port {}, socket{}'.format(
                clientAddr[0], clientAddr[1], clientSocket.fileno()))
        # else:

serverSocket.close()
