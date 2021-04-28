# Student ID: 20171615
# Name: Seonghwan Noh

import socket
import sys
import os


BUFSIZE = 1024


# get filename, filesize


def send_responseMsg(msg, client_socket):
    filename = msg.split('\r\n')[0].split('/')[1].split()[0]
    sent, filesize = 0, 0

    # print(filename)

    try:
        filesize = os.path.getsize(filename)
    except:
        responseMsg = 'HTTP/1.0 404 NOT FOUND\r\nConnection: close\r\nContent-Length: 0\r\nContent-Type: text/html\r\n\r\n'.encode()
        client_socket.send(responseMsg)
    else:
        responseMsg = (
            'HTTP/1.0 200 OK\r\nConnection: close\r\nContent-Length: {}\r\nContent-Type: text/html\r\n\r\n'.format(filesize)).encode()
        client_socket.send(responseMsg)

        with open(filename, 'rb') as f:
            data = f.read(BUFSIZE)
            while data:
                sent += client_socket.send(data)
                data = f.read(BUFSIZE)

    return sent, filesize, filename


if len(sys.argv) != 2:
    print("usage: %s portnum\n" % sys.argv[0])
    exit()

print("Student ID: 20171615")
print("Name: Seonghwan Noh")

portNum = int(sys.argv[1])
ip = '127.0.0.1'

# set server_socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    serverSocket.bind((ip, portNum))
    serverSocket.listen()
except OSError:
    print('Address already in use!')
    exit()


while True:
    # set client_socket
    clientSocket, clientAddr = serverSocket.accept()
    requestMsg = clientSocket.recv(BUFSIZE).decode()
    header = requestMsg.split('\r\n\r\n')[0]
    header_field_num = len(header.split('\r\n'))-1

    print('Connection : Host IP {}, Port {}, socket {}'.format(
        clientAddr[0], clientAddr[1], clientSocket.fileno()))
    print(requestMsg)
    print('{} headers'.format(header_field_num))

    sent, filesize, filename = send_responseMsg(requestMsg, clientSocket)
    if sent > 0 and filesize > 0:
        print('finish {} {}\n'.format(sent, filesize))
    else:
        print('Server Error : No such file ./{}!\n'.format(filename))
    clientSocket.close()

serverSocket.close()
