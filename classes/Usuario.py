class Usuario(object):
    """docstring for Usuario"""
    def __init__(self):
        super(Usuario, self).__init__()
        self.nomeUsuario = ''
        self.nomeReal = ''
        self.nick = ''

    def setNomeUsuario(self, arg):
        self.nomeUsuario = arg

    def setNomeReal(self, arg):
        self.nomeReal = arg

    def setNick(self, arg):
        self.nick = arg

    def getNomeUsuario(self):
        return self.nomeUsuario

    def getNomReal(self):
        return self.nomeReal

    def getNick(self):
        return self.nick
