class GoldenModel():
    def __init__(self):
        self.s=0
        self.c=0

    def check(self, packet):
        self.s=packet.a ^ packet.b
        self.c = packet.a & packet.b

        if packet.s == self.s and packet.c == self.c:
            return True
        else:
            return False