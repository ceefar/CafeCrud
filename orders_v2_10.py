import traceback # for error reporting
import time # for pause terminal control
import random # for random
import logging # for logs
import format_random_v2_00 as fm # for formatting display, getting random things
#import main_menu_v2_01 as mm


# create and configure logger

#LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
#logging.basicConfig(filename = "cafe_app.log",
#                                level = logging.DEBUG,
#                                format = LOG_FORMAT,
#                                filemode = "w")
#logger = logging.getLogger()


# FUNCTIONS
#
# FORMAT_RANDOM (as of v2.06)
# format_display(amount_of_lines = 20, end_with_dashes = False, then_text = None)
# print_dashes(amount_of_dashes = 10, formatting = "spaced", dash_char = "-")
# get_random_string_nothing_to_do
# get_random_address
# get_random_name
# get_random_phone(mob_or_house = 8)
# rando_house_phone(y = 8)
# get_curr_ver_from_fname()
# print_app_name()

# ORDERS (as of v2.06)
# add_order_to_orders
# create_an_order
# delete_an_order
# display_couriers_and_return_courier
# get_curr_ver_from_fname
# get_default_list_if_main_is_empty
# get_default_order_list
# get_orders_from_list
# get_user_yes_true_or_no_false
# main
# print_app_name
# print_orders
# print_orders_menu
# print_some_order_info
# take_order
# update_existing_order
# update_existing_order_status
# update_order_status_from_valid
# update_order_to_preparing_or_other_code 



#############################################################################################################################################################
## ALL FUNCTIONS ############################################################################################################################################
#############################################################################################################################################################

# add_order_to_orders
# create_an_order
# display_couriers_and_return_courier
# get_default_order_list
# get_user_yes_true_or_no_false
# main
# print_orders
# print_orders_menu
# print_some_order_info
# take_order
# update_existing_order
# update_existing_order_status
# update_order_status_from_valid
# update_order_to_preparing_or_other_code


#############################################################################################################################################################
## GET / OTHER FUNCTIONS ####################################################################################################################################
#############################################################################################################################################################


## OTHER FUNCTIONS ####################
#######################################
# - get_user_yes_true_or_no_false()
# - get_default_order_list()
#
# IMPROVEMENTS
#   - 


def get_user_yes_true_or_no_false():
    # needs try except validation probably as tho this should cover some cases it won't cover all/enough?
    print("[ 1 ] = Yes")
    print("[ 2 ] = No")
    fm.print_dashes()
    user_input = input("Your Selection : ".upper())
    if user_input == "1":
        return(True)
    else:
        return(False)


def get_default_order_list(go_live = True): # really just for testing
    default_order_1 = {"customer_name":"Knobhead McAsscream","customer_address":"Our House, In The Middle Of Our Street, Madness, 0UR H53","customer_phone":"074541258","courier_number":4,"order_status":"Out For Delivery"}
    default_order_2 = {"customer_name":"Ass McCream","customer_address":"The White House, 1600 Pennsylvania Avenue, Washington DC","customer_phone":"02084119781","courier_number":2,"order_status":"Preparing"}
    default_order_3 = {"customer_name":"Sweet Baby Jesus","customer_address":"Away Inn, A Manger, Heaven, H34 V3N","customer_phone":"07123456789","courier_number":11,"order_status":"Cancelled"}
    default_order_4 = {"customer_name":"Donald Trump","customer_address":"Trump Tower, 725 5th Ave, New York, NY 10022","customer_phone":"02097845123","courier_number":7,"order_status":"Out For Delivery"}
    default_order_5 = {"customer_name":"Leopold Stotch","customer_address":"Address Road, 123 Imagination Land, South Park, NJ 69420","customer_phone":"02091454123","courier_number":9,"order_status":"Preparing"}
    default_order_6 = {"customer_name":"James Bond","customer_address":"Secret Lair, Undercover Street, Disguise, IDK 007","customer_phone":"02077007007","courier_number":7,"order_status":"Sheduling"}
    default_order_7 = {"customer_name":"Hannibal Lector","customer_address":"Billingham Psychiatric Centre, Ward A, PO BOX 1009","customer_phone":"02066699969","courier_number":7,"order_status":"Preparing"}
    default_order_8 = {"customer_name":"Elon Musk","customer_address":"Tesla Factories, Engineering Sector, Floor 38, IM1 337","customer_phone":"07010101010","courier_number":2,"order_status":"Cancelled"}
    default_order_9 = {"customer_name":"Harry Potter","customer_address":"Cupboard Under The Stairs, 4 Privet Drive, Little Whinging, Surrey","customer_phone":"070054684985","courier_number":2,"order_status":"Preparing"}
    default_order_10 = {"customer_name":"Sherlock Holmes","customer_address":"221B Baker St., London, Baker Street","customer_phone":"02088962153","courier_number":2,"order_status":"Out For Delivery"}
    default_order_11 = {"customer_name":"Morticia Addams","customer_address":"Cemetery Ridge, Cemetary Drive, Texas","customer_phone":"07666666666","courier_number":2,"order_status":"Scheduled"}
    default_order_12 = {"customer_name":"Clark Kent","customer_address":"344 Clinton St., Apt. 3B, Metropolis, New York","customer_phone":"07509372451","courier_number":0,"order_status":"Cancelled"}
    default_order_13 = {"customer_name":"Batman","customer_address":"Wayne Manor, Not Bruce Wayne's Building, Gotham City","customer_phone":"020784784784","courier_number":1,"order_status":"Preparing"}
    default_orders_list = []
    default_orders_list.append(default_order_1)
    default_orders_list.append(default_order_2)
    default_orders_list.append(default_order_3)
    default_orders_list.append(default_order_4)
    default_orders_list.append(default_order_5)
    default_orders_list.append(default_order_6)
    default_orders_list.append(default_order_7)
    default_orders_list.append(default_order_8)
    default_orders_list.append(default_order_9)
    default_orders_list.append(default_order_10)
    default_orders_list.append(default_order_11)
    default_orders_list.append(default_order_12)
    default_orders_list.append(default_order_13)
    print("")
    print("No orders found!".upper())
    fm.print_dashes()
    print("Do you want to load in the default orders list".title())
    if go_live == True:
        print("(it will become the live list)")
    fm.print_dashes()
    temp_input = get_user_yes_true_or_no_false()
    if temp_input == True:
        return(default_orders_list)
    else:
        return([]) # an empty list


