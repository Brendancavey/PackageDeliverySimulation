###Author: Brendan Thoeung

import math
import csv
from datetime import datetime
from datetime import timedelta

from MyHashTable import MyHashTable
from Package import Package
from Graph import Graph
from Graph import Vertex

from Truck import Truck
from Driver import Driver

departure_time = datetime(year=2022, month=8, day=17, hour=8, minute=0, second=0)  # keeps track of the time to determine the status of any package at any given time, and keeps track if a package was delivered on time. Also default time to each truck
Driver1 = Driver("Speedy Sam")
Driver2 = Driver("Nascar Nevil")
Truck1 = Truck(1, Driver1, departure_time)
Truck2 = Truck(2, Driver2, departure_time)
Truck3 = Truck(3, None, departure_time)
list_of_trucks = [Truck1, Truck2, Truck3]
list_of_available_drivers = [] #while Driver1 and Driver2 are assigned initially to Truck1 and Truck2, list of available drivers is initially empty
adjacency_matrix = Graph()
package_hash_table = MyHashTable()
location_dictionary = {} # I want to correspond the delivery address of each package to the correct delivery location.
package_queue = [] #used to determine which packages have yet to be loaded
special_case_packages = [] #used to store special condition packages. Want to keep separate from the normal package_queue
special_case_late_packages = [] #used to store all late packages coming into the hub
packages_must_be_in_truck2 = [] #packages with the condition that must be on truck 2
packages_must_be_delivered_together = [] # packages with the condition that must be delivered together (on the same truck)
list_of_verticies = []  # keeps track of list of verticies when adding into adjacenecy_matrix. Needed because we need to refer back to these verticies when adding edge
list_of_packages = [] #keeps track of all the packages that come into the hub
distance_travelled = 0 #keeps track of the total distance travelled for all trucks moving between verticies
#delivery_status = {} #key - value dictionary that will contain the status of all packages at a given time, where the key is time, and the value is another dictionary containing all packages, and its delivery status for the given
delivery_status2 = {}#the first method of capturing delivery status didnt work. Trying out a new method. It works! Sticking with it.
user_request = None #keeps track of what the user will look up a package by

def capture_all_package_status():
    #captures all package status at any given time and not just times at delivery
    for each_package in list_of_packages:
        for i in range(0, len(list_of_packages)):

            if ((list_of_packages[i].id == 6 or list_of_packages[i].id == 25 or list_of_packages[i].id == 28 or list_of_packages[i].id == 32) and each_package.delivery_time < datetime(year=2022, month=8, day=17, hour=9, minute=5, second=0)):
                each_package.package_status2[list_of_packages[i]] = "At Hub"
            elif (each_package.delivery_time < list_of_packages[i].delivery_time and list_of_packages[i].delivery_truck.departure_time < each_package.delivery_time):
                each_package.package_status2[list_of_packages[i]] = "On Route"
            elif(each_package.delivery_time >= list_of_packages[i].delivery_time):
                each_package.package_status2[list_of_packages[i]] = "Delivered"

            else:#(list_of_packages[i].delivery_time == datetime(year=2022, month=8, day=17, hour=0, minute=0, second=0)):
                each_package.package_status2[list_of_packages[i]] = "At Hub"

    for each_package in list_of_packages:
        delivery_status2[str(each_package.delivery_time)] = each_package.package_status2

    ##CAPTURING INITIAL 8:01AM STATUS TIME################################
    #status between 8am and time of first delivery have not been captured. Need to check for this edge case.
    lift_off_time = datetime(year=2022, month=8, day=17, hour=8, minute=1, second=0)
    initial_package_status_after_8am = {}

    for i in range(0, len(list_of_packages)):
        # Since the trucks iterate 1 after another, need to simulate truck 1 and 2 left at the same time. If a package was delivered from a previous iteration, and their time of delivery is less greater than lift off time and they weren't at the hub, then they were on route.
        #Truck 3 doesnt lift off until after truck1 comes back, so packages delivered by truck3 couldnt have been on route at lift_off_time. Packages 6, 25, 28, and 32 are not ready to be loaded into trucks until after 9:05am, so they must be at hub at lift_off_time.
        if(package_hash_table.search(list_of_packages[i].id)[1].delivery_truck.truck_id == 3 or list_of_packages[i].id == 6 or list_of_packages[i].id == 25 or list_of_packages[i].id == 28 or list_of_packages[i].id == 32):
            initial_package_status_after_8am[package_hash_table.search(list_of_packages[i].id)[1]] = "At Hub"
        elif(package_hash_table.search(list_of_packages[i].id)[1].delivery_time > lift_off_time and package_hash_table.search(list_of_packages[i].id)[1].delivery_truck.truck_id != 3):
            initial_package_status_after_8am[package_hash_table.search(list_of_packages[i].id)[1]] = "On Route"  # loading delivery status of all packages into dictionary "initial package status after 8am"

    delivery_status2[str(lift_off_time)] = initial_package_status_after_8am  # placing dictionary "initial package status after 8am" into the delivery status at "lift off time"


