###First Name: Brendan||||Last Name: Thoeung||||Student ID: 007494550

from datetime import datetime
class Package:
    def __init__(self, id, delivery_address, delivery_city, delivery_zipcode, delivery_deadline, package_weight, delivery_status):
        self.id = id
        self.delivery_address = delivery_address
        self.delivery_deadline = delivery_deadline
        self.delivery_city = delivery_city
        self.delivery_zipcode = delivery_zipcode
        self.package_weight = str(package_weight) + " kilos"
        self.delivery_status = delivery_status
        #self.successfully_delivered = False
        self.package_status = {} # a dictionary containing the package status of all packages at the time of current package delivery
        self.package_status2 = {} #the first method of trying to capture delivery_status didn't work. Trying out a different method.
        self.delivery_time = datetime(year=2022, month=8, day=17, hour=0, minute=0, second=0)
        self.delivery_truck = None
        self.delivered_by = None
        self.vertex_id = None #vertex_id is used to determine which vertex this package will be delivered to that corresponds to the correct delivery_address
        self.found_vertex_address = False
        self.address_updated = False #used for packages with initial incorrect delivery addresses. Switches to True when address has been corrected if need be.

    def __repr__(self):
        return ("package" + str(self.id))

    def update_delivery_status(self, update):
        self.delivery_status = update

    def is_delivered(self):
        if(self.successfully_delivered == True):
            return True
        else:
            return False
    def update_delivery_time(self, delivery_time):
        self.delivery_time = delivery_time