#############################################################################################################################################################
## ORDERING FUNCTIONS #######################################################################################################################################
#############################################################################################################################################################

# print
# update (status, general)
# delete

## PRINT AN ORDER #####################
#######################################
# - print_orders(orders_list)
#
# IMPROVEMENTS
#   - put search and scroll in own functions


def print_orders(orders_list):
    fm.format_display(then_text = " PRINT ORDERS ".center(60, '-'))
    # if the list is empty prompt user to load the default list (otherwise what you printing huh bud?)
    if len(orders_list) < 1:
        orders_list = get_default_order_list(False) # you are prompted in here, if you say no then it returns an empty list
        fm.format_display()
    
    # if the orders list isn't empty do the print stuff below (you had a chance to just load a default one so this was ur call)
    if len(orders_list) >= 1: # yes this is if not elif intentionally, we want to check twice if the orders list is empty at the start
        print("")
        #fm.format_display()
        print("Printing Default Orders List [ {} Total Orders ]".format(len(orders_list)))
        fm.print_dashes()
        if len(orders_list) >= 3:
            print("[ 1 ] = Search For Order Number")
            fm.print_dashes()
        print("[ 2 ] = Scroll Orders List")
        fm.print_dashes()
        one_or_two = input("Your Selection : ")
        fm.print_dashes()

        if one_or_two == "1": # SEARCH
            fm.format_display(end_with_dashes = True)
            wanted_order = int(input("Enter An Order Number [#1 - #{}] : ".format(len(orders_list))))
            fm.format_display() 
            print(" ORDER #{} FOR {} ".format(wanted_order, orders_list[wanted_order - 1]["customer_name"]).center(60, '-'))
            print("")
            print(" Customer Name = {}".format(orders_list[wanted_order - 1]["customer_name"]))
            print(" Customer Address = {}".format(orders_list[wanted_order - 1]["customer_address"]))
            print(" Customer Phone Number = {}".format(orders_list[wanted_order - 1]["customer_phone"]))
            print(" Courier Number = {}".format(orders_list[wanted_order - 1]["courier_number"]))
            print(" Order Status = {}".format(orders_list[wanted_order - 1]["order_status"]))
            print("")
            faux_input = input("Press Enter To Continue : ")
            
        elif one_or_two == "2": # SCROLL
            # prints by scrolling through the items
            # could always add skip 5 if order list is say over 20
            for order_number, order in enumerate(orders_list): 
                fm.format_display() 
                print(" ORDER #{} ".format(order_number + 1).center(60, '-'))
                print("")
                print(" Customer Name = {}".format(order["customer_name"]))
                print(" Customer Address = {}".format(order["customer_address"]))
                print(" Customer Phone Number = {}".format(order["customer_phone"])) 
                print(" Courier Number = {}".format(order["courier_number"]))
                print(" Order Status = {}".format(order["order_status"]))
                print("")
                #print_dashes(30)
                fm.print_dashes(59, "not spaced")
                print("")
                faux_input = "" # storing the variable so it can be checked for an escape key (m)
                if order_number + 1 < len(orders_list):
                    print("")
                    print("")
                    print("(enter m for menu)")
                    faux_input = input("Press Enter To Print Next Order ({}/{}): ".format(order_number + 1, len(orders_list)))
                else:
                    fm.print_dashes()
                    print("NO MORE ORDERS ({}/{})".format(order_number + 1, len(orders_list)))
                    fm.print_dashes()
                    faux_input = input("Press Enter To Continue : ")
                if faux_input == "M" or faux_input == "m":
                    # if the faux input is M then break (don't keep printing the loop)
                    break

    else:
        # it found no list checking first, it asked you to load one, you said no, so it aint guna do nutting duh!
        fm.print_dashes()
        print("Nothing To Print, You Don't Wanna Load...")
        time.sleep(1)
        print(".")
        time.sleep(0.5)
        print(".")
        time.sleep(0.5)
        print(".")
        time.sleep(0.5)
        print(fm.get_random_string_nothing_to_do())
        fm.print_dashes()
        faux_input = input("Press Enter To Continue : ")