def look_up_package(by_user_request):
    print_package_info_how_many_times = 0
    #print("User request requested was " + str(user_request))
    if(user_request == 1): #1 corresponds to look up by ID
        id = by_user_request
        print_package_info_how_many_times = 1
    if(user_request == 2): #2 corresponds to look up by delivery_address
        list_of_matching_delivery_addresses_id = []
        index = 0
        for i in range(1, len(list_of_packages)+1):
            if(by_user_request == package_hash_table.search(i)[1].delivery_address):
                list_of_matching_delivery_addresses_id.append(package_hash_table.search(i)[1].id)
        print_package_info_how_many_times = len(list_of_matching_delivery_addresses_id)
        if (len(list_of_matching_delivery_addresses_id) == 0):
            print("No packages found with delivery address: " + str(by_user_request))
            return
        id = list_of_matching_delivery_addresses_id[index]
        print("All packages that have the delivery address (" + str(by_user_request) + ") are :")
    if(user_request == 3): #3 corresponds to delivery city
        list_of_matching_delivery_city_id = []
        index = 0
        for i in range(1, len(list_of_packages)+1):
            if(by_user_request == package_hash_table.search(i)[1].delivery_city):
                list_of_matching_delivery_city_id.append(package_hash_table.search(i)[1].id)
        print_package_info_how_many_times = len(list_of_matching_delivery_city_id)
        if (len(list_of_matching_delivery_city_id) == 0):
            print("No packages found with delivery city: " + str(by_user_request))
            return
        id = list_of_matching_delivery_city_id[index]
        print("All packages that have the delivery city (" + str(by_user_request) + ") are :")
    if (user_request == 4):  # 4 corresponds to  zipcode
        list_of_matching_delivery_zip_code_id = []
        index = 0
        for i in range(1, len(list_of_packages) + 1):
            if (by_user_request == package_hash_table.search(i)[1].delivery_zipcode):
                list_of_matching_delivery_zip_code_id.append(package_hash_table.search(i)[1].id)
        print_package_info_how_many_times = len(list_of_matching_delivery_zip_code_id)
        if (len(list_of_matching_delivery_zip_code_id) == 0):
            print("No packages found with delivery zipcode: " + str(by_user_request))
            return
        id = list_of_matching_delivery_zip_code_id[index]
        print("All packages that have the delivery zipcode (" + str(by_user_request) + ") are :")
    if (user_request == 5):  # 5 corresponds to  weight
        list_of_matching_weight_id = []
        index = 0
        for i in range(1, len(list_of_packages) + 1):
            if (str(by_user_request) + " kilos" == str(package_hash_table.search(i)[1].package_weight)):
                list_of_matching_weight_id.append(package_hash_table.search(i)[1].id)
        print_package_info_how_many_times = len(list_of_matching_weight_id)
        if (len(list_of_matching_weight_id) == 0):
            print("No packages found with weight: " + str(by_user_request))
            return
        id = list_of_matching_weight_id[index]
        print("All packages that have package weight of (" + str(by_user_request) + ") are :")
    if (user_request == 6):  # 6 corresponds to  deadline
        list_of_matching_delivery_deadline_id = []
        index = 0
        for i in range(1, len(list_of_packages) + 1):
            if (by_user_request == package_hash_table.search(i)[1].delivery_deadline):
                list_of_matching_delivery_deadline_id.append(package_hash_table.search(i)[1].id)
        print_package_info_how_many_times = len(list_of_matching_delivery_deadline_id)
        if (len(list_of_matching_delivery_deadline_id) == 0):
            print("No packages found with delivery deadline: " + str(by_user_request))
            return
        id = list_of_matching_delivery_deadline_id[index]
        print("All packages that have the delivery deadline (" + str(by_user_request) + ") are :")
    if (user_request == 7):  # 7 corresponds to  delivery_status
        list_of_matching_delivery_status_code_id = []
        index = 0
        for i in range(1, len(list_of_packages) + 1):
            if (by_user_request == package_hash_table.search(i)[1].delivery_status):
                list_of_matching_delivery_status_code_id.append(package_hash_table.search(i)[1].id)
        print_package_info_how_many_times = len(list_of_matching_delivery_status_code_id)
        if (len(list_of_matching_delivery_status_code_id) == 0):
            print("No packages found with delivery status: " + str(by_user_request))
            return
        id = list_of_matching_delivery_status_code_id[index]
        print("All packages that have the delivery status (" + str(by_user_request) + ") are :")
    # need to verify if the item located at the index using the hash function doesn't return false. If it is not empty, then we may
    #proceed to obtain the item attributes located at that hash table
    while(print_package_info_how_many_times > 0):
        print("--------------------------------------------------------")
        if(user_request == 2):

            id = list_of_matching_delivery_addresses_id[index]
            if (index < len(list_of_matching_delivery_addresses_id) - 1):
                index += 1
        if(user_request == 3):

            id = list_of_matching_delivery_city_id[index]
            if (index < len(list_of_matching_delivery_city_id) - 1):
                index += 1
        if (user_request == 4):

            id = list_of_matching_delivery_zip_code_id[index]
            if (index < len(list_of_matching_delivery_zip_code_id) - 1):
                index += 1
        if (user_request == 5):

            id = list_of_matching_weight_id[index]
            if (index < len(list_of_matching_weight_id) - 1):
                index += 1
        if (user_request == 6):

            id = list_of_matching_delivery_deadline_id[index]
            if (index < len(list_of_matching_delivery_deadline_id) - 1):
                index += 1
        if (user_request == 7):

            id = list_of_matching_delivery_status_code_id[index]
            if (index < len(list_of_matching_delivery_status_code_id) - 1):
                index += 1
        if(package_hash_table.search(id) != False):
            print("Package ID: " + str(package_hash_table.search(id)[1].id))
            print("Delivery Address: " + str(package_hash_table.search(id)[1].delivery_address))
            print("Delivery City: " + str(package_hash_table.search(id)[1].delivery_city))
            print("Delivery Zip Code: " + str(package_hash_table.search(id)[1].delivery_zipcode))
            print("Delivery Deadline: " + str(package_hash_table.search(id)[1].delivery_deadline))
            print("Package Weight: " + str(package_hash_table.search(id)[1].package_weight))
            print("Delivery Status: " + str(package_hash_table.search(id)[1].delivery_status))
            print("Delivered on: " + str(package_hash_table.search(id)[1].delivery_time))
            print("Delivered by: " + str(package_hash_table.search(id)[1].delivery_truck))
        else:
            print("No item with ID: " + str(id) + " found.")
        print_package_info_how_many_times -= 1

def look_up_address(delivery_address): #I want to find the corresponding vertex with the given delivery address
    for i in range(0, len(list_of_verticies)):
        string_to_compare = list_of_verticies[i].label
        if(longest_substr(string_to_compare, delivery_address) == True):
            return list_of_verticies[i]
def convert_list_of_verticies_into_dictionary(location_dictionary): #I want to place all verticies (locations) into a dictionary where the corresponding package delivery address will be the key, and vertex be the value.
    for i in range(0, len(list_of_verticies)):
        string_to_compare = list_of_verticies[i].label
        for x in range(0, len(list_of_packages)):
            delivery_address_to_compare = list_of_packages[x].delivery_address
            if(longest_substr(string_to_compare, delivery_address_to_compare) == True):
                location_dictionary[delivery_address_to_compare] = list_of_verticies[i]
    return location_dictionary
