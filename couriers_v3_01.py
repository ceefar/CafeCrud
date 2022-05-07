import format_random_v2_00 as fm
import re # from re import match - why doesnt this work wtf?
#import csv

# CLASSES ########################################
# COURIERS CLASS #################################

class Couriers:
    couriers_list = [] # list to store all instances of each courier
    couriers_id_cache = []

    # initialisation
    def __init__(self, name:str, phone_number:str, location:str, courier_id:int = None, availability:list = []): 
        """ Load or create new courier with name, phone numb, & id numb """

        def get_valid_courier_id():
            """ if the id you want to use is in the couriers_id_cache then create a new one """
            current_value = int(max(self.couriers_id_cache)) + 1 # plus one to the largest number in the id cache gives you the most valid number for the id (will not duplicate)
            missing_elements = [ele for ele in range(max(self.couriers_id_cache)+1) if ele not in self.couriers_id_cache and ele != 0] # get the missing elements in the list and store in in a new (temp) list
            
            if missing_elements: # has items (so there are valid missing numbers we could use for IDs)
                self.courier_id = missing_elements[0] # use the first (lowest numbered) item in that list (of missing elements)
            else: 
                self.courier_id = current_value # if no missing elements then just the "highest" + 1

            self.couriers_id_cache.append(self.courier_id) # append the id to our cache, having cache means no duplicates, no duplicates means search by id number is plausible
            #END IF
        #END INLINE FUNCTION

        # varaibles, set regardless of load or create (so all except id)
        self.name = name
        self.phone_number = phone_number
        self.location = location
        self.availability = availability # leaving as blank for now as you will set it yourself, tho obvs if we have it then we load it

        # for differences between loading existing and creating new
        if courier_id: # if id has a value, this means you have existing data to use when creating this new object
            self.courier_id = courier_id
            
            if self.courier_id in self.couriers_id_cache:
                # if there is a ID clash then update the id
                print(f"[ Potential ID Clash ({self.courier_id}) Averted ]")
                get_valid_courier_id()
            else:
                self.courier_id = courier_id
                self.couriers_id_cache.append(self.courier_id)
            self.couriers_list.append(self)
            print(f"#{self.courier_id} {self.name} - {self.location} - {self.phone_number} Loaded") # TO ADD A BOOL PARAM FOR SHOWING THIS PRINT STATEMENT?
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
            print(f"#{self.courier_id} - {self.name} - {self.location} - {self.phone_number} Created") # TO ADD A BOOL PARAM FOR SHOWING THIS PRINT STATEMENT?  
        #END IF
    #END INIT    

## PRINT ################################

    # PRINT COURIERS (basic) - one line generator
    def generate_index_name_string(self):
        return((f"{i+1}. {p.name} (#{p.courier_id}) {p.location} {p.phone_number}") for i,p in enumerate(self.couriers_list))

## END CLASS DECLARATIONS #######################################################################################################################################################



## CREATE NEW FUNCTIONS #######################################################################################################################################################


def create_new_courier(disp_size):
    """Create new courier by calling appropriate functions (for validatoin) then creating new instance with the validated inputs"""
    fm.format_display(disp_size)
    print(f"Create New Courier\n{fm.print_dashes(return_it=True)}")
    name = get_name()
    phone_number = get_mobile()
    location = get_location_from_list()
    Couriers(str(name), str(phone_number), str(location))
    fm.format_display()
    get_zeros = lambda x : "0"*(4 - len(str(x)))
    cr = Couriers.couriers_list[-1] # the instances's address in memory
    print(f"Courier #{get_zeros(cr.courier_id)}{cr.courier_id} - {cr.name} Created Sucessfully")
    fm.print_dashes()


def get_name():
    """Get and return name of courier with simple regex validation, not used for update but should refactor for this?"""
    invalid_name = True
    name_is_good = lambda x : re.match(r"\D[a-zA-Z]+($\s{1}|.)", x) # no digits + only a-z chars & ends with exactly one space or only a-z (needs improvement, will do for now), lmabda lets us keep expression outside of loop
    while invalid_name:
        name = input("Enter Name (1 or 2 words, no special characters) : ")
        if name_is_good(name):
            print(f"Name [{name}] Validated")
            break
        else:
            print("Try Again")
    return(name)


def get_location_from_list():
    locations_list = ["London","Manchester","Birmingham","Bristol","Nottingham","Sheffield","Leeds","Newcastle"]
    print(f"Choose Status To Set To Order\n{fm.print_dashes(return_it=True)}") # want order number? could be done easily enough
    print(*(f"[{i+1}] - {location}" for i, location in enumerate(locations_list)))
  
 
    fm.print_dashes()
    user_code = int(input("Choose A Code For The Order : "))
    if user_code == 1:
        return("Preparing")
    elif user_code == 2:
        return("Out For Delivery")
    elif user_code == 3:
        return("Delivered")
    elif user_code == 4:
        return("Recieved")
    elif user_code == 5:
        return("Cancelled")
    elif user_code == 6:
        return("Scheduling")
    else:
        return("Error") # guna return error for debugging but ig should return preparing as default


def get_mobile():
    invalid_mob = True
    mob_is_good = lambda x : re.match(r"^(07\d{8,12}|447\d{7,11})$", x) # lambda lets us keep expression outside of loop, allows 07 start or 447 start but not +
    while invalid_mob:
        num = input("Enter Valid UK Mobile Number (no + symbol) : ")
        if mob_is_good(num):
            print("Number Validated")
            break
        else:
            print("Try Again")
    return(num)


def get_courier_info(self, the_key):
    pass


# GET LOCATION SIMPLE THEN CONTINUE
# THEN UPDATE USING KEY VALUE THING SO ONLY NEED ONE PULL LOOP
# THEN IG IMPROVED STUFF LIKE PAGINATION? check spec tbf


