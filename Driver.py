###Author: Brendan Thoeung

class Driver:
    def __init__(self, name):
        self.name = name
        self.attitude = "Has a need for speed"
        self.return_time = None

    def __repr__(self):
        return self.name