def look_up_delivery_time(delivery_time): #A function to check if a package has been delivered successfully at a given time. If true, return true.
    package_found = False
    for x in range(0, len(list_of_packages)):
        if(package_hash_table.search(list_of_packages[x].id)[1].delivery_time == delivery_time and package_hash_table.search(list_of_packages[x].id)[1].delivery_truck.truck_id != 1 ): #since there are no previous iterations from truck1, we dont want to check delivery package status from truck 1
            package_found = True
            #package_with_matching_delivery_time = package_hash_table.search(list_of_packages[x].id)[1]
            #print(str(package_with_matching_delivery_time) + " was delivered at " + str(package_hash_table.search(list_of_packages[x].id)[1].delivery_time) + " by " + str(package_hash_table.search(list_of_packages[x].id)[1].delivery_truck) + " driven by " + str(package_hash_table.search(list_of_packages[x].id)[1].delivered_by))
            #return package_with_matching_delivery_time
            return package_found
    return package_found
    #if(package_found == False):
        #print("No packages were delivered at " + str(delivery_time))
def find_next_delivery_time(hour, minute): ##returns the time of when the next package was delivered after the given time
    current_time = datetime(year=2022, month=8, day=17, hour=hour, minute=minute, second=0)
    while (look_up_delivery_time(current_time) == False): #since the number of minutes in a day is not variable, then this section is not O(n), but actually constant O(1)
        current_time = current_time + timedelta(minutes=1)
        if(current_time > datetime(year=2022, month=8, day=17, hour=14, minute=0, second=0)): # after 2pm, all packages should have been delivered by now. Stop the search.
            return None
    return current_time

def find_previous_delivery_time(hour,minute): #returns the time of when the previous package was delivered before the given time
    current_time = datetime(year=2022, month=8, day=17, hour=hour, minute=minute, second=0)
    while(look_up_delivery_time(current_time) == False):
        current_time = current_time - timedelta(minutes=1)
        if (current_time < datetime(year=2022, month=8, day=17, hour=8, minute=0, second=0)):  #Before 8am, all packages are still at the hub. Stop the search.
            return None
    return current_time

def package_status_at_time(hour, minute): #look up the package status of all packages at a given hour and minute of the day
    current_time = datetime(year=2022, month=8, day=17, hour=hour, minute=minute, second=0)
    package_9_update_time = datetime(year=2022, month=8, day=17, hour=10, minute=20, second=0)
    next_delivery_time = find_next_delivery_time(hour, minute)
    previous_delivery_time = find_previous_delivery_time(hour, minute)
    print("Delivery status of all packages at: " + str(current_time))
    #####EDGE CASES####
    # if no previous delivery_time was found and current_time entered is greater than 8am, then user entered a time before any packages were delivered but after 8am, so the status is the same as the 8:01am status
    if(previous_delivery_time == None and current_time > datetime(year=2022, month=8, day=17, hour=8, minute=0)):
        for key, value in delivery_status2[str(datetime(year=2022, month=8, day=17, hour=8, minute=1))].items():
            if (key.id == 9):
                print(key, ' : ', value + " | Delivery Deadline: " + str(key.delivery_deadline) + " | Deliver to: " + "300 State St" + ", " + str(key.delivery_city) + ", " + "84103" + " | Weight: " + str(key.package_weight))
            elif (value == "Delivered"):
                print(key, ' : ', value + " at " + str(key.delivery_time) + " | Delivery Deadline: " + str(key.delivery_deadline) + " | Delivered to: " + str(key.delivery_address) + ", " + str(key.delivery_city) + ", " + str(key.delivery_zipcode) + " | Weight: " + str(key.package_weight))
            else:
                print(key, ' : ', value + " | Delivery Deadline: " + str(key.delivery_deadline) + " | Deliver to: " + str(key.delivery_address) + ", " + str(key.delivery_city) + ", " + str(key.delivery_zipcode) + " | Weight: " + str(key.package_weight))
        #print(delivery_status[str(datetime(year=2022, month=8, day=17, hour=8, minute=0, second=0))])
    elif(previous_delivery_time == None):
        # if no previous delivery_time was found, then user entered a time before any packages were delivered before 8am so the status is the same as the 8:00am status
        for key, value in delivery_status2[str(datetime(year=2022, month=8, day=17, hour=8, minute=0))].items():
            if (key.id == 9):
                print(key, ' : ', value + " | Delivery Deadline: " + str(key.delivery_deadline) + " | Deliver to: " + "300 State St" + ", " + str(key.delivery_city) + ", " + "84103" + " | Weight: " + str(key.package_weight))
            elif (value == "Delivered"):
                print(key, ' : ', value + " at " + str(key.delivery_time) + " | Delivery Deadline: " + str(key.delivery_deadline) + " | Delivered to: " + str(key.delivery_address) + ", " + str(key.delivery_city) + ", " + str(key.delivery_zipcode) + " | Weight: " + str(key.package_weight))
            else:
                print(key, ' : ', value + " | Delivery Deadline: " + str(key.delivery_deadline) + " | Deliver to: " + str(key.delivery_address) + ", " + str(key.delivery_city) + ", " + str(key.delivery_zipcode) + " | Weight: " + str(key.package_weight))
    elif(next_delivery_time == None): #if no next delivery_time was found, then user entered a time after all packages were delivered, so the status is the same as the last package delivered status, which is the previous_delivery time from the current time
        for key, value in delivery_status2[str(previous_delivery_time)].items():
            if (value == "Delivered"):
                print(key, ' : ', value + " at " + str(key.delivery_time) + " | Delivery Deadline: " + str(key.delivery_deadline) + " | Delivered to: " + str(key.delivery_address) + ", " + str(key.delivery_city) + ", " + str(key.delivery_zipcode) + " | Weight: " + str(key.package_weight))
            else:
                print(key, ' : ',value + " | Delivery Deadline: " + str(key.delivery_deadline) + " | Deliver to: " + str(key.delivery_address) + ", " + str(key.delivery_city) + ", " + str(key.delivery_zipcode) + " | Weight: " + str(key.package_weight))
        #print(delivery_status[str(previous_delivery_time)])

    else:#(current_time < next_delivery_time): #all else cases fall in the category where the current time is less than next_delivery_time, so print the previous delivery time status
        for key, value in delivery_status2[str(previous_delivery_time)].items():
            #verifying package 9 shows the correct information at the current time
            if(current_time < package_9_update_time):
                if (key.id == 9):
                    print(key, ' : ', value + " | Delivery Deadline: " + str(
                        key.delivery_deadline) + " | Deliver to: " + "300 State St" + ", " + str(
                        key.delivery_city) + ", " + "84103" + " | Weight: " + str(key.package_weight))
                elif (value == "Delivered"):
                    print(key, ' : ', value + " at " + str(key.delivery_time) + " | Delivery Deadline: " + str(
                        key.delivery_deadline) + " | Delivered to: " + str(key.delivery_address) + ", " + str(
                        key.delivery_city) + ", " + str(key.delivery_zipcode) + " | Weight: " + str(key.package_weight))
                else:
                    print(key, ' : ', value + " | Delivery Deadline: " + str(key.delivery_deadline) + " | Deliver to: " + str(
                          key.delivery_address) + ", " + str(key.delivery_city) + ", " + str(
                          key.delivery_zipcode) + " | Weight: " + str(key.package_weight))
            else:
                if (value == "Delivered"):
                    print(key, ' : ', value + " at " + str(key.delivery_time) + " | Delivery Deadline: " + str(
                        key.delivery_deadline) + " | Delivered to: " + str(key.delivery_address) + ", " + str(
                        key.delivery_city) + ", " + str(key.delivery_zipcode) + " | Weight: " + str(key.package_weight))
                else:
                    print(key, ' : ', value + " | Delivery Deadline: " + str(key.delivery_deadline) + " | Deliver to: " + str(
                          key.delivery_address) + ", " + str(key.delivery_city) + ", " + str(
                          key.delivery_zipcode) + " | Weight: " + str(key.package_weight))
        #print(delivery_status[str(previous_delivery_time)])

