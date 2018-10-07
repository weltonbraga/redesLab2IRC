import socket, select, sys, time
from classes.Usuario import Usuario

class Channel(object):
    numChannels = 0
    def __init__(self):
        self.users_online = 0
        self.my_number = Channel.numChannels

        Channel.numChannels += 1

    def userJoin(self):
        self.users_online += 1

    def userLeft(self):
        self.users_online -= 1

    def getMyNumber(self):
        return self.my_number

    def getOnlineCount(self):
        return self.users_online

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

        self.lobby_channel = 0

        self.channels_amount = 5

        self.channels_list = [Channel() for num in range(0, self.channels_amount)]

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
        address = list_args.pop(0)
        new_nick = ' '.join(list_args.pop(0))
        sock = self.users_dict[address].getSocket() #sock = list_args.pop(0)

        if new_nick in [a_user.getNick() for a_user in self.users_dict.values()]:
            return '!\r\33[31m\33[1m [Erro] Esse nick já está sendo usado! \33[0m'

        if new_nick:
            old_nick = self.users_dict[address].getNick()
            msg = '!\33[32m\r\33[1m '+ old_nick +' mudou o nick para ' + new_nick + '. \33[0m'
            self.users_dict[address].setNick(new_nick)
            self.sendToChannel(self.users_dict[address], msg)
            return '!\r\33[34m\33[1m [Sucesso] Seu nick foi alterado. \33[0m'

        return '!\r\33[31m\33[1m [Erro] Nick invalido. Digite /nick <seu nick> \33[0m'

    def newClientHandler(self, address, args):
        print('new client')

    def deleteClientHandler(self, list_args ):
        address = list_args.pop(0)
        sock = self.users_dict[address].getSocket() #sock = list_args.pop(0)
        user_nick = self.users_dict[address].getNick()
        #print('\n      delete client\n')
        msg = "\r\33[1m"+"\33[31m "+ user_nick +" saiu do canal. \33[0m\n"
        self.sendToChannel(self.users_dict[address], msg)
        print ("Client {} is offline [{}]".format(address, user_nick))
        self.channels_list[self.users_dict[address].getChannel()].userLeft()
        del self.users_dict[address]
        self.connected_list.remove(sock)
        sock.close()

        #print('      fim delete client\n')
        return

    def subscribeChannelHandler(self, list_args):
        print('l:',list_args)
        address = list_args.pop(0)
        #sock = self.users_dict[address].getSocket() #sock = list_args.pop(0)
        old_ch_num = self.users_dict[address].getChannel()
        print('l:',list_args)
        try:
            number = ' '.join(list_args.pop(0))
            print('n:', number)
            new_ch_num = int(number)
            if new_ch_num in [ch.getMyNumber() for ch in self.channels_list[1:] ]:
                if new_ch_num == old_ch_num:
                    return '!\r\33[31m\33[1m [Erro] Voce ja esta conectado no canal ' + str(new_ch_num) + '. \33[0m'
                self.users_dict[address].setChannel(new_ch_num)
                self.channels_list[old_ch_num].userLeft()
                self.channels_list[new_ch_num].userJoin()
                msg = '!\33[32m\33[1m \n '+ self.users_dict[address].getNick() +' entrou no canal. \33[0m'
                self.sendToChannel(self.users_dict[address], msg)
                return '!\r\33[34m\33[1m [Sucesso] Voce entrou no canal ' + str(new_ch_num) +'. \33[0m'
            return '!\r\33[31m\33[1m [Erro] Esse canal nao existe. \33[0m '

        except ValueError:
            return '!\r\33[31m\33[1m [Erro] Digite um numero de canal valido. \33[0m '


    def unsubscribeChannelHandler(self, args_list):
        address = args_list.pop(0)
        user = self.users_dict[address]
        num_channel = user.getChannel()
        if num_channel == self.lobby_channel:
            return '!\r\33[31m[1m [Erro] Voce nao esta em um canal. \33[0m '
        self.channels_list[num_channel].userLeft()
        user.setChannel(self.lobby_channel)

        msg = '!\33[31m\33[1m \n Voce saiu do canal '+ str(num_channel) +'. \33[0m \n'
        sock = user.getSocket()
        self.sendToHost(sock, msg)
        msg = '!\33[31m\33[1m \n ' + user.getNick() + ' saiu do canal. \33[0m \n'
        self.sendToChannel(user, msg)

    def listChannelHandler(self, args_list):
        return '\33[32m\r\33[1m Todos os canais disponiveis:\n' +\
                '\n'.join(['  (' + str(ch.getMyNumber()) + ') : usuários online ['+ str(ch.getOnlineCount()) +']' for ch in self.channels_list[1:]]) + \
                '\33[0m \n'

    def sendToHost(self, sock, msg):
        message = msg.encode()
        try :
            sock.sendall(message)
        except :
            # if connection not available
            sock.close()
            self.connected_list.remove(sock)
        return

    def sendToChannel (self, sender, msg):
        print('manda...')
        message = msg.encode()
        #Message not forwarded to server and sender itself
        for user in self.users_dict.values():
            if user.getChannel() == sender.getChannel():
                if user != sender:
                    try:
                        user.getSocket().sendall(message)
                    except:
                        # if connection not available
                        print('sendToChannel - Error ')
                        self.channels_list[sender.getChannel()].userLeft()
                        user.getSocket().socket.close()
                        self.connected_list.remove(user.getSocket())
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

                        # Handle the case in which there is a new connection recieved through server_socket
                        new_sock, address = self.server_socket.accept()
                        print('   Novo user', address)
                        #print('hn:', socket.getaddress(),'| ip?', address, ' | peer: ', new_sock.getsockname() )

                        data = new_sock.recv(self.buffer)
                        data = data.decode()
                        print('   data: ', data)
                        try:
                            user_nick, hostname = data.split('\n')
                        except:
                            new_sock.close()
                            print("Conexão falhou: nome de usuario invalido")
                            continue

                        self.connected_list.append(new_sock)

                        self.users_dict[address] = Usuario(new_sock)


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
                            self.users_dict[address].setChannel(self.lobby_channel)
                            print ("Client {} connected [{}]".format(address, self.users_dict[address].getNick()))
                            message = '!\n\33[32m\r\33[1m ### Bem vindo ao chat ### \n'
                            #message += self.handlers['/LISTAR']()
                            message += '\n Digite /LISTAR para ver lista de canais. \33[0m\n'
                            self.sendToHost(new_sock, message)

                            self.sendToChannel(self.users_dict[address], "!\33[32m\33[1m \n "+ user_nick + " entrou no canal. \33[0m \n")
                            # print('n:',new_sock.getpeername())

                    #Some incoming message from a client
                    else:
                        # Data from client

                        try:
                            data = sock.recv(self.buffer)
                            data = data.decode()
                            address = sock.getpeername()
                            print('Data from client:', address)
                            if not data:
                                self.sendToChannel(self.users_dict[address], "!\33[31m \33[1m " + self.users_dict[address].getNick() + " saiu do canal inesperadamente.\33[0m\n")
                                del self.users_dict[address]
                                self.connected_list.remove(sock)
                                sock.close()
                            elif data[:1] == '/': # é comando
                                print('Eh um comando')
                                data_list = data.split()
                                command = data_list.pop(0).upper()
                                args = data_list.copy()
                                if command in self.handlers:
                                    resp = self.handlers[command]([address, args])
                                    if resp:
                                        self.sendToHost(sock, resp)
                                        print(resp)
                                else:
                                    msg = '!\r\33[31m\33[1m [Erro] Comando invalido. \33[0m'
                                    self.sendToHost(sock, msg)
                            else:
                                if self.users_dict[address].getChannel() == self.lobby_channel:
                                    msg = '!\n\33[32m\r\33[1m Digite /entrar <numero> para entrar num canal. \33[0m'
                                    self.sendToHost(sock, msg)
                                else:
                                    msg = "\r\33[1m"+"\33[35m " + self.users_dict[address].getNick() +": "+"\33[0m"+data+"\n"
                                    self.sendToChannel(self.users_dict[address], msg)

                        #abrupt user exit
                        except KeyboardInterrupt:
                            print('deu ruim')
                            address=sock.getpeername()
                            self.sendToChannel(self.users_dict[address], "\r\33[31m \33[1m"+ self.users_dict[address].getNick() +" saiu do canal inesperadamente.\33[0m\n")
                            print ("Client {} is offline (error) [{}]".format(address, self.users_dict[address].getNick()))
                            del self.users_dict[address]
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
