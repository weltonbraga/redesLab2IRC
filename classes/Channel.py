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