def calculate_time_elapsed(next_edge_weight, truck_speed, current_time): #calculate the time elapsed from travelling the next_edge_weight
    time_elapsed = int((60.0 * float(next_edge_weight / truck_speed)))
    return current_time + timedelta(minutes=time_elapsed)

def load_package_into_queue(truck, queue_of_unvisited_verticies):
    for each_package in truck.container_of_packages:
        if (each_package.found_vertex_address == False):
            #the location_dictionary returns the corresponding vertex with the associated delivery address. This is because delivery address, and vertex address don't completely match
            matching_vertex_address = location_dictionary[each_package.delivery_address]
            queue_of_unvisited_verticies.append(matching_vertex_address)
            each_package.vertex_id = matching_vertex_address.vertex_id #update each_package vertex id to the corresponding vertex.vertex_id to be able to later remove the package from truck when successfully "delivered" to the correct vertex location
            package_hash_table.search(each_package.id)[1].update_delivery_status("On Route")
            each_package.found_vertex_address = True #updating package info to where the corresponding vertex to the delivery address has been found
    return queue_of_unvisited_verticies

def find_shortest_path(graph, current_vertex, queue_of_unvisited_verticies, smallest_edge):
    for i in range(0, len(queue_of_unvisited_verticies)):  # go through the list of unvisited_verticies and find the package containing the delivery address with the smallest weight to the current_vertex
        if (current_vertex != queue_of_unvisited_verticies[i]):  ##if the current_vertex is already at the location, then no need get get_edge_weight
            next_edge_weight = float(graph.edge_weight[current_vertex, queue_of_unvisited_verticies[i]])
            if(next_edge_weight < smallest_edge):
                smallest_edge = next_edge_weight
                index_of_smallest_edge = i
    return current_vertex, queue_of_unvisited_verticies, index_of_smallest_edge

def longest_substr(str1, str2):
# since delivery_address of a package is different than the vertex address, then I need to verify which vertex contains
 # the delivery address by comparing the longest substring. If there is a match, then return true. The algorithm is from zybooks

    match_count = 0 #keeps track of how many matching letters there are to determine good enough to be true
    # Create one row of the matrix.
    matrix_row = [0] * len(str2)

    # Variables to remember the largest value, and the row it
    # occurred at.
    max_value = 0
    max_value_row = 0
    for row in range(len(str1)):
        # Variable to hold the upper-left value from the
        # current matrix position.
        up_left = 0
        for col in range(len(str2)):
            # Save the current cell's value; this will be up_left
            # for the next iteration.
            saved_current = matrix_row[col]

            # Check if the characters match
            if str1[row] == str2[col]:
                matrix_row[col] = 1 + up_left

                # Update the saved maximum value and row,
                # if appropriate.
                if matrix_row[col] > max_value:
                    max_value = matrix_row[col]
                    max_value_row = row
            else:
                matrix_row[col] = 0

            # Update the up_left variable
            up_left = saved_current

    # The longest common substring is the substring
    # in str1 from index max_value_row - max_value + 1,
    # up to and including max_value_row.
    start_index = max_value_row - max_value + 1
    matching_string = str1[start_index : max_value_row + 1]
    match_count = len(matching_string)
    if(str2 == matching_string or match_count > 24): ##if there are at least 24 consecutive matching characters in the string. Good enough to be considered a match
        return True
    return False
