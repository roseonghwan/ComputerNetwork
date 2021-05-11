import socket, select, sys

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

    name = ""
    # dictionary to store address corresponding to username
    record = {}
    # List to keep track of socket descriptors
    connected_list = []
    buffer = 4096
    port = int(sys.argv[1])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind(("localhost", port))
    server_socket.listen(8)  # listen atmost 10 connection at one time

    # Add server socket to the list of readable connections
    connected_list.append(server_socket)
    display()
    # print("\33[32m \t\t\t\tSERVER WORKING \33[0m")

    while 1:
        # Get the list sockets which are ready to be read through select
        rList, wList, error_sockets = select.select(connected_list, [], [])

        for sock in rList:
            # New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                name = sockfd.recv(buffer)
                name = name.decode()
                connected_list.append(sockfd)
                record[addr] = ""
                print("connection from host %s, port %s," % addr, "socket %s"%sockfd.fileno())
                # print "record and conn list ",record,connected_list

                # if repeated username
                # if name in record.values():
                #     sockfd.send("\r\33[31m\33[1m Username already taken!\n\33[0m")
                #     del record[addr]
                #     connected_list.remove(sockfd)
                #     sockfd.close()
                #     continue
                # else:
                #     # add name and address
                #     record[addr] = name
                #     print("connection from host %s, port %s," % addr, "socket %s"%sockfd.fileno())
                #     # print("connection from host %s, port %s," % addr, " [", record[addr], "]")
                #     sockfd.send("\33[32m\r\33[1m Welcome to chat room. Enter 'tata' anytime to exit\n\33[0m".encode())
                #     send_to_all(sockfd, "\33[32m\33[1m\r " + name + " joined the conversation \n\33[0m")

            # Some incoming message from a client
            else:
                # Data from client
                try:
                    data1 = sock.recv(buffer)
                    data1 = data1.decode()
                    # print "sock is: ",sock
                    data = data1[:data1.index("\n")]
                    # print "\ndata received: ",data

                    # get addr of client sending the message
                    i, p = sock.getpeername()
                    if data == "quit":
                        # msg = "\r\33[1m" + "\33[31m " + record[(i, p)] + " left the conversation \33[0m\n"
                        # send_to_all(sock, msg)

                        print("Connection Closed %s" % sock.fileno())
                        del record[(i, p)]
                        connected_list.remove(sock)
                        sock.close()
                        continue

                    else:
                        msg = data + "\n"
                        send_to_all(sock, msg)

                # abrupt user exit
                except:
                    (i, p) = sock.getpeername()
                    send_to_all(sock, " left the conversation unexpectedly\n")
                    print("Connection Closed %s"%sock.fileno())
                    del record[(i, p)]
                    connected_list.remove(sock)
                    sock.close()
                    continue

    server_socket.close()