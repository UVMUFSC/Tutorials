class GoldenModel():
    def __init__(self):
        self.mealy_o=0
        self.next_state=0
        self.current_state=0

    def check(self, packet):
        self.current_state = packet.current_state
        self.mealy_o = 0

        if(packet.rst_i == 0):
            self.next_state = 0
            self.mealy_o = 0
                
        else:
            match packet.current_state:
                case 0:
                    if(packet.mealy_i):
                        self.next_state = 1
                    else:
                        self.next_state = 0
                case 1:
                    if(packet.mealy_i):
                        self.next_state = 1
                    else:
                        self.next_state = 2
                case 2:
                    if(packet.mealy_i):
                        self.next_state = 3
                    else:
                        self.next_state = 0
                case 3:
                    if(packet.mealy_i):
                        self.next_state = 1
                    else:
                        self.next_state = 0
                        self.mealy_o = 1
                case _:
                    self.mealy_o = 0
                    self.next_state = 0


        if (self.mealy_o, self.current_state, self.next_state) == (packet.mealy_o, packet.current_state, packet.next_state):
            return True
        else:
            return False