def nearest_neighbor(graph, truck, start_vertex, current_time):
    initial_package_status_after_8am = {} # I need to capture the package status of all packages at 8:01am initially to capture the package status between after the trucks leave, and before the initial first delivery
    current_vertex = start_vertex
    queue_of_unvisited_verticies = []
    list_of_truck_packages = [] #temporary list that gets overwrriten on each function call. will be used to keep track of which packages were on the truck, even when packages have been removed from truck
    for i in range(0, len(truck.container_of_packages)):
        list_of_truck_packages.append([])
    for i in range(0, len(truck.container_of_packages)):
        list_of_truck_packages[i] = truck.container_of_packages[i]
    smallest_edge = 1000  # will keep track of the smallest edge_weight between current_vertex and remainder of verticies in the truck. Intialized to 1000, since no two connected locations are greater than 1000
    distance = 0
    index_of_smallest_edge = 0 #will keep track of the index of the vertex that contains the smallest edge
    time_elapsed = 0 #will keep track of how much time passed given the distance travelled and Truck avg_speed in mph
    #print("Starting delivery process with truck " + str(truck.truck_id))
    print("truck" + str(truck.truck_id) + " left the hub at " + str(truck.departure_time) + " with driver: " + str(truck.driver))

    #####################CHECKING FOR SPECIAL CONDITION REQUIREMENTS FOR PROJECT################################
    # the delivery people know that package 9 delivery address is incorrect. They will receive the correct delivery address at 10:20am
    if (truck.truck_id == len(list_of_trucks)): #checks to see if truck is truck3 since package 9 is only loaded onto truck3.
        wrong_address_list = [] #package 9 will still be loaded onto the truck, but is set aside from the normal list of packages
        index_of_package_9 = truck.container_of_packages.index(package_hash_table.search(9)[1])
        wrong_address_list.append(truck.container_of_packages.pop(index_of_package_9))
        package_hash_table.search(9)[1].delivery_status = "On Route"

    #############LOADING UNDELIVERED PACKAGES INTO QUEUE##################
    queue_of_unvisited_verticies = load_package_into_queue(truck, queue_of_unvisited_verticies)


    ##################BEGIN DELIVERING PACKAGE ROUTE######################
    if(truck.contains_driver()): ##Will only go on route if there is a driver present in the truck
        while (len(truck.container_of_packages) != 0):

            #####################CHECKING FOR SPECIAL CONDITION REQUIREMENTS FOR PROJECT################################
            # checking to see if the current time is greater than 9:05AM. If so, then truck2 goes back to hub to load new packages that arrived at 9:05am
            special_condition_time_for_late_arrival_packages = datetime(year=2022, month=8, day=17, hour=9, minute=5, second=0)
            if (current_time >= special_condition_time_for_late_arrival_packages and truck.truck_id == 2 and len(special_case_late_packages) != 0):
                if(current_vertex != hub_vertex):
                    print("Currently it is " + str(current_time) + ". New packages arrived at hub at " + str(special_condition_time_for_late_arrival_packages) + ". Truck" + str(truck.truck_id) + " rerouting from (" + str(current_vertex) + ") to (" + str(hub_vertex) + ") to pick up more packages.")

                    next_edge_weight = float(graph.edge_weight[current_vertex, hub_vertex])
                    #print("This is a distance of " + str(next_edge_weight)) #debugging
                    distance += next_edge_weight  # successfully drove to next vertex, adding distance travelled to calculated total distance
                    current_vertex = hub_vertex

                #########CALCULATING TIME ELAPSED FOR TRAVELING THE EDGE_WEIGHT################################
                current_time = calculate_time_elapsed(next_edge_weight, truck.avg_speed, current_time)

                #arrived at hub, loading late packages into truck
                while(len(special_case_late_packages) != 0):
                    #print("successfully loaded " + str(special_case_late_packages[len(special_case_late_packages)-1]) + " onto truck" + str(truck.truck_id)) #debugging
                    truck.load(special_case_late_packages.pop()) #loading the truck with late packages, and popping from the list to iterate through while-loop
                #print("truck " + str(truck.truck_id) + "list of packages: " + str(truck.container_of_packages))

                #################LOADING UNDELIVERED PACKAGES FROM THE 9:O5AM LATE PACKAGE LIST INTO QUEUE#################
                #Append verticies from the packages that have not been loaded into queue of unvisited verticies
                queue_of_unvisited_verticies = load_package_into_queue(truck, queue_of_unvisited_verticies)


                #############################FIND SHORTEST PATH FROM HUB VERTEX##################
                current_vertex, queue_of_unvisited_verticies, index_of_smallest_edge = find_shortest_path(graph, current_vertex, queue_of_unvisited_verticies, smallest_edge)


            else: #continue to find shortest path if late packages have not arrived yet

                #####################CHECKING FOR SPECIAL CONDITION REQUIREMENTS FOR PROJECT################################
                # the delivery people know that package 9 delivery address is incorrect. They will receive the correct delivery address at 10:20am
                special_condition_time_for_package9 = datetime(year=2022, month=8, day=17, hour=10, minute=20, second=0)

                if (current_time >= special_condition_time_for_package9 and truck.truck_id == len(list_of_trucks) and package_hash_table.search(9)[1].address_updated == False): #check for the condition for package 9 on last truck since package 9 will only be loaded onto the last truck
                    package_hash_table.search(9)[1].delivery_address = "410 S State St"
                    package_hash_table.search(9)[1].delivery_zipcode = "84111"
                    package_hash_table.search(9)[1].address_updated = True #using boolean value to verify address has been updated.
                    print(str( package_hash_table.search(9)[1]) + " is sitting in Truck" + str(truck.truck_id))
                    print("its after 10:20am so " + str( package_hash_table.search(9)[1]) + " delivery address is updated to " + str(package_hash_table.search(9)[1].delivery_address) + " and added onto normal package list")
                    truck.load(wrong_address_list.pop()) #moving package 9 into normal package list

                    ###########LOADING NEW PACKAGES INTO UNVISITED VERTICIES###############################
                    queue_of_unvisited_verticies = load_package_into_queue(truck, queue_of_unvisited_verticies)


                #############################FIND SHORTEST PATH FROM CURRENT VERTEX##################
                current_vertex, queue_of_unvisited_verticies, index_of_smallest_edge = find_shortest_path(graph, current_vertex, queue_of_unvisited_verticies,smallest_edge)


            ###############################VISIT NEXT VERTEX######################################
            if (current_vertex != queue_of_unvisited_verticies[index_of_smallest_edge]):  ##if the current_vertex is already at the location, then no need to add distance
                next_edge_weight = float(graph.edge_weight[current_vertex, queue_of_unvisited_verticies[index_of_smallest_edge]])
                distance += next_edge_weight   #successfully drove to next vertex, adding distance travelled to calculated total distance and "package successfully delivered"
                current_vertex = queue_of_unvisited_verticies[index_of_smallest_edge] #updating current location to the visited vertex
                #print("current_vertex is now " + str(current_vertex)) #debugging

                #########CALCULATING TIME ELAPSED FOR TRAVELING THE EDGE_WEIGHT################################
                current_time = calculate_time_elapsed(next_edge_weight, truck.avg_speed, current_time)

                ##########################UPDATING PACKAGE STATUS#####################################
                # looking at the package that was just delivered and comparing it to the vertex of the current location
                # the look_up_address function returns the corresponding vertex with the associated delivery address
                #print(str(current_time))
                for x in range(0, len(truck.container_of_packages)):
                    #print("current index in container of packages is: " + str(x) + " which is " + str(truck.container_of_packages[x])) #debugging
                    if(current_vertex == location_dictionary[truck.container_of_packages[x].delivery_address]):
                    #if (current_vertex == look_up_address(truck.container_of_packages[x].delivery_address)):
                        #print("current vertex found a matching delivery address at: " + str(look_up_address(truck.container_of_packages[x].delivery_address)))
                        #print(truck.container_of_packages[x]) #debugging
                        #print("has been delivered at: " + str(current_time)) #debugging
                        package_hash_table.search(truck.container_of_packages[x].id)[1].update_delivery_time(current_time) #updating package delivery time with when it was delivered
                        #print(str(current_vertex) + " is the same location as " + str(truck.container_of_packages[x].delivery_address)) #debugging
                        #print(str(package_hash_table.search(truck.container_of_packages[x].id)[1]) + " delivery status was " + package_hash_table.search(truck.container_of_packages[x].id)[1].delivery_status + " but is now...") #debugging
                        package_hash_table.search(truck.container_of_packages[x].id)[1].update_delivery_status("Delivered")  # updating package delivery_status in hashtable database
                        package_hash_table.search(truck.container_of_packages[x].id)[1].delivery_truck = truck              #updating which truck delivered the package
                        package_hash_table.search(truck.container_of_packages[x].id)[1].delivered_by = truck.driver         #updating which driver delivered the package



                ##################REMOVING VERTEX FROM UNVISITED LIST AND REMOVING PACKAGE FROM TRUCK#################################
                for each_package in truck.container_of_packages: #removing corresponding package from truck
                    #print(str(each_package) + "vertex id is: " + str(each_package.vertex_id) + " and matching vertex with with vertex id is: " + str(queue_of_unvisited_verticies[index_of_smallest_edge].vertex_id)) #debugging
                    #print(str(truck.container_of_packages)) #debugging
                    if (each_package.vertex_id == queue_of_unvisited_verticies[index_of_smallest_edge].vertex_id):
                        #print(str(each_package) + " will be removed from truck now")
                        truck.container_of_packages.remove(each_package)
                    # for some reason I need to enter the for loop again to check for all previous entries if any previous entries of container_of_packages have a matching vertex_id. I am not sure, but it might have to do
                    # with removing each package for each interval, and for-loops in python when using each_package doesn't necessarily count each package, but the specific index. Since I remove the package in the interval, then the index of the packages afterwards change,
                    # and I need to iterate over the container of packages again to verify for any changes made to the indicies of each_package
                    for each_package in truck.container_of_packages:
                        if(each_package.vertex_id == queue_of_unvisited_verticies[index_of_smallest_edge].vertex_id):
                            #print(str(each_package) + " will be removed from truck now")
                            truck.container_of_packages.remove(each_package)
                queue_of_unvisited_verticies.pop(index_of_smallest_edge)  # removing visited vertex from queue of unvisited verticies
                smallest_edge = 1000  # smallest edge of the current loop has been found and traversed, resetting smallest edge for the next loop


        ##############FINAL TOUCHES################
        distance += float(graph.edge_weight[current_vertex, list_of_verticies[0]]) ##make sure to drive back to hub
        current_time = calculate_time_elapsed(float(graph.edge_weight[current_vertex, list_of_verticies[0]]), truck.avg_speed, current_time) #updating current time
        truck.return_time = current_time  # updating truck return time
        truck.driver.return_time = current_time  # updating driver return time to be used for next truck without a driver departure time
        list_of_available_drivers.append(truck.driver) #driver arrived back to the hub safely, placing truck driver into available list of drivers
        truck.driver = None #removing driver from current truck
        return distance, current_time
    return 0, current_time