## CREATE AN ORDER #####################
#######################################
# - create_an_order(main_orders_list, main_couriers_list)
#     - take_order(order_number, main_couriers_list)
#           SOLE USE
#           - update_order_to_preparing_or_other_code()
#           - print_some_order_info(customer_name, customer_address, customer_phone, courier_number)
#           - display_couriers_and_return_courier
#           NESTED
#           - if_want_rando_then_rando(to_rando, the_thing)
#           - format_print_info()
#     - add_order_to_orders(orders_list, **order)
#
# IMPROVEMENTS
#   - 


def create_an_order(main_orders_list, main_couriers_list = ["Jesus", "Mary", "Joseph"]):
    # take a new order, store it here
    #logger.debug("main_couriers_list({})".format(main_couriers_list))
    new_order = take_order(len(main_orders_list), main_couriers_list, main_orders_list)
    # then send that order and running orders list to add orders list, which adds the new order to the running orders list
    main_orders_list = add_order_to_orders(main_orders_list, new_order)
    # return the running orders list
    return(main_orders_list)


def take_order(order_number, main_couriers_list, main_orders_list):
    # declarations
    customer_name = ""
    customer_address = ""
    customer_phone = ""
    courier_number = ""
    order_status = ""

    # literally once i realised this works i had to try it lol nested functions wtf, does make so much sense tho, like does actually work for this case, i just made it excessively long to see its interactions
    def if_want_rando_then_rando(to_rando, the_thing = "customer_name"):
        # to rando is the number we're returning that we want to randomise
        # the thing is the key in the key:value pair in the orders dictionary, hence the default "customer_name"        
        order_key = ""

        # get the input, and take input based on the key that you are taking
        # if NOT courier number is same for all >> enter input (with the key formatted to display appropriately)
        # if IS courier number, pull up the couriers list
        #   - then if its a 0 (since everything above 0 will (if in range) be an input)
        #     get a random in between 1 and the length of the list (in range amount) and that will become the return value
        if the_thing != "courier_number":
            to_rando = input("Enter {} : ".format(the_thing))
        elif the_thing == "courier_number":
            #logger.debug("main_couriers_list({})".format(main_couriers_list))
            to_rando = display_couriers_and_return_courier(main_couriers_list, main_orders_list)
            #print("to_rando = {} of type {}".format(to_rando, type(to_rando)))
            if to_rando == 0:
                order_key = random.randint(1, len(main_couriers_list))
                #print("to_rando = {} of type {}".format(to_rando, type(to_rando)))
                to_rando = order_key
                #print("to_rando = {} of type {}".format(to_rando, type(to_rando)))
                print("Randomly Assigned Courier {}".format(to_rando))
            else:
                to_rando -= 1 # legit need this adjust as a return value was altered elsewhere
        # END IF

        # then 
        # since the key is now defo not the courier number (only needs to be different that the others due to the need for the menu we bring up, so you get names)  
        # if its a 0 BRUHHH idk 
        if to_rando == "0":
            order_key = random.randint(1, len(main_couriers_list))
            to_rando = order_key
        # else (if) we just call the random function for each remaining key (name, phone, address) if they key matches the name given 
        elif to_rando == "1": ### USED TO BE ELSE
            if the_thing == "customer_name":
                order_key = fm.get_random_name()
            elif the_thing == "customer_phone":
                order_key = fm.get_random_phone()
            elif the_thing == "customer_address":
                order_key = fm.get_random_address()
            to_rando = order_key
            print("Using Random {} : {}".format(the_thing, to_rando).title())
            return(to_rando)
        else:
            return(to_rando)
    
    def format_print_info():
        fm.format_display()
        print_some_order_info(customer_name, customer_address, customer_phone, courier_number, order_status)
        fm.print_dashes()

    fm.format_display()
    #order number is just amount of orders in the orders list + 1 (basically the index of the next order added to the list)
    print(" TAKE ORDER ".center(60, '-'))
    print("")
    print("ORDER #{}".format(order_number + 1))
    fm.print_dashes(5)
    # takes all order details, returns the order as a dictionary of [ str : str ] pairs
    customer_name = if_want_rando_then_rando(customer_name, "customer_name")
    fm.print_dashes()
    customer_address = if_want_rando_then_rando(customer_address, "customer_address")
    fm.print_dashes()
    customer_phone = if_want_rando_then_rando(customer_phone, "customer_phone")
    fm.print_dashes()
    fm.format_display()
    print_some_order_info(customer_name, customer_address, customer_phone)
    fm.print_dashes()
    #logger.debug("main_couriers_list({})".format(main_couriers_list))
    courier_number = if_want_rando_then_rando(courier_number, "courier_number") # displays couriers with index, returns the users selection with display not index format (it is already + 1, if using this variable to get from couriers_list would need to minus 1 again)
    fm.print_dashes()
    faux_input = input("Press Enter To Continue : ") # could have function here which prompts to press 1 if want to add preparing, or 2 which allows you to add something else, if you press 1 it just insta returns "PREPARING"
    fm.format_display()
    print_some_order_info(customer_name, customer_address, customer_phone, courier_number)
    fm.print_dashes()
    order_status = update_order_to_preparing_or_other_code() # could commit confirm with y or n
    format_print_info()
    order_to_add = {"customer_name": customer_name, "customer_address": customer_address, "customer_phone": customer_phone, "courier_number": courier_number, "order_status": order_status}
    print("ORDER #{} CONFIRMED".format(order_number + 1))
    fm.print_dashes()
    faux_input = input("Press Enter To Continue : ")
    fm.print_dashes()
    return(order_to_add)
    # previously had EXCEPT here that, if hits exception returns default order so it doesn't error, not set up properly anyway so removing


