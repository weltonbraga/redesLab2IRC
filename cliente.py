from classes.MySocket import MySocket

host  = 'localhost'
port =  10001
buffer = 1024

mySock = MySocket()
mySock.connect(host, port)


usuario = input('\33[34m\33[1m \n Digite o USUARIO: \33[0m')
usuario = usuario.lower()

mySock.mySend(usuario)
mySock.sockLoop()