def open_distance_data(file_name):
    location_list = [] #location list to keep all locations
    weight_list = []    #edge_weight of location to location, listed in ..??
    location_count = 0 #keeps track of how many locations in the file


    ##need to open the file twice? Once for filling the location_list, and once again for filling the edge_weight list.
    #otherwise, if its only opened once, the contents of the file is emptied after i fill in the first list? thats strange
    with open(file_name) as distance_table_file:
        distance_data = csv.reader(distance_table_file, delimiter=',')
        for i in range(0, 8):  # skipping formatting in the distance data file
            next(distance_data)
        for location in distance_data:  #filling location list with all locations
            location_list.append(location[0])
            location_count += 1         #keeping track of how many physical address locations in file
    with open(file_name) as distance_table_file:
        distance_data = csv.reader(distance_table_file, delimiter=',')

        for i in range(0, 8):  # skipping formatting in the distance data file
            next(distance_data)
        for i in range(0, location_count): #adding the address locations as verticies in the adjacency_matrix
            vertex = location_list[i]
            temp_vertex = Vertex(vertex)
            adjacency_matrix.add_vertex((temp_vertex))
            list_of_verticies.append(temp_vertex) #appending temp_vertex into list_of_verticies to refer to when adding edge weights
            temp_vertex.vertex_id = i
        for location in distance_data:
            # distance_data csv file is formatted where after the location, is the "distance between".
            # Numbers following "distance between" represent the weight from the start of location_list[0] to
            # the end of location_list, but if it reads in an empty string, then there is no weight in that direction
            #if the weight is 0, then that is the distance between the location and itself so it is not needed.
            #start the for loop at index 2 because of formatting of the file. The first two indicies contain locations. Don't need locations inside the weight_list
            for i in range(2, location_count + 1): #go through the range of location_count+1 because of the need to count the current location twice in the adjacency_matrix
                if(location[i] != "" and location[i] != '0.0'):
                    weight_list.append(location[i])
        #to add the edge weights to the verticies, It was easier in my mind to count backwards from the end of the csv file. I used a double for-loop to traverse the
        #2d matrix (the csv file). From the end of the list (j), I iterated backwards  and for each (j), I needed to traverse the list again up to (j) where (j) is the
        #location we are currently. In this second iteration (k), I used the list_of_verticies to obtain the temp_verticies I had stored earlier from adding the verticies to the adjacency matrix,
        #and used weight_list where I stored each edge_weight from every location. In order to obtain the correct edge weight in the synchronous order as the list of verticies, I used the formulas
        #as seen in the code (with a lot of trial and error). After whiteboarding, the logic makes sense.
        for j in range(location_count - 1, 0, -1):  #J starts at the end of the 2d matrix and iterates backwards
            for k in range(1, j+1):                 #K starts at 1 since it is unnecessary to start at 0, where 0 would be the same location as current J, and K iterates up to J+1 since j+1 in the for loop is exclusive, and
                                                    #i need K to include the value of J. J is used as an index for list__of_verticies that contain all verticies in the same order as the 2d matrix
                # to obtain the corresponding weight in weight_list, it is the amount of locations * locations-1, divided by 2. Then I iterated backwards by k. In order to stay within range of the list, adjustments were made.
                adjacency_matrix.add_undirected_edge(list_of_verticies[j], list_of_verticies[j-k], weight_list[int((((j+1)*(j))/2)- k)])
                #print(weight_list[int((((j+1)*(j))/2)- k)]) #debugging
                #print(location_list[(j+1)-(k+1)])           #debugging