def update_order_to_preparing_or_other_code():
    print("Set Order Status To PREPARING?")
    fm.print_dashes()
    print("[ 1 ] = Yes (set preparing)")
    print("[ 2 ] = No (choose status)")
    fm.print_dashes()
    user_answer = input("Enter Your Answer : ")
    # was theorising this as a quick input method, obvs the index switch way is hardly long, but say there were lots of codes, or manual codes then yeah this would be better for UX imo
    if user_answer == "Y" or user_answer == "y" or user_answer == "1":
        return("Preparing")
    elif user_answer == "N" or user_answer == "n" or user_answer == "2":
        new_code = update_order_status_from_valid()
        return(new_code)
    else:
        print("Invalid Input")
        print("Setting Order Status To Error") # by default should just set to preparing but setting to Error for debugging
        return("Error")
        # could have try except, and except here returning "error" (as order status) just in case


def add_order_to_orders(orders_list, order):
    # take the order from take order (sent from create_an_order) 
    # add order to orders list
    order_to_add = {"customer_name": order["customer_name"], "customer_address": order["customer_address"], "customer_phone": order["customer_phone"], "courier_number": order["courier_number"], "order_status": order["order_status"]}
    orders_list.append(order_to_add) 
    # list(orders_list).append(order_to_add) ?
    return(orders_list)


def print_some_order_info(customer_name, customer_address, customer_phone, courier_number = 0, order_status = None):
    print("Customer Name = {}".format(customer_name))
    print("Customer Address = {}".format(customer_address))
    print("Customer Phone Number = {}".format(customer_phone))
    if courier_number != 0:
        print("Courier Assigned = {}".format(int(courier_number) + 1))
    if order_status != None:
        print("Order Status = {}".format(order_status))


def display_couriers_and_return_courier(main_couriers_list, main_orders_list, ipl = 8):
    #ipl = 8 #### IF SHIT BREAKS REMOVE THE IPL PARAMETER AND JUST ADD HERE - IF REEEEALLY NEEDED TO CHANGE IT COULD BE A SETTING
    the_remainder = len(main_couriers_list) % ipl
    the_pages = int(len(main_couriers_list) / ipl)
    if the_remainder > 0:
        the_pages += 1
    the_spacs = the_pages * 22
    format_spaces = ""
    for m in range(the_spacs):
        format_spaces += " "
    print("Attach A Courier To The Order"+format_spaces+"[1 - {}]".format(len(main_couriers_list)))
    print("courier orders"+"   "+format_spaces+"(preping/live/total)")
    fm.print_dashes(int(the_spacs) - 4)
    print("")
    fm.print_page_formatted_single_list_detailed(main_couriers_list, ipl, main_orders_list) # number is items per vertical line/list - #print(*("[ " + str(item_index + 1) + " ] - " + list_item for item_index, list_item in enumerate(main_couriers_list)), sep="\n") 
    fm.print_dashes()
    user_input = int(input("Enter Your Selection : "))
    if user_input == 0: # this is where you can get random with 0
        return(0) # hence why it returns 0, 0 is the validator for randomisation
    else:
        fm.print_dashes()
        #print("You Selected Courier ({}) - {}".format(main_couriers_list.index(main_couriers_list[user_input - 1]), main_couriers_list[user_input - 1]))
        print("You Selected Courier ({}) - {}".format(int(main_couriers_list.index(main_couriers_list[user_input - 1]) + 1), main_couriers_list[user_input - 1]))
        fm.print_dashes()
        print("Assigning This Courier To The Order Now")
        rv = int(user_input)
        return(rv)


