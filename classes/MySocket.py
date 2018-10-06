import socket, sys, time, select
class MySocket:
    """demonstration class only
      - coded for clarity, not efficiency
    """

    def __init__(self, sock=None):
        self.MSGLEN = 0
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

        self.buffer = 1024
        self.sock.settimeout(2)

    def display(self) :
        user = "\33[33m\33[1m"+" Eu: "+"\33[0m"
        sys.stdout.write(user)
        sys.stdout.flush()

    def getMySocket(self):
        return self.sock

    def connect(self, host, port):
        try:
            self.sock.connect((host, port))
            print ('\33[34m\33[1m [Sucesso] Conectando em {} porta {}. \33[0m'.format(host, port), end= '', flush=False)
        except:
            print ("\33[31m\33[1m \n [Erro] Nao foi possivel conectar ao servidor. \33[0m")
            sys.exit(1)

    def sendNickAndHostname(self, msg):
        usuario = msg
        hostname = socket.gethostname()
        dados = usuario + '\n' + hostname
        #print('dados:', dados, '|enviado!')
        dados = dados.encode()
        self.sock.send(dados)
        primeiro_acesso = False

    def mySend(self, msg):
            message = msg.encode()
            self.sock.sendall(message)

    def mysend_old(self, msg):
        self.MSGLEN = len(msg)
        totalsent = 0
        while totalsent < self.MSGLEN:
            sent = self.sock.send(msg[totalsent:].encode())
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def myreceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < self.MSGLEN:
            chunk = self.sock.recv(min(self.MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)

    def sockLoop(self):
        primeiro_acesso = True
        while True:
            socket_list = [ self.sock, sys.stdin ]

            # Get the list of sockets which are readable
            rList, wList, error_list = select.select(socket_list, [], [], 0)

            time.sleep(.100)
            for sock in rList:

                #incoming message from server
                if sock == self.sock:
                    data = self.sock.recv(self.buffer)

                    if not data:
                        print ('\33[31m\33[1m \n DISCONNECTED!!\n \33[0m')
                        sys.exit()
                    else:
                        data = data.decode()
                        if data[:1] == '!':
                            print(data[1:])
                        else:
                            sys.stdout.write(data)
                        self.display()
                #user entered a message
                else :
                    self.display()
                    msg = sys.stdin.readline()
                    msg = msg[:msg.index('\n')].encode()
                    self.sock.send(msg)
