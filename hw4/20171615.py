# Student ID: 20171615
# Name: Seonghwan Noh

import socket
import select
import sys

BUFSIZE = 1024


def display():
    print('Student ID : 20171615')
    print('Name : Seonghwan Noh')


def order(msg):
    msg_list = msg.split()
    if msg_list[0] == '@talk':
        host_name = msg_list[1]
        tc_port = int(msg_list[2])
        clientSocket.connect((host_name, tc_port))
        inputList.append(clientSocket)
    elif msg_list[0] == '@quit':
        exit()
    else:
        msg = user_id + ' : ' + msg
        clientSocket.send(msg.encode())
    print(user_id + '>')


if len(sys.argv) != 3:
    print('Usage: {} <tcpport> \n'.format(sys.argv[0]))
    exit(1)

display()

ip = '127.0.0.1'
port_num = int(sys.argv[1])
user_id = sys.argv[2]

# set serverSocket, clientSocket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    serverSocket.bind((ip, port_num))
    serverSocket.listen()
    inputList = [serverSocket, sys.stdin]

except OSError:
    print('Address already in use!')
    exit()

print(user_id + ">")

while True:
    rlist, wlist, xlist = select.select(inputList, [], [])
    for sock in rlist:
        # Input from the client for new connection
        if sock == serverSocket:
            clientSocket, clientAddr = serverSocket.accept()
            inputList.append(clientSocket)
            print(
                f'connection from host {clientAddr[0]}, port {clientAddr[1]}, socket {clientSocket.fileno()}')
        # order(stdin)
        elif sock == sys.stdin:
            msg = sys.stdin.readline()
            order(msg)
        # input data in client
        else:
            data = sock.recv(BUFSIZE).decode()
            if data:
                print(data)
            # client close socket
            else:
                print(f'Connection Closed {sock.fileno()}')
                inputList.remove(sock)
                sock.close()


serverSocket.close()