## UPDATE AN ORDER ####################
#######################################
# - update_order_status_from_valid()
# - update_existing_order_status(main_orders_list)
# - update_existing_order(main_orders_list)
#
# IMPROVEMENTS
#   - 


def update_order_status_from_valid(the_code = None):
    #logger.info("ENTER - update_order_status_from_valid({})".format(the_code))
    
    if the_code == None:
        print("Choose Status To Set To Order") # want order number? could be done easily enough
        fm.print_dashes()
        print("[ 1 ] = Preparing")
        print("[ 2 ] = Out For Delivery")
        print("[ 3 ] = Delivered")
        print("[ 4 ] = Recieved")
        print("[ 5 ] = Cancelled")
        print("[ 6 ] = Scheduling")
        # print("[ 7 ] = Custom Code")  #not doing (rn anyways) but could
        fm.print_dashes()
        user_code = int(input("Choose A Code For The Order : "))
    else:
        #logger.debug("if the code != None, User Code = The Code ({})".format(the_code))
        code_to_int = int(the_code)
        user_code = code_to_int
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


def get_orders_from_list(an_orders_list):
    o = 1
    for order_index, order_as_dict in enumerate(an_orders_list):
        order_index = order_index + 1
        fm.print_dashes()
        final_string = ("[ {} ] - ORDER #{} for {}, Current Status = {}".format(o, order_index, order_as_dict["customer_name"], order_as_dict["order_status"]))
        o += 1
        yield(final_string)
        #END FOR
    o = 1
            


def update_existing_order_status(main_orders_list):
    fm.print_dashes()
    fm.format_display(then_text = " UPDATE EXISTING ORDER STATUS ".center(60, '-'))
    
    # if the orders list you get in to this function is empty (len = 0), used to prompt user to load immediately, now prompt to load from menu
    if len(main_orders_list) < 1:
        fm.print_dashes()
        print("No Valid Orders".upper())
        print("- Load Default Orders List From Orders Menu [9]")
        fm.print_dashes()
        faux_input = input("Press Enter To Continue : ")

    # if the orders list isn't empty do the update stuff below (you had a chance to just load a default one so this was ur call)
    elif len(main_orders_list) >= 1:
        for order in get_orders_from_list(main_orders_list):
            print(order)
        fm.print_dashes()
        user_input = int(input("Your Selection : "))
        fm.print_dashes()
        fm.format_display()
        print("Updating Order #{} For {}".format(int(main_orders_list.index(main_orders_list[user_input - 1])) + 1, main_orders_list[user_input - 1]["customer_name"]))
        print("CURRENT ORDER STATUS = {}".format(main_orders_list[user_input - 1]["order_status"]))
        fm.print_dashes()
        new_order_status = update_order_status_from_valid()
        main_orders_list[user_input - 1]["order_status"] = new_order_status
        print("-{}-{}-".format(main_orders_list[user_input - 1]["order_status"],"order_status"))
        faux_input = input("Press Enter To Continue : ")
        return(main_orders_list)
    else:
        # it found no list checking first, it asked you to load one, you said no, so it aint guna do nutting duh!
        fm.print_dashes()
        print("You Didn't Load A Default File")
        time.sleep(0.5)
        print("So I Have Nothing To Do...")
        time.sleep(0.5)
        print(".")
        time.sleep(0.5)
        print(".")
        time.sleep(0.5)
        print(".")
        time.sleep(0.5)
        print(fm.get_random_string_nothing_to_do())
        fm.print_dashes()
        faux_input = input("Press Enter To Continue : ")
        return(main_orders_list)


