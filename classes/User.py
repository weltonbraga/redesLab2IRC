import socket
class User(object):
    """docstring for User"""
    def __init__(self, sock):
        self.sock = sock

        self.userName = ''
        self.realName = ''
        self.hostname = ''
        self.nick = ''

        self.channel = -1

    def setUserName(self, str_userName):
        self.userName = str_userName

    def setRealName(self, str_realName):
        self.realName = str_realName

    def setHostname(self, str_hostname):
        self.hostname = str_hostname

    def setNick(self, str_nick):
        self.nick = str_nick

    def setChannel(self, int_channel):
        self.channel = int_channel

    def getUserName(self):
        return self.userName

    def getRealName(self):
        return self.realName

    def getHostname(self):
        return self.hostname

    def getNick(self):
        return self.nick

    def getChannel(self):
        return self.channel

    def getSocket(self):
        return self.sock
