import datetime


class Package:
    def __init__(self, package_id, address, city, state, zipcode, delivery_deadline, mass, status):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.delivery_deadline = delivery_deadline
        self.mass = mass
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    # package status gets changed according to whatever time user enters
    # also setting address for package #9 since it gets corrected at 10:20
    def update_state(self, user_time):
        # setting statuses
        if self.delivery_time < user_time:
            self.status = "delivered"
        elif (self.delivery_time > user_time) & (self.departure_time < user_time):
            self.status = "en route"
        else:
            self.status = "at the hub"

        # setting address for package 9
        if (user_time >= datetime.timedelta(hours=10, minutes=20)) & (self.package_id == "9"):
            self.address = "410 S State St"
        elif self.package_id == "9":
            self.address = "300 State St"

    # prints out each package in a neat table format
    def to_string(self):
        return_str = '{:4s} {:40s} {:18s} {:7s} {:10s}'.format(self.package_id, self.address, self.city, self.state, self.zipcode)
        departure_time = "--------"
        delivery_time = "--------"
        if self.status == "delivered":
            delivery_time = str(self.delivery_time)
            departure_time = str(self.departure_time)
        elif self.status == "en route":
            departure_time = str(self.departure_time)
        return_str += '{:^10s} {:^7s} {:^12s} {:^15s} {:^20s}'.format(self.delivery_deadline, self.mass, self.status, departure_time, delivery_time)
        return return_str
