class GoldenModel():
    def __init__(self):
        self.y=0

    def check(self, packet):
        match packet.sel_i:

            case 0:
                self.y = packet.x0_i
            case 1:
                self.y = packet.x1_i
            case 2:
                self.y = packet.x2_i
            case 3:
                self.y = packet.x3_i
            

        if packet.y_o == self.y:
            return True
        else:
            return False