class Usuario(object):
    """docstring for Usuario"""
    def __init__(self, sock):
        self.sock = sock
        self.channel = -1

        self.nomeUsuario = ''
        self.nomeReal = ''
        self.hostname = ''
        self.nick = ''

    def setNomeUsuario(self, arg):
        self.nomeUsuario = arg

    def setNomeReal(self, arg):
        self.nomeReal = arg

    def setHostname(self, arg):
        self.hostname = arg

    def setNick(self, arg):
        self.nick = arg

    def setChannel(self, arg):
        self.channel = arg

    def getNomeUsuario(self):
        return self.nomeUsuario

    def getNomReal(self):
        return self.nomeReal

    def getHostname(self):
        return self.hostname

    def getNick(self):
        return self.nick

    def getSocket(self):
        return self.sock

    def getChannel(self):
        return self.channel
