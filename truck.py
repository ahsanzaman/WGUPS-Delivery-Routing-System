import datetime


class Truck:
    def __init__(self, truck_name, mileage, address, delivery_manifest, depart_time):
        self.truck_name = truck_name

        self.mileage = mileage
        self.current_address = address
        self.delivery_manifest = []
        for delivery in delivery_manifest:
            self.delivery_manifest.append(delivery)

        self.depart_time = depart_time
        self.total_time = depart_time

        # constant to track speed
        self.speed = 18

    # trucks travel at 18 mph
    # simulate delivery by:
    # update current address
    # calculate time with distance and speed(18 mph)
    # convert time to seconds
    # update total_time for truck
    # update mileage
    # remove package from manifest
    def perform_delivery(self, address, distance, package_id):
        self.current_address = address
        delivery_time = distance/self.speed
        self.total_time += datetime.timedelta(seconds=delivery_time*60*60)
        self.mileage += distance
        self.delivery_manifest.remove(int(package_id))
        return self.total_time
