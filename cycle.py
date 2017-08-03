from data import LEDnet

class Cycle:

    def __init__(self, name, mode, target, time, values=None):
        self.name = name
        self.mode = mode
        self.target = target
        self.time = time
        self.values = values

    def get_name(self):
        return self.name

    def get_mode(self):
        return self.mode

    def get_target(self):
        return self.target

    def get_time(self):
        return self.time

    def get_values(self):
        return self.values
