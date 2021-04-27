# Computer Network, 2021
#
# 20171615 - HTTP file server implementation
#
# Author: Seonghwan Noh
# Date: April 26th, 2021
import socket
import sys
import os


BUFSIZE = 1 << 10


def handle_file(msg: str, client_socket) -> (int, int):
    filename = msg.split('\r\n')[0].split('/')[1].split()[0]
    sent, filesize = 0, 0

    print(filename)

    try:
        filesize = os.path.getsize(filename)
    except:
        header = f'HTTP/1.0 404 NOT FOUND\r\nConnection: close\r\nContent-Length: 0\r\nContent-Type: text/html\r\n\r\n'.encode(
        )
        client_socket.send(header)
    else:
        header = f'HTTP/1.0 200 OK\r\nConnection: close\r\nContent-Length: {filesize}\r\nContent-Type: text/html\r\n\r\n'.encode(
        )
        client_socket.send(header)

        with open(filename, 'rb') as f:
            data = f.read(BUFSIZE)
            while data:
                sent += client_socket.send(data)
                data = f.read(BUFSIZE)

    return sent, filesize


if len(sys.argv) != 2:
    print("usage: %s portnum\n" % sys.argv[0])
    exit()

portNum = int(sys.argv[1])
ip = '127.0.0.1'

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((ip, portNum))
serverSocket.listen()

print("Student ID: 20171615")
print("Name: Seonghwan Noh")

while True:
    clientSocket, clientAddr = serverSocket.accept()
    requestMsg = clientSocket.recv(BUFSIZE).decode()
    header = requestMsg.split('\r\n\r\n')[0]
    header_field_len = len(header.split('\r\n'))-1

    print('Connection : Host IP {}, Port {}, socket {}'.format(
        clientAddr[0], clientAddr[1], clientSocket.fileno()))
    print(f'{requestMsg}{header_field_len} headers')

    sent, filesize = handle_file(requestMsg, clientSocket)
    print(f'finish {sent} {filesize}')
    clientSocket.close()

serverSocket.close()
