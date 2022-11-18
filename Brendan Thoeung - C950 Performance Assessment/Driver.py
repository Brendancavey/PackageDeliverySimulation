###First Name: Brendan||||Last Name: Thoeung||||Student ID: 007494550

class Driver:
    def __init__(self, name):
        self.name = name
        self.attitude = "Has a need for speed"
        self.return_time = None

    def __repr__(self):
        return self.name