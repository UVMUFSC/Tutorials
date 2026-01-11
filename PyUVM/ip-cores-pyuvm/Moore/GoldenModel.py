class GoldenModel():
    def __init__(self):
        self.out=0
        self.previous_state=0
        self.current_state=0

    def check(self, packet):
        self.previous_state = packet.previous_state

        match packet.previous_state:
            case 0:
                self.out = 0
                if(packet.next_i):
                    self.current_state = 1
            case 1:
                self.out = 0
                if(not packet.next_i):
                    self.current_state = 2
                else:
                    self.current_state = 1
            case 2:
                self.out = 0
                if(packet.next_i):
                    self.current_state = 3
                else:
                    self.current_state = 0
            case 3:
                self.out = 0
                if(packet.next_i):
                    self.current_state = 4
                else:
                    self.current_state = 2
            case 4:
                self.out = 1
                if(packet.next_i):
                    self.current_state = 1
                else:
                    self.current_state = 2
            case _:
                self.out = 0
                self.current_state = 0

        match packet.rst_i:
            case 1:
                self.out = 0
                self.current_state = 0

        if (self.out, self.previous_state, self.current_state) == (packet.out_o, packet.previous_state, packet.current_state):
            return True
        else:
            return False