def open_package_data(file_name):
    load_truck = 0   #used to keep track if a truck has been filled, then iterate load_truck to get the next truck in the list_of_trucks
    with open(file_name) as package_data_file:
        package_data = csv.reader(package_data_file, delimiter=',')
        for i in range(0, 8):  #skipping formatting in package data file
            next(package_data)
        for package in package_data:            #labeling all required labels for package from the package_data
            package_id = int(package[0])
            delivery_address = package[1]
            delivery_city = package[2]
            delivery_zipcode = package[4]
            delivery_deadline = package[5]
            delivery_weight = package[6]
            status_of_delivery = "At Hub"


            ###########PLACING PACKAGE INFORMATION INTO HASHTABLE########
            new_package = Package(package_id, delivery_address, delivery_city, delivery_zipcode, delivery_deadline, delivery_weight, status_of_delivery) #creating new_package with required details
            package_hash_table.insert(new_package.id, new_package)      #inserting new_package with new_package.id being the key to hash, and new_package object being the item associated with that key
            list_of_packages.append(new_package)   #inserting package into a list to keep track of packages that come into the hub

        ###############LOADING TRUCKS WITH PACKAGES#############################
            if (new_package.id == 6 or new_package.id == 25 or new_package.id == 28 or new_package.id == 32):  # these packages arrive late at 9:05am. Cannot load these packages at hub until after 9:05am
                #print("successfully added " + str(new_package) + " to late packages list") #debugging
                special_case_late_packages.append(new_package)

            elif (new_package.id == 9):  # special case package where the delivery address is incorrect. The correct address won't be known until 10:20am. Load this item into the last truck.
                special_case_packages.append(new_package)

            elif (new_package.id == 3 or new_package.id == 18 or new_package.id == 36 or new_package.id == 38): #special case packages where they must be on truck 2
                packages_must_be_in_truck2.append(new_package)

            elif (new_package.id == 13 or new_package.id == 14 or new_package.id == 15 or new_package.id == 16 or new_package.id == 19 or new_package.id == 20): #special case packages where they must be delivered together (on the same truck)
                packages_must_be_delivered_together.append(new_package)

            elif(new_package.delivery_deadline != "EOD"): ##Making sure to load the first truck with packages that have a delivery deadline first
                list_of_trucks[load_truck].load(new_package)
                #print("load truck is: " + str(load_truck)) #debugging
                #print("truck " + str(load_truck) + " has " + str(len(list_of_trucks[load_truck].container_of_packages)) + " packages in it.") #debugging

            else:                                    #else if the package does contain a delivery deadline with "EOD", then place package into a package queue intil all packages with delivery deadlines have been loaded
                package_queue.append(new_package)    #if all trucks have been loaded with delivery deadline packages, then place package into package_queue to keep track of which packages still need to be loaded
                #print(package_queue) #debugging
        package_queue.reverse() #reverse the list so that popping pops the first package that was inserted instead of the last item
        for i in range(0, len(package_queue)):
            if (list_of_trucks[load_truck].is_not_full()):  # if the truck is not full after loading all packages with a delivery deadline, continue loading with packages from the package queue
                list_of_trucks[load_truck].load(package_queue.pop())
                #print("load truck is: " + str(load_truck))  # debugging
                #print("truck " + str(load_truck) + " has " + str(len(list_of_trucks[load_truck].container_of_packages)) + " packages in it.")  # debugging
                #print(package_queue)  #debugging
                if (load_truck == len(list_of_trucks)-1): #loading special case packages where the delivery address will be updated at 10:20am only in the final truck
                    for q in (range(0, len(special_case_packages))):
                        list_of_trucks[load_truck].load(special_case_packages.pop())
                elif(list_of_trucks[load_truck].truck_id == 2): #loading special case packages where these packages must be loaded onto truck2
                    while(len(packages_must_be_in_truck2) != 0):
                        list_of_trucks[load_truck].load(packages_must_be_in_truck2.pop())
                elif(list_of_trucks[load_truck].truck_id == 1): #since most of the packages that must be delivered together have a delivery deadline, I want them to be on the first truck to be delivered asap.
                    while(len(packages_must_be_delivered_together) != 0):
                        list_of_trucks[load_truck].load(packages_must_be_delivered_together.pop())

                if (list_of_trucks[load_truck].is_full()):  # continue loading packages into trucks until max capacity has been reached
                    if (load_truck < len(list_of_trucks) - 1):  # continue loading trucks until the end of the list_of_trucks have been reached
                        load_truck += 1

    ##############INITIALIZING PACKAGE STATUS AT REQUIRED 8AM TIME####################
    default_package_status = {}
    default_time = datetime(year=2022, month=8, day=17, hour=8, minute=0, second=0)
    for k in range(0, len(list_of_packages)):
        default_package_status[package_hash_table.search(list_of_packages[k].id)[1]] = package_hash_table.search(list_of_packages[k].id)[1].delivery_status
        # print("package status of " + str(package_hash_table.search(list_of_packages[j].id)[1]) + ": " + str(package_hash_table.search(list_of_packages[j].id)[1].package_status))
    delivery_status2.update({str(default_time) : default_package_status})


