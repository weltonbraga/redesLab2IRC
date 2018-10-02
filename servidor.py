# https://pymotw.com/3/socket/tcp.html
import socket, select, sys, time
from classes.Usuario import Usuario

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
users_dict={}
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
    time.sleep(.100)
    # Get the list sockets which are ready to be read through select
    rList,wList,error_sockets = select.select(connected_list,[],[], 0)
    #print('l:', len(rList))
    for sock in rList:
        #print('sock:', sock)
        #New connection
        if sock is server_socket:
            print('server')
            # Handle the case in which there is a new connection recieved through server_socket
            new_sock, hostname = server_socket.accept()
            message = "\r\33[34m\33[1m \n Digite o seu USUARIO:\n \33[0m"
            message = message.encode()
            new_sock.send(message)
            user_name = new_sock.recv(buffer)

            message = "\r\33[34m\33[1m \n Digite o seu APELIDO:\n \33[0m"
            message = message.encode()
            new_sock.send(message)
            nickname  = new_sock.recv(buffer)

            user_name = user_name.decode()
            connected_list.append(new_sock)
            users_dict[hostname] = Usuario()
            users_dict[hostname].setNomeUsuario(user_name)
            users_dict[hostname].setNick(nickname)
            #print ("users_dict and conn list ",users_dict,connected_list)

            #if repeated username
            if user_name in [a_user.getNomeUsuario() for a_user in users_dict.values()]: #if user_name in users_dict.values(): 
                message = "\r\33[31m\33[1m Username already taken!\n\33[0m"
                message = message.encode()
                new_sock.send(message)
                del users_dict[hostname]
                connected_list.remove(new_sock)
                new_sock.close()
                continue
            else:
                #add user_name and address
                users_dict[hostname] = user_name
                print ("Client {} connected [{}]".format(hostname, users_dict[hostname]))
                message = "\33[32m\r\33[1m Welcome to chat room.\n\33[0m"
                message = message.encode()
                new_sock.sendall(message)
                send_to_all(new_sock, "\33[32m\33[1m\r "+ user_name + " joined the conversation \n\33[0m")
                print('n:',new_sock.getpeername())

        #Some incoming message from a client
        else:
            # Data from client
            print('Data from client')
            try:
                data = sock.recv(buffer)

                ip, porta = sock.getpeername()
                if not data:
                    send_to_all(sock, "\r\33[31m \33[1m"+users_dict[(ip,porta)]+" left the conversation unexpectedly\33[0m\n")
                    del users_dict[(ip,porta)]
                    connected_list.remove(sock)
                    sock.close()
                else:
                    data = data.decode()
                    msg = "\r\33[1m"+"\33[35m "+users_dict[(ip,porta)]+": "+"\33[0m"+data+"\n"
                    send_to_all(sock, msg)

            #abrupt user exit
            except:
                print('aki')
                (ip,porta)=sock.getpeername()
                send_to_all(sock, "\r\33[31m \33[1m"+users_dict[(ip,porta)]+" left the conversation unexpectedly\33[0m\n")
                print ("Client {} is offline (error) [{}]".format((ip,porta),users_dict[(ip,porta)]))
                del users_dict[(ip,porta)]
                connected_list.remove(sock)
                sock.close()
                continue

server_socket.close()
