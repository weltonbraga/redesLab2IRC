from classes.MyServerSocket import *

def main():
    host = ''
    num_channels = -1
    if len(sys.argv) == 2:
        arg = sys.argv[1]
        if arg.isalnum():
            num_channels = int(arg)
        else:
            if (arg.count('.') == 3) or (arg.lower() == 'localhost'):
                host = arg.lower()
    else:
        print('\n \tIniciando servidor com ip local.')
        print(' \tÉ possível inserir o IP do servidor ao digitar:')
        print(' \tpython servidor.py <IP>\n')
        print(' \tTambém possível inserir o NUMERO DE CANAIS do servidor:')
        print(' \tpython servidor.py <NUMERO DE CANAIS>\n')

    server = MyServerSocket(num_channels)
    server.listen(host)
    server.run()

if __name__ == '__main__':
    main()