def update_existing_order(main_orders_list, main_couriers_list):
    fm.print_dashes()
    fm.format_display(then_text = " UPDATE EXISTING ORDER ".center(68, '-'))
    

    def update_values_in_order_with_info(new_value, the_key, user_input_index):
        fm.print_dashes()
        temp_info = the_key_formatted + " = UPDATED [ " + (int(new_value) + 1) + " ]"
        temp_info_strings.append(temp_info)
        temp_info_strings.append("- - - - - - - - - -")
        main_orders_list[user_input_index - 1][the_key] = new_value
        faux_input = input("Press Enter To Continue : ")
        

    # if the orders list you get in to this function is empty (len = 0) then prompt user about loading from menu
    if len(main_orders_list) < 1:
        fm.print_dashes()
        print("No Valid Orders".upper())
        print("- Load Default Orders List From Orders Menu [9]")
        fm.print_dashes()
        faux_input = input("Press Enter To Continue : ")
        #main_orders_list = get_default_order_list()


    # if the orders list isn't empty do the update stuff below (you had a chance to just load a default one so this was ur call)
    elif len(main_orders_list) >= 1:
        for order in get_orders_from_list(main_orders_list):
            print(order)
        fm.print_dashes()
        user_input = int(input("Your Selection : "))
        fm.print_dashes()
        # used to display some basic information about the loop to the user, exists outside of scope as is appended within loop (so vars change each loop)
        temp_info_strings = ["UPDATE LOG (no random functionality)", "-----------------------------------"]
        for the_key, the_value in main_orders_list[user_input - 1].items():
            if the_key != "order_status":
      
                fm.format_display()

                print(*temp_info_strings, sep="\n")
                fm.print_dashes()
                print("Update {}?".format(fm.return_formatted_varaible_name(the_key)))
                print("- current value = {}".format(the_value))
                fm.print_dashes()
                the_key_formatted = fm.return_formatted_varaible_name(the_key)
                quick_input = get_user_yes_true_or_no_false()
                if quick_input == False:
                    if the_key != "courier_number": # done with != courier as it is the last keyvalue pair in the list, so final text display is slightly different
                        fm.print_dashes()
                        print("Ok. Moving To Next Update Field")
                        fm.print_dashes()
                    else:
                        fm.print_dashes()
                        print("Ok. Update User Completed")
                        fm.print_dashes()
                    faux_input = input("Press Enter To Continue : ")
                    temp_info = the_key_formatted + " = NOT UPDATED "
                    temp_info_strings.append(temp_info)
                    temp_info_strings.append("- - - - - - - - - -")
                    continue
                elif the_key != "courier_number":
                    fm.print_dashes()
                    new_value = input("Enter The Update : ")
                    fm.print_dashes()
                    update_values_in_order_with_info(new_value, the_key, user_input)
                    #temp_info = the_key_formatted + " = UPDATED [ " + new_value + " ]"
                    #temp_info_strings.append(temp_info)
                    #temp_info_strings.append("- - - - - - - - - -")
                    #main_orders_list[user_input - 1][the_key] = new_value
                    #faux_input = input("Press Enter To Continue : ")
                elif the_key == "courier_number":
                    fm.format_display(end_with_dashes = True)
                    print("DO NOT USE RANDOM [0] HERE!")
                    new_courier = display_couriers_and_return_courier(main_couriers_list, main_orders_list)
                    # THIS FUNCTION CAN'T DO RANDOM YET!
                    new_courier -= 1
                    fm.print_dashes()
                    temp_info = the_key_formatted + " = UPDATED [ " + str(new_courier) + " ]"
                    temp_info_strings.append(temp_info)
                    temp_info_strings.append("- - - - - - - - - -")
                    main_orders_list[user_input - 1][the_key] = new_courier
                    faux_input = input("Press Enter To Continue : ")
            # END IF
        # END FOR
        temp_info_strings[0] = "FINAL UPDATE RESULTS"
        temp_info_strings[1] = "- - - - - - - - - -"
        fm.format_display()
        print(*temp_info_strings, sep="\n")
        fm.print_dashes()
        faux_input = input("Press Enter To Continue : ")
        return(main_orders_list)
    else:
        # it found no list checking first, it asked you to load one, you said no, so it aint guna do nutting duh!
        fm.print_dashes()
        print("You Didn't Load A Default File")
        time.sleep(0.5)
        print("So I Have Nothing To Do...")
        time.sleep(0.5)
        print(".")
        time.sleep(0.5)
        print(".")
        time.sleep(0.5)
        print(".")
        time.sleep(0.5)
        print(fm.get_random_string_nothing_to_do())
        fm.print_dashes()
        faux_input = input("Press Enter To Continue : ")
        return(main_orders_list)
    

## DELETE AN ORDER ####################
#######################################
# - delete_an_order(main_orders_list)
#
# IMPROVEMENTS
#   - 


