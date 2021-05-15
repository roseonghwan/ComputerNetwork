import socket
import select
import sys


def display():
    print("Student ID : 20175163")
    print("Name : ParkJeongHwan")

# Function to send message to all connected clients


def send_to_all(sock, message):
    # Message not forwarded to server and sender itself
    for socket in connected_list:
        if socket != server_socket and socket != sock:
            try:
                socket.send(message.encode())
            except:
                # if connection not available
                socket.close()
                connected_list.remove(socket)


if __name__ == "__main__":
    record = {}
    connected_list = []
    buffer = 4096
    port = int(sys.argv[1])
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", port))
    server_socket.listen(10)
    connected_list.append(server_socket)
    display()

    while 1:
        rList, wList, error_sockets = select.select(connected_list, [], [])

        for sock in rList:
            # New connection
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                connected_list.append(sockfd)
                record[addr] = ""
                print("connection from host %s, port %s," %
                      addr, "socket %s" % sockfd.fileno())
            else:
                try:
                    data1 = sock.recv(buffer)
                    data1 = data1.decode()
                    data = data1[:data1.index("\n")]
                    i, p = sock.getpeername()
                    # print((i, p)), ip, port
                    if data == "quit":
                        print("Connection Closed %s" % sock.fileno())
                        del record[(i, p)]
                        connected_list.remove(sock)
                        sock.close()
                        continue
                    else:
                        msg = data + "\n"
                        send_to_all(sock, msg)
                except:
                    (i, p) = sock.getpeername()
                    send_to_all(sock, " left the conversation unexpectedly\n")
                    print("Connection Closed %s" % sock.fileno())
                    del record[(i, p)]
                    connected_list.remove(sock)
                    sock.close()
                    continue

    server_socket.close()
