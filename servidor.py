import socket, select, sys, time
from classes.Usuario import Usuario

class Servidor(object):
    """docstring for Servidor"""
    def __init__(self, host=''):
        print('SERVIDOR')
        # comprimeto máximo de uma mensagem
        self.buffer = 1024

        # dictionary to store address corresponding to username
        self.users_dict={}

        self.server_address = (host, 9999)

        # List to keep track of socket descriptors
        self.connected_list = []

        # Create a TCP/IP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        self.server_socket.bind(self.server_address)
        print('Conectando em {} porta {}'.format(*self.server_address))

        # Listen for incoming connections
        self.server_socket.listen(10)

        # Add server socket to the list of readable connections
        self.connected_list.append(self.server_socket)

        # registra handlers para comandos
        self.handlers = {"/NICK"   : self.nickClientHandler,
                         "/USUARIO": self.newClientHandler,
                         "/SAIR"   : self.deleteClientHandler,
                         "/ENTRAR" : self.subscribeChannelHandler,
                         "/SAIRC"  : self.unsubscribeChannelHandler,
                         "/LISTAR" : self.listChannelHandler,
                        }

    def nickClientHandler(self, list_args):
        clientAddr = list_args.pop(0)
        sock = list_args.pop(0)
        new_nick = ' '.join(list_args.pop(0))

        if new_nick in [a_user.getNick() for a_user in self.users_dict.values()]:
            return '!\r\33[31m\33[1m [Erro] Esse nick já está sendo usado! \33[0m'

        if new_nick:
            old_nick = self.users_dict[clientAddr].getNick()
            msg = '!\33[32m\r\33[1m '+ old_nick +' mudou o nick para ' + new_nick + '. \33[0m'
            self.users_dict[clientAddr].setNick(new_nick)
            self.send_to_all(sock, msg)
            return '!\r\33[34m\33[1m [Sucesso] Seu nick foi alterado. \33[0m'

        return '!\r\33[31m\33[1m [Erro] Nick invalido. Digite /nick <seu nick> \33[0m'

    def newClientHandler(self, clientAddr, args):
        print('new client')

    def deleteClientHandler(self, list_args ):
        clientAddr = list_args.pop(0)
        sock = list_args.pop(0)
        user_nick = self.users_dict[clientAddr].getNick()
        #print('\n      delete client\n')
        msg = "\r\33[1m"+"\33[31m "+ user_nick +" saiu do canal. \33[0m\n"
        self.send_to_all(sock, msg)
        print ("Client {} is offline [{}]".format(clientAddr, user_nick))
        del self.users_dict[clientAddr]
        self.connected_list.remove(sock)
        sock.close()
        #print('      fim delete client\n')
        return

    def subscribeChannelHandler(self, clientAddr, args):
        pass

    def unsubscribeChannelHandler(self, clientAddr, args):
        pass

    def listChannelHandler(self, clientAddr, args):
        pass

    def send_to_host(self, sock, msg):
        message = msg.encode()
        try :
            sock.sendall(message)
        except :
            # if connection not available
            sock.close()
            self.connected_list.remove(sock)
        return

    def send_to_all (self, sock, msg):
        print('manda...')
        message = msg.encode()
        #Message not forwarded to server and sender itself
        for socket in self.connected_list:
            if socket != self.server_socket and socket != sock :
                try :
                    socket.sendall(message)
                except :
                    # if connection not available
                    socket.close()
                    self.connected_list.remove(socket)
        return

    def run(self):
        try:
            while True:
                time.sleep(.100)
                # Get the list sockets which are ready to be read through select
                rList,wList,error_sockets = select.select(self.connected_list,[],[], 0)
                #print('l:', len(rList))
                for sock in rList:
                    #print('sock:', sock)
                    #New connection
                    if sock is self.server_socket:
                        print('Recebido')
                        # Handle the case in which there is a new connection recieved through server_socket
                        new_sock, address = self.server_socket.accept()
                        #print('hn:', socket.getaddress(),'| ip?', address, ' | peer: ', new_sock.getsockname() )

                        data = new_sock.recv(self.buffer)
                        data = data.decode()
                        try:
                            user_nick, hostname = data.split('\n')
                        except:
                            new_sock.close()
                            print("Conexão falhou: nome de usuario invalido")
                            continue
                        self.connected_list.append(new_sock)
                        self.users_dict[address] = Usuario()
                        #print ("self.users_dict and conn list ",self.users_dict,self.connected_list)

                        # if repeated username
                        if user_nick in [a_user.getNick() for a_user in self.users_dict.values()]: #if user_nick in self.users_dict.values():
                            message = "\r\33[31m\33[1m [Erro] Esse nick já está sendo usado! \n\33[0m"
                            message = message.encode()
                            new_sock.send(message)
                            del self.users_dict[address]
                            self.connected_list.remove(new_sock)
                            new_sock.close()
                            continue
                        else:
                            # add user_nick and address
                            self.users_dict[address].setNick(user_nick)
                            self.users_dict[address].setHostname(hostname)
                            print ("Client {} connected [{}]".format(address, self.users_dict[address].getNick()))
                            message = "\33[32m\r\33[1m Bem vindo ao chat. \n\33[0m"
                            message = message.encode()
                            new_sock.sendall(message)
                            self.send_to_all(new_sock, "\33[32m\33[1m\r "+ user_nick + " entrou no canal. \n\33[0m")
                            # print('n:',new_sock.getpeername())

                    #Some incoming message from a client
                    else:
                        # Data from client
                        print('Data from client')
                        try:
                            data = sock.recv(self.buffer)
                            data = data.decode()
                            ip, port = sock.getpeername()
                            if not data:
                                self.send_to_all(sock, "\r\33[31m \33[1m" + self.users_dict[(ip,port)].getNick() + " saiu do canal inesperadamente.\33[0m\n")
                                del self.users_dict[(ip,port)]
                                self.connected_list.remove(sock)
                                sock.close()
                            else:
                                command = ''
                                args = []
                                if data[:1] == '/': # é comando
                                    print('Eh um comando')
                                    data_list = data.split()
                                    command = data_list.pop(0).upper()
                                    args = data_list.copy()
                                    if command in self.handlers:
                                        resp = self.handlers[command]([address, sock, args])
                                        if resp:
                                            self.send_to_host(sock, resp)
                                            print(resp)
                                    else:
                                        msg = '!\r\33[31m\33[1m [Erro] Comando invalido. \33[0m'
                                        self.send_to_host(sock, msg)
                                else:
                                    msg = "\r\33[1m"+"\33[35m " + self.users_dict[(ip,port)].getNick() +": "+"\33[0m"+data+"\n"
                                    self.send_to_all(sock, msg)

                        #abrupt user exit
                        except:
                            print('deu ruim')
                            (ip,port)=sock.getpeername()
                            self.send_to_all(sock, "\r\33[31m \33[1m"+ self.users_dict[(ip,port)].getNick() +" saiu do canal inesperadamente.\33[0m\n")
                            print ("Client {} is offline (error) [{}]".format((ip,port), self.users_dict[(ip,port)].getNick()))
                            del self.users_dict[(ip,port)]
                            self.connected_list.remove(sock)
                            sock.close()

                            continue
        except KeyboardInterrupt :
            self.server_socket.close()
            print('\nServidor desconectado.')

def main():
    host = ''
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        print('\n \tIniciando servidor com ip local.')
        print(' \tÉ possível inserir um ip para o servidor ao digitar:')
        print(' \tpython servidor.py <endereço ip>\n')
        host = socket.gethostbyname(socket.gethostname())

    s = Servidor(host)
    s.run()

if __name__ == '__main__':
    main()