def delete_an_order(main_orders_list):
    """take the main_o_list , format & print main_o_list, allow user to select index and delete order from main_o_list, then return main_o_list"""
    #logger.info("delete_an_order({})".format(main_orders_list))

    fm.print_dashes()
    #logger.debug("# *personal test of format display parameters")
    fm.format_display(then_text = " DELETE AN ORDER ".center(68, '-'))
    
    # if the orders recieved is empty (len = 0) prompts the user to load from menu, so they can't break by deleting from nothing
    #logger.debug("# if length of main_orders_list is less than 1")
    if len(main_orders_list) < 1:
        fm.print_dashes()
        print("No Valid Orders".upper())
        print("- Load Default Orders List From Orders Menu [9]")
        fm.print_dashes()
        faux_input = input("Press Enter To Continue : ")

    # else if the orders list isn't empty do the update stuff below (you had a chance to just load a default one so this was ur call)
    elif len(main_orders_list) >= 1:
        #logger.debug("# if length of main_orders_list is greater than or equal to 1")
        for order in get_orders_from_list(main_orders_list):
            print(order)
            #END FOR
        fm.print_dashes()
        user_input = int(input("Your Selection : "))
        fm.print_dashes()
        fm.format_display(end_with_dashes = True)
        print("DELETE ORDER #{} FOR {}?".format(int(main_orders_list.index(main_orders_list[user_input - 1])) + 1, main_orders_list[user_input - 1]["customer_name"]))
        fm.print_dashes()
        if get_user_yes_true_or_no_false() == True:
            fm.print_dashes()
            print("Deleting Order #{}".format(int(main_orders_list.index(main_orders_list[user_input - 1])) + 1))
            main_orders_list.pop(user_input - 1)
        else:
            print("Deletion of Order #{} Cancelled".format(int(main_orders_list.index(main_orders_list[user_input - 1])) + 1))
        fm.print_dashes()
        faux_input = input("Press Enter To Continue : ")
        #logger.info("delete_an_order END - return({})".format(main_orders_list))
        return(main_orders_list)



#############################################################################################################################################################
## MAIN, ORDERS MENU, & DRIVER ##############################################################################################################################
#############################################################################################################################################################


## ORDERS MENU FUNCTIONS ##############
#######################################
# - main()
#     - print_orders_menu()
#
# IMPROVEMENTS
#   - 


def main_orders(main_couriers_list, main_orders_list):
    # ORDERS MENU
    # INITIALISING VARIABLES
    #main_couriers_list = ["Jesus","Mary","Jane","Joseph","Mary Jane","Sweet Baby Jesus"]
    user_orders_menu_input = 1
    try:
        # FUNCTION
        #logger.debug("main_couriers_list({})".format(main_couriers_list))
        while user_orders_menu_input != "0":
            # PRINT THE MENU & GET THE USERS INPUT
            print_better_orders_menu()
            user_orders_menu_input = input("Enter Menu Selection : ") # make int and dont check against strings or ? (confirm what would be best ig)
            # PRINT ALL ORDERS
            if user_orders_menu_input == "1":
                print_orders(main_orders_list)
            # CREATE AN ORDER
            elif user_orders_menu_input == "2":
                main_orders_list = create_an_order(main_orders_list, main_couriers_list)
            # UPDATE AN ORDER - ONLY ORDER STATUS
            elif user_orders_menu_input == "3":
                main_orders_list = update_existing_order_status(main_orders_list)
            # UPDATE AN ORDER - EXCEPT ORDER STATUS
            elif user_orders_menu_input == "4":
                main_orders_list = update_existing_order(main_orders_list, main_couriers_list)
            # DELETE AN ORDER
            elif user_orders_menu_input == "5":
                main_orders_list = delete_an_order(main_orders_list)
            # magic
            elif user_orders_menu_input == "8":
                x = input("Give me an order code and i will tell you it's value")
                print(update_order_status_from_valid(x))
                fm.fake_input()
            # LOAD A DEFAULT ORDERS LIST
            elif user_orders_menu_input == "9":
                # if you don't have an empty list it doesn't let you do this (should increase the size of the default list so this is more useful)
                main_orders_list = get_default_list_if_main_is_empty(main_orders_list)
            # QUIT THE MENU
            elif user_orders_menu_input == "0":
                # randomised leaving message function here pls
                break
            # HANDLING ERRORED INPUTS
            elif int(user_orders_menu_input) >= 5:
                print("ERROR - INPUT MORE THAN VALID RANGE")
                fm.print_dashes()
                print("WTF Are You Doing?")
                faux_input = input("Press Enter To Try Again : ")
            elif int(user_orders_menu_input) <= -1:
                print("ERROR - INPUT LESS THAN VALID RANGE")
                fm.print_dashes()
                print("Wow, Negative Numbers Huh")
                print("You Tryna Kill Me? WTF!")
                faux_input = input("Press Enter To Try Again : ")
            else:
                print("ERROR - NOT A VALID INPUT")
                fm.print_dashes()
                print("Seriously... WTF Are You Doing?")
                faux_input = input("Press Enter To Try Again : ")
    except Exception as e:
        fm.print_dashes()
        print("ERROR - There Has Been A Fatal Error".upper())
        e.traceback = traceback.format_exc()
        error = 'Unhandled exception in asyn call:\n{}'.format(e.traceback)
        print(error)
        fm.print_dashes()  
    # WHILE LOOP HAS BEEN BROKEN
    # now this isn't the top level menu just return the orders list when you break
    #fm.format_display(end_with_dashes = True)
    #print("Aite Bish We Out")
    #fm.print_dashes()
    #print("Do Save And Shit Here")
    #fm.print_dashes(20)
    #faux_input = input("Press Enter To Exit : ")
    return(main_orders_list)


