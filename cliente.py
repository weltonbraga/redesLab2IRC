from classes.MySocket import MySocket
import sys

def main():
    host = ''
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        print('\n \tIniciando cliente com ip local.')
        print(' \tÉ possível inserir um ip para o servidor ao digitar:')
        print(' \tpython cliente.py <endereço ip>\n')
        host  = 'localhost'
    port = 9999
    buffer = 1024

    mySock = MySocket()
    mySock.connect(host, port)

    nick = input('\33[34m\33[1m \n Digite o USUARIO: \33[0m')
    nick = nick.lower()

    mySock.sendNickAndHostname(nick)
    mySock.sockLoop()

if __name__ == '__main__':
    main()
