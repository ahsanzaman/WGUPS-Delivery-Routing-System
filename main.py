# Ahsan Zaman, Student ID #002765859
import csv
import datetime
from package import Package
from hashmap import HashMap
from truck import Truck

# not using default utf-8 encoding to strip off Byte Order Mark
with open("csv/distance_table.csv", encoding='utf-8-sig') as dtable_file:
    distance_table = csv.reader(dtable_file)
    distance_table = list(distance_table)

with open("csv/packages.csv", encoding='utf-8-sig') as packages_file:
    packages_file = csv.reader(packages_file)
    packages_file = list(packages_file)

with open("csv/addresses.csv", encoding='utf-8-sig') as addresses:
    addresses = csv.reader(addresses)
    addresses = list(addresses)


# uses distance table to find distance between addresses
def calculate_distance(x, y):
    distance = distance_table[int(x)][int(y)]
    if distance == '':
        distance = distance_table[y][x]
    return float(distance)


# returns the index of the address
def address_index(lookup_address):
    index = 0
    for address in addresses:
        if lookup_address in address[1]:
            return index
        index += 1
    print("index not returned")


# reads in package data from the package csv
def read_packages(packages_hashmap):
    for packages in packages_file:
        each_package = Package(packages[0], packages[1], packages[2], packages[3], packages[4], packages[5],
                               packages[6], "at the hub")
        packages_hashmap.insert_item(packages[0], each_package)


# Uses a function in truck to simulate truck delivery in trucks where it takes an address.
# Implements nearest neighbour algorithm to calculate next route.
# Invokes perform_delivery method for truck, which will remove package from manifest after delivery.
# Updates package status.
def run_route(trucks, packages_hashmap):
    for truck in trucks:
        while truck.delivery_manifest:
            closest_address_distance = -1
            closest_package = None
            # finding the closest address in the manifest
            for delivery in truck.delivery_manifest:
                package = packages_hashmap.lookup_item(delivery)
                distance = calculate_distance(address_index(truck.current_address), address_index(package.address))
                # initial condition where a package hasnt been set yet
                if closest_address_distance == -1:
                    closest_package = package
                    closest_address_distance = distance
                # if distance of current package is lower than the current closest distance, set new minimum
                elif distance < closest_address_distance:
                    closest_package = package
                    closest_address_distance = distance
            # once the closest address has been found, perform delivery.
            if closest_address_distance != -1:
                closest_package.delivery_time = truck.perform_delivery(closest_package.address, closest_address_distance, closest_package.package_id)
                closest_package.status = "delivered"
                closest_package.departure_time = truck.depart_time


class Main:
    hub_address = addresses[0][1]

    # creating and initializing hashmap
    packages_hashmap = HashMap()
    read_packages(packages_hashmap)

    # correct address for package 9
    packages_hashmap[9].address = "410 S State St"

    # Instantiating and initializing trucks into a list of trucks
    trucks_list = []

    # manually loading packages
    delivery_manifest = [1, 2, 13, 14, 15, 16, 19, 27, 29, 31, 34, 35, 40]
    trucks_list.append(Truck("Truck A", 0, hub_address, delivery_manifest, datetime.timedelta(hours=8)))
    delivery_manifest = [3, 6, 12, 17, 18, 20, 21, 23, 28, 30, 36, 37, 38, 39]
    trucks_list.append(Truck("Truck B", 0, hub_address, delivery_manifest, datetime.timedelta(hours=9, minutes=5)))
    delivery_manifest = [4, 5, 7, 8, 9, 10, 11, 22, 24, 25, 26, 32, 33]
    trucks_list.append(Truck("Truck C", 0, hub_address, delivery_manifest, datetime.timedelta(hours=10, minutes=20)))

    # trucks running through route using nearest neighbour algorithm
    run_route(trucks_list, packages_hashmap)

    total_mileage = 0
    for truck in trucks_list:
        total_mileage += truck.mileage
        print("Mileage for "+truck.truck_name+": "+'{:7.2f}'.format(truck.mileage))
    print("Total Mileage for the route: "+'{:7.2f}'.format(total_mileage)+" miles")

    # CLI for querying times
    user_input = ""
    while user_input != "q":
        try:
            print('{:^150s}'.format("+++++++WGU Parcel Service (WGUPS)+++++++"))
            user_input = input("Please choose an option or enter q to exit:\n1. Show all packages\n2. Lookup a package\n")

            # look_flag shows if the option to search a specific package with package id was chosen.
            lookup_flag = False
            if user_input == "1":
                lookup_flag = False
            elif user_input == "2":
                lookup_flag = True
            elif user_input == "q":
                break
            else:
                raise ValueError("Incorrect option chosen.")

            # if option 2 is chosen, get the id of the package to search for
            if lookup_flag:
                user_input = input("Please enter id of the package that you want to search: ")
            package_id = user_input

            user_input = input("Enter starting time in format HH:MM:SS (24 hour format) or enter q to quit: ")
            if user_input != "q":
                # alternative to displaying time in timedelta
                # first_time = datetime.datetime.strptime(user_input, "%H:%M:%S")
                # print(datetime.datetime.strftime(first_time, "%I:%M %p"))

                # splitting user input by colon to get hours, min, sec for the time
                (hr, min, sec) = user_input.split(":")

                # printing lines to make data more presentable
                printing_line = "="
                for i in range(1, 150):
                    printing_line += "="
                print(printing_line)

                # printing out headers with appropriate spaces
                print('{:4s} {:^40s} {:^18s} {:7s} {:^10s} {:^10s} {:^7s} {:^12s} {:^15s} {:^20s}'.format("ID", "Address", "City", "State", "Zip", "Deadline", "Weight", "Status", "Departure", "Delivery Time"))

                # printing bottom line below headers to make data more presentable
                printing_line = "-"
                for i in range(1, 150):
                    printing_line += "-"
                print(printing_line)

                # if the option was chosen to search package with id
                # use the id provided to display the package
                if lookup_flag:
                    package = packages_hashmap.lookup_item(package_id)
                    package.update_state(datetime.timedelta(hours=int(hr), minutes=int(min), seconds=int(sec)))
                    print(package.to_string())
                else:
                    # case where all packages need to be displayed
                    # iterating through each package
                    # updating status of each package according to the time entered by user
                    # printing out the package with updated status
                    for i in range(1, 41):
                        package = packages_hashmap.lookup_item(i)
                        package.update_state(datetime.timedelta(hours=int(hr), minutes=int(min), seconds=int(sec)))
                        print(package.to_string())
        except ValueError:
            print("Incorrect value entered. Please try again.")
