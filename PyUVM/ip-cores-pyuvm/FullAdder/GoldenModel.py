class GoldenModel():
    def __init__(self):
        self.s=0
        self.c=0

    def check(self, packet):
        self.s=packet.a_i ^ packet.b_i ^ packet.carry_i
        self.c = (packet.a_i & packet.b_i) | (packet.a_i & packet.carry_i) | (packet.b_i & packet.carry_i)

        if packet.sum_o == self.s and packet.carry_o == self.c:
            return True
        else:
            return False