'''
def get_price(to_display = Product.count_products_list(Product) + 1):
    the_price = "1"
    while the_price != "0":
        fm.print_dashes()
        name = input(f"Enter A Name For Product {Product.count_products_list(Product) + 1} : ")
        price_in_pounds = input(f"Enter The Price (In GBP - e.g 12.99) For Product {to_display} : £")
        price_is_good = (re.match(r'\d+(?:\.\d{0,2})?$', price_in_pounds))
        #print(f"price is good? {price_is_good}")
        if price_is_good :
            #print(price_is_good.span())
            #print(price_is_good.group())
            the_price == "0"
            break
        else:
            price_in_pounds = "1"
            print("Wrong Format - Please Try Again")
    # END WHILE
    x = float(price_in_pounds)
    print(f"Returning {x}{type(x)}")
    return(float(price_in_pounds))
'''

## MAIN MENU FUNCTIONS #######################################################################################################################################################

def main_menu():
    disp_size = 20
    rows = 3
    menu_string = [f"COURIERS v3.01\n(using object oriented principles)\n{fm.print_dashes(return_it=True)}\n","[ 1 ] Create New", "[ 2 ] Print All Couriers", "[ - ] -", "[ - ] -", "[ - ] -", "[ - ] -", "[ 8 ] Quick Add 30", "[ 9 ] Quick Add 150", "[ S ] -", "[ L ] -", "[ 0 ] Quit\n","- - - - - - - - - - -"]
    user_menu_input = 1
    print_again = True
    while user_menu_input != "0":
        if print_again: # for quick menu, returns the user to their place in this switch statement without printing the menu again
            # PRINT THE MENU & GET MENU INPUT  
            fm.format_display(disp_size)
            print(*menu_string, sep="\n")
            user_menu_input = input("Enter Menu Selection : ")
        
        # [1] CREATE NEW COURIER
        if user_menu_input == "1":
            create_new_courier(disp_size)
            # QUICK MENU / CREATE AGAIN
            print("Quick Create Another Courier?\n")
            if get_user_yes_true_or_no_false():
                print_again = False
                user_menu_input = "1"
            else:
                print_again = True

        # [2] PRINT COURIERS
        elif user_menu_input == "2":
            print(*(Couriers.generate_index_name_string(Couriers)), sep="\n")
            fm.fake_input()

        # [3] - 
        elif user_menu_input == "3":
            pass
            
        # [7] -  
        elif user_menu_input == "7":
            pass

        # [8] - QUICK ADD 30
        elif user_menu_input == "8":
            quick_add_30_couriers()

        # [9] - QUICK ADD 150
        elif user_menu_input == "9":
            quick_add_30_couriers()
            quick_add_30_couriers()
            quick_add_30_couriers()
            quick_add_30_couriers()
            quick_add_30_couriers()
            quick_add_30_couriers()

        # [S] SETTINGS SUB MENU
        elif user_menu_input == "S" or user_menu_input == "s":
            pass

        # [L] L - LOAD (HIDDEN)
        elif user_menu_input == "L" or user_menu_input == "l":
            pass

        # [0] QUIT THE MENU / LOOP
        elif user_menu_input == "0":
            print("Aite cya")
            break

        # CATCHING WRONG INPUTS
        #else:
        #    print(user_menu_input)
        #    print(go_again)
        #    print("Some Wrong Input Error Message")
        #    break

    # END WHILE
    print("SAVING...")

## OTHER FUNCTIONS #######################################################################################################################################################


def get_user_yes_true_or_no_false():
    # needs try except validation probably as tho this should cover some cases it won't cover all/enough?
    print("[ 1 ] = Yes\n[ 2 ] = No\n")
    fm.print_dashes()
    user_input = input("Your Selection : ".upper())
    if user_input == "1":
        return(True)
    else:
        return(False)

# QUICK ADD COURIERS 
def quick_add_30_couriers():
    print("\n\n\n")
    Couriers("John","07939545242","Birmingham")
    Couriers("Jim","07939545243","Birmingham")
    Couriers("Joseph","07939545241","Birmingham",1)
    Couriers("James","07939545244","Birmingham")
    Couriers("Jhin","07939545245","Birmingham",11)
    Couriers("Jimmy","07939545246","Birmingham")
    Couriers("Joe","07939545241","Birmingham",5)
    Couriers("Jimothy","07939545247","Birmingham")
    Couriers("Jon","07939545248","Birmingham")
    Couriers("Johnny","07939545249","Birmingham")
    Couriers("Joey","07939545241","Birmingham",1)
    Couriers("Jonathon","07939545250","Birmingham",11)
    Couriers("Jonatron","07939545269","Birmingham")
    Couriers("Johnathon","07939545266","Birmingham",20)
    Couriers("Jonamong","07939545169","Birmingham")
    Couriers("Jonathong","07939545260","Birmingham",2)
    Couriers("Jonapong","07939545369","Birmingham")
    Couriers("Jackson","07939545369","Birmingham",5)
    Couriers("Julian","07939545369","Birmingham",55)
    Couriers("Jaxon","07939545369","London",101)
    Couriers("Josh","07939545369","London")
    Couriers("Joshua","07939545369","London",1)
    Couriers("Jack","07939545369","London")
    Couriers("Jayden","07939545369","London",99)
    Couriers("Josiah","07939545369","London")
    Couriers("Jordan","07939545369","London")
    Couriers("Jameson","07939545369","London",3)
    Couriers("Jayce","07939545369","London")
    Couriers("JoJo","07939545369","London")
    Couriers("Mojo-Jojo","07939545369","London")



# DRIVER
main_menu()