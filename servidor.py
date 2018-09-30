# https://pymotw.com/3/socket/tcp.html
import socket, select, sys

def send_to_all (sock, msg):
    print('manda...')
    message = msg.encode()
    #Message not forwarded to server and sender itself
    for socket in connected_list:
        if socket != server_socket and socket != sock :
            try :
                socket.sendall(message)
            except :
                # if connection not available
                socket.close()
                connected_list.remove(socket)


print('SERVIDOR')
buffer = 1024
#dictionary to store address corresponding to username
record={}
# List to keep track of socket descriptors
connected_list = []

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10001)
print('starting up on {} port {}'.format(*server_address))
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(10)

# Add server socket to the list of readable connections
connected_list.append(server_socket)

while True:
    # Get the list sockets which are ready to be read through select
    rList,wList,error_sockets = select.select(connected_list,[],[], 0)
    #print('l:', len(rList))
    for sock in rList:
        #print('sock:', sock)
        #New connection
        if sock is server_socket:
            print('server')
            # Handle the case in which there is a new connection recieved through server_socket
            sockfd, addr = server_socket.accept()
            name = sockfd.recv(buffer)
            name = name.decode()
            connected_list.append(sockfd)
            record[addr]=""
            #print ("record and conn list ",record,connected_list)

            #if repeated username
            if name in record.values():
                mensagem = "\r\33[31m\33[1m Username already taken!\n\33[0m"
                mensagem = mensagem.encode()
                sockfd.send(mensagem)
                del record[addr]
                connected_list.remove(sockfd)
                sockfd.close()
                continue
            else:
                #add name and address
                record[addr] = name
                print ("Client {} connected [{}]".format(addr, record[addr]))
                mensagem = "\33[32m\r\33[1m Welcome to chat room.\n\33[0m"
                mensagem = mensagem.encode()
                sockfd.sendall(mensagem)
                send_to_all(sockfd, "\33[32m\33[1m\r "+ name + " joined the conversation \n\33[0m")
                print('n:',sockfd.getpeername())

        #Some incoming message from a client
        else:
            # Data from client
            print('Data from client')
            try:
                data = sock.recv(buffer)

                ip, porta = sock.getpeername()
                if not data:
                    send_to_all(sock, "\r\33[31m \33[1m"+record[(ip,porta)]+" left the conversation unexpectedly\33[0m\n")
                    del record[(ip,porta)]
                    connected_list.remove(sock)
                    sock.close()
                else:
                    data = data.decode()
                    msg = "\r\33[1m"+"\33[35m "+record[(ip,porta)]+": "+"\33[0m"+data+"\n"
                    send_to_all(sock, msg)

            #abrupt user exit
            except:
                print('aki')
                (ip,porta)=sock.getpeername()
                send_to_all(sock, "\r\33[31m \33[1m"+record[(ip,porta)]+" left the conversation unexpectedly\33[0m\n")
                print ("Client {} is offline (error) [{}]".format((ip,porta),record[(ip,porta)]))
                del record[(ip,porta)]
                connected_list.remove(sock)
                sock.close()
                continue



server_socket.close()
