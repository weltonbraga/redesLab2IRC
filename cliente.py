from classes.MyClientSocket import *

def main():
    host = ''
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        print('\n \tIniciando cliente com ip local.')
        print(' \tÉ possível inserir um ip para o servidor ao digitar:')
        print(' \tpython cliente.py <endereço ip>\n')


    nick = input('\33[32m\r\33[1m \n Digite o USUARIO: \33[0m')
    nick = nick.lower()

    mySock = MyClientSocket()
    mySock.connect(host)

    mySock.sendNickAndHostname(nick)
    mySock.sockLoop()

if __name__ == '__main__':
    main()
