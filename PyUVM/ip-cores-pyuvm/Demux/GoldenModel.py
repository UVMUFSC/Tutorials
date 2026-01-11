class GoldenModel():
    def __init__(self):
        self.y0=0
        self.y1=0
        self.y2=0
        self.y3=0

    def check(self, packet):
        match packet.sel_i:

            case 0:
                self.y0 = packet.x_i
                self.y1 = 0
                self.y2 = 0
                self.y3 = 0
            case 1:
                self.y1 = packet.x_i
                self.y0 = 0
                self.y2 = 0
                self.y3 = 0
            case 2:
                self.y2 = packet.x_i
                self.y1 = 0
                self.y0 = 0
                self.y3 = 0
            case 3:
                self.y3 = packet.x_i
                self.y1 = 0
                self.y2 = 0
                self.y0 = 0
            

        if (packet.y0_o, packet.y1_o, packet.y2_o, packet.y3_o) == (self.y0, self.y1, self.y2, self.y3):
            return True
        else:
            return False