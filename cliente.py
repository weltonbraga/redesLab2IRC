import socket, select, string, sys
import time


def display() :
    you="\33[33m\33[1m"+" Eu: "+"\33[0m"
    sys.stdout.write(you)
    sys.stdout.flush()

'''
CONECTADO = True
DESCONECTADO = False
STATUS['CONECTADO']
'''
# Create a TCP/IP socket
# ->1 # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10001)
buffer = 1024
# ->2 # sock.connect(server_address)


# Create a TCP/IP socket faz a mesma coisa de ->1 e ->2 juntos
print('\33[34m\33[1m Client. Conecting... \33[0m', end= '', flush=False)

try:
    mySock = socket.create_connection(server_address)
except:
    print ("\33[31m\33[1m \n Can't connect to the server \33[0m")
    sys.exit(1)

mySock.settimeout(2)
ip, porta = mySock.getpeername()

print('\33[34m\33[1m{} porta {} \33[0m'.format(ip, porta))


usuario = input('\33[34m\33[1m Digite o USUARIO: \33[0m')
usuario = usuario.lower().encode()
mySock.sendall(usuario)
#display()

while True:
    socket_list = [ mySock, sys.stdin ]

    # Get the list of sockets which are readable
    rList, wList, error_list = select.select(socket_list, [], [], 0)

    time.sleep(.100)
    #print('l',len(rList))
    for sock in rList:
        #print('\ns:', sock)

        #incoming message from server
        if sock == mySock:
            #print("server")
            data = sock.recv(buffer)

            if not data:
                print ('\33[31m\33[1m \r DISCONNECTED!!\n \33[0m')
                sys.exit()
            else:
                #print('hmm')
                data = data.decode()
                sys.stdout.write(data)
                display()
        #user entered a message
        else :
            #print("eu\n")
            msg = sys.stdin.readline()
            msg = msg[:msg.index('\n')].encode()
            mySock.sendall(msg)
            display()