def get_default_list_if_main_is_empty(main_orders_list):
    fm.format_display(end_with_dashes = True)
    if len(main_orders_list) >= 1:
        print("You Already Have A Usable Orders List")
        fm.print_dashes()
        print("Returning To Menu")
        fm.print_dashes()
        faux_input = input("Press Enter To Continue : ")
        return(main_orders_list)
    else:
        main_orders_list = get_default_order_list()
        if len(main_orders_list) >= 1:
            print("Default List Loaded")
            fm.print_dashes()
            faux_input = input("Press Enter To Continue")
            return(main_orders_list)


def print_orders_menu():
    fm.print_app_name("orders")
    print("[ 1 ] to Print Orders List")
    print("[ 2 ] to Create New Order")
    print("[ 3 ] to Update Existing Orders Status")
    print("[ 4 ] to Update Existing Order")
    print("[ 5 ] to Delete Existing Order")
    print("[ 9 ] to Load The Default Orders List [testing]")
    print("[ - ] to Main Menu")
    print("[ 0 ] to Quit") 
    fm.print_dashes()   


def print_better_orders_menu():
    fm.print_app_name("orders")
    menu_string = ["[ 1 ] to Print Orders List",
                    "[ 2 ] to Create New Order",
                    "[ 3 ] to Update Existing Orders Status",
                    "[ 4 ] to Update Existing Order",
                    "[ 5 ] to Delete Existing Order",
                    "[ 8 ] to Get Order Code Info (alpha)",
                    "[ 9 ] to Load The Default Orders List (testing)",
                    "[ 0 ] for Main Menu",
                    "- - - - - - - - - - -"]
    print(*menu_string, sep="\n")


# DRIVER
#main_orders()




##################### PRINT CURRENT FUNCTIONS
#for module_name in dir():
#    print("#"+module_name)


##################### VERSION HISTORY / CHANGE LOG 
# - start doing this properly pls
#
# v1.04
#   - finishing print orders list function (should have another new function to call the print for the purpose of tidying up or nah?)
#   - ensuring create order and print work as expected then probably new version for continuing
#
# v1.06
#   - print and create orders now working and formatted
#       - needs proper v1 validation and try and excepts still tho
#
# v1.07
#   - added a function that allowed for manual/custom order status input
#       - realise now that is supposed to be through indexed items not custom strings so updating for it
#   - then doing remaining update ahd delete order
#   - want to start putting shit in different files asap btw
#
# v2.01
#   - currently completing 
#       - update existing order status 
#       - update existing order
#
# v2.02
#   - moving the get_default_list outside of the functions it's called in, and placing it in a menu item for better clarity and to avoid potential future issues
#
#




#############################################################################################################################################################
## PRESENTATION NOTES #######################################################################################################################################
#############################################################################################################################################################

## UX IMPROVEMENTS AND FUNCTIONALITY ##############
###################################################

# im a big fan of UX design, as such first thing I decided to divert from spec on to improve ux was
# expand the input format to include b and m keys as well as the additional menu options and keep these consistent, m always main menu, b always back
# this was because tho inputs worked fine as give, as menu scope expanded this gave *me* as a user more ease of manueverability through the menus
# making the process seem effortless, instead of laborious (good ux is never noticed, bad ux is...)
# but that is from previous version
# in this current refactoring...
# my first big ux step has been to design the entire program from the ground up with my person "lay z boi" methodology,
# this states that design is best (from both a users and a coders perspectives) when it can be used in the laziest way possible
# essentially meaning this entire program can be used (by the programmer) with one hand
# this meant not only ensuring that typical terminal inputs like "Y for Yes or N for No" are swapped out for "1" and "2" - though you can still use Y or N if you wish
# but also creating default options for loading in data for testing (if it isn't currently available) by using the menu to load this in to usable variables
# and even further still for inputs like names addresses and phone numbers you can utilise the number pad only to produce complete, random results
# and even randomise things like courier number too (though for this the 0 key is used instead of 1 since 1 it the first displayed selection for ints)
# this means lots of escape keys, extra functions and variables, however personally for me has not just been interesting and rewarding
# but also saved a lot of time, and actually seconding that point by properly using UX principles, like displaying back verification when something has happened,
# on the fly testing has been much easier that when the program was far more simplified and instantaneous with its input/output actions
# obviously also having a clean UI has helped, all in all i have felt the impact of the extra time spend developing and not debugging 
# due to solid and intuitive UX practices