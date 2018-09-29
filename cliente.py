import socket
import sys
'''
CONECTADO = True
DESCONECTADO = False
STATUS['CONECTADO']
'''
print('CLIENTE')
# Create a TCP/IP socket
# ->1 # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10001)

# ->2 # sock.connect(server_address)


# Create a TCP/IP socket faz a mesma coisa de ->1 e ->2 juntos
print('conectando em {} porta {}'.format(*server_address))
sock = socket.create_connection(server_address)

try:
    while True:
        # codifica mensagem do teclado
        message = input('Digite uma mensagem: ') #message = 'olá servidor!'.encode()

        # Create a TCP/IP socket faz a mesma coisa de ->1 e ->2 juntos
        print('conectando em {} porta {}'.format(*server_address))

        # Send data
        print('enviando {}' .format(message))
        sock.sendall(message.encode())

        # Look for the response
        amount_received = 0
        amount_expected = len(message)

        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            data = data.decode()
            print('recebido {}'.format(data))

        # ctrl + D para sair
        if message == '\x04':
            print('saindo ...')
            break

finally:
    print('desconectando do socket')
    sock.close()