#######################################MAIN##############################################################
#########################################################################################################


##########OPENING PACKAGE AND DISTANCE FILES############################################
open_distance_data("Distance Table.csv")
open_package_data("Package File.csv")


##########################LOADING LOCATION DICTIONARY###################
convert_list_of_verticies_into_dictionary(location_dictionary)


###############DELIVERING PACKAGES##############################################################
hub_vertex = list_of_verticies[0] #the first vertex in list_of_verticies is the hub.

print("Running simulation...Press Enter to continue")
user_continue = input()

distance_travelled1, return_time1 = nearest_neighbor(adjacency_matrix, Truck1, hub_vertex, Truck1.departure_time)
distance_travelled2, return_time2 = nearest_neighbor(adjacency_matrix, Truck2, hub_vertex, Truck2.departure_time)

print("Currently delivering packages...Press Enter to continue...")
user_continue = input()

print("Truck1 returned to the hub at " + str(return_time1))
print("Press Enter to continue...")
user_continue = input()
if(Driver1.return_time < Driver2.return_time):
    Truck3.driver = Driver1
else:
    Truck3.driver = Driver2
Truck3.departure_time = Truck3.driver.return_time
distance_travelled3, return_time3 = nearest_neighbor(adjacency_matrix, Truck3, hub_vertex, Truck3.departure_time)
print("Press Enter to continue...")
user_continue = input()

print("Truck3 returned to the hub at " + str(return_time3))
print("Truck2 returned to the hub at " + str(return_time2))
print("Press Enter to continue...")
user_continue = input()

distance_list = [str(round(distance_travelled1, 2)), str(round(distance_travelled2, 2)), str(round(distance_travelled3, 2))]
distance_travelled = distance_travelled1 + distance_travelled2 + distance_travelled3

################################CAPTURING PACKAGE STATUS OF ALL TIMES######################
capture_all_package_status()
##########################################################################################



#####################INTERFACE########################
print("All packages have been delivered.")
print("All trucks arrived back at hub and travelled a total of " + str(distance_travelled) + " miles.")
print("-------------------------------------------------------------------------------")
for i in range(0, len(list_of_trucks)):
    print("Departure time for truck" + str(list_of_trucks[i].truck_id) + " is: " + str(list_of_trucks[i].departure_time))
    print("Return time for truck" + str(list_of_trucks[i].truck_id) + " is: " + str(list_of_trucks[i].return_time))
    print("Truck" + str(list_of_trucks[i].truck_id) + " distance travelled was " + str(distance_list[i]))
    print("---------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------")

user_input_checking_what = None
#user_input_method_to_find_package = None
user_look_up_package = None
user_input_hour = None
user_input_minute = None
user_check_anything_else = '1'

while(user_check_anything_else == '1'):
    print("What would you like to check?")
    print("1.) Look up a package")
    print("2.) Look up the delivery status of all packages at a specific time")

    while (user_input_checking_what not in ['1', '2']):
        user_input_checking_what = input()
        #user_input_checking_what = int(user_input_checking_what)
        if(user_input_checking_what not in ['1', '2']):
            print("Invalid input. Please select a valid input.")
    if(user_input_checking_what == '1'):
        print("Which method would you like to use to find your package?")
        print("1.) By ID")
        print("2.) By Delivery Address")
        print("3.) By Delivery City")
        print("4.) By Delivery Zipcode")
        print("5.) By Package Weight")
        print("6.) By Delivery Deadline")
        print("7.) By Delivery Status")
        user_request = int(input())
        if(user_request == 1):
            print("Which package info with ID were you looking for?")
            user_look_up_package = int(input())
            #look_up_package(user_request)
        if(user_request == 2):
            print("Which delivery address are you referring to?")
            user_look_up_package = input()
        if(user_request == 3):
            print("Which delivery city are you referring to?")
            user_look_up_package = input()
        if (user_request == 4):
            print("Which delivery zipcode are you referring to?")
            user_look_up_package = input()
        if (user_request == 5):
            print("How much did the package weigh? (Just enter a number i.e(1))")
            user_look_up_package = input()
        if (user_request == 6):
            print("What was the delivery deadline of the package?")
            user_look_up_package = input()
        if (user_request == 7):
            print("Which delivery status are you referring to? ('At Hub', 'On Route', 'Delivered')")
            print("All packages have been successfully delivered. Enter 'Delivered' to see all packages")
            print("All other entries will return no results")
            print("If you are searching for the delivery status of all packages at a given time, return to main menu and select option (2)")
            user_look_up_package = input()
        look_up_package(user_look_up_package)
    if(user_input_checking_what == '2'):
        while(user_input_hour not in range(0,24)):
            print("Please enter the hour you wish to see in military time. Do not enter any leading zeros i.e( 8 - instead of 08)")
            user_input_hour = int(input())
        while(user_input_minute not in range(0, 60)):
            print("Please enter the minute you wish to see. Do not enter any leading zeros i.e( 1 - instead of 01)")
            user_input_minute = int(input())
        package_status_at_time(user_input_hour, user_input_minute)

    print("Would you like to check anything else?")
    print("1.) Yes")
    print("2.) No")
    user_check_anything_else = input()
    if(user_check_anything_else == '1'):
        clear = "\n" * 100
        print(clear)
        user_input_checking_what = None
        user_look_up_package = None
        user_input_hour = None
        user_input_minute = None
        user_request = None
    if(user_check_anything_else == '2' or user_check_anything_else != '1'):
        break
        exit()







