import format_random_v2_00 as fm
import csv

# CLASSES ########################################

# PRODUCTS CLASS ########################################

class Couriers:
    couriers_list = [] # list to store all instances of each courier
    couriers_id_cache = []

    # initialisation
    def __init__(self, name:str, phone_number:str, courier_id:int = None): 
        """ Load or create new courier with name, phone numb, & id numb """

        def get_valid_courier_id():
            """ if the id you want to use is in the couriers_id_cache then create a new one """
            current_value = int(max(self.couriers_id_cache)) + 1 # plus one to the largest number in the id cache gives you the most valid number for the id (will not duplicate)
            print(f"MOST VALID ID = {current_value}")
            print(f"ID CACHE {self.couriers_id_cache}")
            self.courier_id = current_value
            self.couriers_id_cache.append(self.courier_id) # append the id to our cache, having cache means no duplicates, no duplicates means search by id number is plausible

        # varaibles, set regardless of load or create
        self.name = name
        self.phone_number = phone_number

        # for differences between loading existing and creating new
        if courier_id: # has items, so you are creating a new object from existing data
            self.name, self.phone_number, self.courier_id = name, phone_number, courier_id
            self.couriers_list.append(self)
            # regardless of loading and the fact that I'm not letting users change ID numbers, should still perform a check here > if id is in id_cache, then change it
            if self.courier_id in self.couriers_id_cache:
                print(f"ID CACHE {self.couriers_id_cache}")
                print(f"THE ID {self.courier_id}")
                print("AVERTING POTENTIAL ID CLASH... UPDATING COURIER ID")
                get_valid_courier_id()
            else:
                self.couriers_id_cache.append(self.courier_id)
            print(f"#{self.courier_id} {self.name} - {self.phone_number} Loaded\n")
        else:
            # you are creating from scratch, so you need a new, dynamically created courier_id
            if self.couriers_id_cache: # has items
                get_valid_courier_id()
            else:
                # if the cache has no items then its the first ite, so if its a brand new courier their number will be one (ooooo lucky you huh)
                self.courier_id = 1
                self.couriers_id_cache.append(self.courier_id)
            # append it to the "global" list and print back confirmation
            self.couriers_list.append(self)
            print(f"#{self.courier_id} - {self.name} - {self.phone_number} Created\n")   
        #END IF
    #END INIT    




Couriers("John","07939545242")
Couriers("Jim","07939545243")
Couriers("Joseph","07939545241",1)
Couriers("James","07939545244")
Couriers("Jhin","07939545245")
Couriers("Jimmy","07939545246")
Couriers("Joe","07939545241",1)
Couriers("Jimothy","07939545247")
Couriers("Jon","07939545248")
Couriers("Johnny","07939545249")
Couriers("Joey","07939545241",1)
Couriers("Jonathon","07939545250")



fm.fake_input()