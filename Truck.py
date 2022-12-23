###Author: Brendan Thoeung

class Truck:
    def __init__(self,truck_id, driver, departure_time):
        self.driver = driver
        self.max_capacity = 16
        self.avg_speed = 18
        self.container_of_packages = []
        self.truck_id = truck_id
        self.departure_time = departure_time
        self.return_time = None

    def __repr__(self):
        return "truck" + str(self.truck_id)
    def load(self, package):
        if(len(self.container_of_packages) < 16):
            self.container_of_packages.append(package)
        else:
            print("Unable to load package. Truck is full.")

    def is_full(self):
        if(len(self.container_of_packages) >= self.max_capacity):
            return True
        else:
            return False

    def is_not_full(self):
        if(len(self.container_of_packages) < self.max_capacity):
            return True
        else:
            return False

    def contains_packages(self):
        if(len(self.container_of_packages) > 0):
            return True
        else:
            return False

    def is_empty(self):
        if(len(self.container_of_packages) <= 0):
            return True
        else:
            return False
    def contains_driver(self):
        if(self.driver != None):
            return True
        else:
            return False
    def print_container(self):
        print(self.container_of_packages)
