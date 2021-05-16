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
        # Input from the client for new connection
        if sock == serverSocket:
            clientSocket, clientAddr = serverSocket.accept()
            inputList.append(clientSocket)
            print('Connection from host {}, port {}, socket{}'.format(
                clientAddr[0], clientAddr[1], clientSocket.fileno()))
        else:
            try:
                # receive message from client
                msg = sock.recv(BUFSIZE).decode()
                # msg = msg.split('\r\n')[0]
                # msg = msg[: -2]
                msg = msg[: msg.index('\r')]
                msg += '\n'
                # send message
                for sock_in_list in inputList:
                    if sock_in_list != serverSocket and sock_in_list != sock:
                        try:
                            sock_in_list.send(msg.encode())
                        except:
                            sock_in_list.close()
                            inputList.remove(sock_in_list)
            except:
                # connection end
                for sock_in_list in inputList:
                    if sock_in_list != serverSocket and sock_in_list != sock:
                        try:
                            sock_in_list.send('good bye\n'.encode())
                        except:
                            sock_in_list.close()
                            inputList.remove(sock_in_list)
                print('Connection Closed {}'.format(sock.fileno()))
                inputList.remove(sock)
                sock.close()

serverSocket.close()
