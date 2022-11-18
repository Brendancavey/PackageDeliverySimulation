###First Name: Brendan||||Last Name: Thoeung||||Student ID: 007494550

#assisstance from csDojo
import math

class MyHashTable:
    #table_size must be a prime number in order for double-hasing collision checking to work
    table_size = 11
    #table_count keeps track of how many items have been inserted into the table. When table_count exceeds optimal amount for table_size,
    #then table_size needs to be adjusted.
    table_count = 0
    #current_index_of_known_prime_numbers refers to table_resize function, where I keep track of which index
    #known prime numbers list is at
    current_index_of_known_prime_numbers = 0
    def __init__(self): #constructor
        self.list = []
        for x in range(0, self.table_size):
            self.list.append([])
    #by using a double-hashing collision method, searching is O(1) operations in the worst case, vs
    #using a chaining collision method where the worst case can be O(N)
    def search(self, key):
        index = self.my_hash_function(key)
        if(self.list[index] != []): #check to see if item at calculated index is empty. If not, proceed
            if(self.list[index][0] == key): #self.list[index][0] is the id key in the key - item pair
                #print(str(key) + " is found at index: " + str(index))  #debugging test
                # Successfully found key-item pair. Return the index in which it was found.
                # This is so this function can be reused whenever we need to verify an item is in the
                #list and need to use the index of where the item is located
                return index, self.list[index][1]    #the item located at this index can also be returned using subscript [1]
        else:
            return False
            print("Unable to find " + str(key) + " in the hash table")

    #To handle collisions, we use double-hashing where we probe the index + C if there is an item already
    #in place of where the item is supposed to be placed. We continue iterating with + C until a space has been found successfully.
    #C is an integer where the GCD(C,table_size) = 1 in order to guarantee each index in the list will be checked.
    #Since I've made sure to have table_size always be prime, then GCD(C,table_size) will always be 1
    def insert(self, key, item):
        #before each insert, need to check if the hash table has an optimal amount of space. If not, we need to
        #resize the table. In this case, if the number of items in the list > 2/3, then the table size is adjusted
        #this allows for search, insertion, and deletion to be done in O(1)
        if (float(self.table_count/self.table_size) > float(2/3)):
            #print("table_size needs to be adjusted in order to be optimized. Resizing...") #debugging test
            self.table_resize(self.table_size)
            #print("new table_size is " + str(self.table_size)) #debugging test
        index = self.my_hash_function(key)
        while(self.list[index] != []):
            #constant is found by taking the current index that was found using the previous hash function, and modding that index by
            #table_size-1 to stay within range of the list. The result is (table_size - 2), so, We add +1 to get within the range of
            #the table_size list, which is table_size-1 since (table_size-2+1) = (table_size-1)
            constant = self.my_hash_function(key) % (self.table_size - 1) + 1
            #print("constant is " + str(constant)) #debugging test
            index += constant
            #if the calculated index is greater than the size of the list, then we must subtract table_size from the calculated index
            #to have calcuated index loop to the front of the list
            if(index > self.table_size-1):
                index -= self.table_size
            #print("index is at " + str(index)) #debugging test
        #key_item is a short list where the first index 0 will always be the key which is used in hash calculations,
        #and the second index 1 will be the item linked to that specific key. We place this short list in the desired area of the hash table
        #using the index calculated from the hash function on the key
        key_item = [key, item]
        self.list[index] = key_item
        self.table_count += 1

    #use the search function to return the index of the item if found, and replace the item at that index with an empty item
    def delete(self, key):
        index_of_item_to_delete = self.search(key)

        if(index_of_item_to_delete != None):
            print("Deleting item with key: " + str(key))
            self.list[index_of_item_to_delete] = []
            self.table_count -= 1                   #adjusting table count to reflect the deleted key


    #Uses the modulo operator as the hash function in order to insert, search, and delete items into the list.
    #We mod by the table_size in order to have the index be within range of the table size.
    def my_hash_function(self, key):
        index = key % self.table_size
        #print(str(key) + " modulo " + str(self.table_size) + " is " + str(index) ) #debugging test
        return index

    #in order for double-hashing collision to continue working, the table size must be a prime number.
    #I used a list of known prime numbers after the initial table_size, and the table_size will adjust to the next known prime number.
    #The hash table can hold a total of 401 items if need be
    #Having the table be resized does take extra time due to copying and reinserting into the new list, but the advantage is that
    #searching, insertion, and deletion will remain constant O(1) when the table doesn't have to be readjusted
    def table_resize(self, current_table_size):
        known_prime_numbers = [23, 41, 83, 163, 293, 401]
        new_list = []
        next_prime_number = known_prime_numbers[self.current_index_of_known_prime_numbers]
        self.current_index_of_known_prime_numbers += 1

        #print("The next prime number is " + str(next_prime_number) + ", adjusting table...") #debugging test
        self.table_size = next_prime_number

        #making new list with adjusted table size
        for x in range(0, self.table_size):
            new_list.append([])

        # reset table count to the new table
        self.table_count = 0
        #now that table_size has been adjusted, I need to make a copy of the old list, and insert all of the previous
        #items into the new list so that search and delete functions can work with the same hash function that now does work on the new list size
        old_list = self.list
        self.list = new_list
        for x in range(0, len(old_list)):
            if(old_list[x] != []):
                self.insert(old_list[x][0], old_list[x][1] ) #old_list[x][0] is the id, and old_list[x][1] is the item



    def print_list(self):
        print(self.list)

    def print_length(self):
        print(len(self.list))



