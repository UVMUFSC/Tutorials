class GoldenModel():
    def __init__(self):
        self.s=0
        self.c=0

    def check(self, packet):

        total_sum=int(packet.a_i) + int(packet.b_i)
        self.s=total_sum & 0xF
        self.c = total_sum >> 4

        if packet.sum_o == self.s and packet.carry_o == self.c:
            return True
        else:
            return False