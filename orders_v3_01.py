import format_random_v2_00 as fm
import re
import couriers_v3_01 as cour
import products_v1_02 as prdct
import pymysql
import os
import random
from dotenv import load_dotenv
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)
 

## END IMPORTS


# Load environment variables from .env file
load_dotenv()
host = os.environ.get("mysql_host")
user = os.environ.get("mysql_user")
password = os.environ.get("mysql_pass")
database = os.environ.get("mysql_db")

# Establish a database connection
connection = pymysql.connect(
    host = host,
    user = user,
    password = password,
    database = database
)

def get_from_db(command):
    cursor = connection.cursor()
    cursor.execute(f"{command}") 
    myresult = cursor.fetchall()
    #.commit()
    #cursor.close()
    #connection.close()
    return(myresult)

def read_from_db():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM couriers") 
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)
    #connection.commit()
    #cursor.close()
    #connection.close()

def add_to_db(command):
    cursor = connection.cursor()
    cursor.execute(f"{command}") 
    connection.commit()
    #cursor.close()
    #connection.close()


# CLASSES ##################################################################################################################################################################

# ORDERS CLASS #################################

class Orders:
    """ Orders class stores each order object in a 'global' list, customer name, address, phone + courier id + product ids + order status and (new) tot price """
    orders_list = [] # list to store all instances of each courier
    orders_id_cache = [] # for ensuring the same orders id is NEVER used again, this is of critical importance imo

    # init constructor
    def __init__(self, customer_name:str, customer_address:str, customer_phone:str, order_status:str, order_price:float, order_id:int, courier_id:int = None, products_ids:list = []): 
        """ Load or create new courier with name, phone numb, & id numb """
        
        def get_valid_order_id():
            """ if the id you want to use is in the couriers_id_cache then create a new one """
            current_value = int(max(self.orders_id_cache)) + 1 
            missing_elements = [ele for ele in range(max(self.orders_id_cache)+1) if ele not in self.orders_id_cache and ele != 0] 

            if missing_elements: # has items
                self.order_id = missing_elements[0]
            else: 
                self.order_id = current_value 

            self.orders_id_cache.append(self.order_id)
            #END IF
        #END INLINE FUNCTION

        # varaibles, set regardless of load or create (so all except id)
        self.customer_name = customer_name
        self.customer_address = customer_address
        self.customer_phone = customer_phone
        self.order_status = order_status
        self.order_price = order_price
        self.courier_id = courier_id
        self.products_ids = products_ids  # leaving as blank for now as you will set it yourself, tho obvs if we have it then we load it

        # for differences between loading existing and creating new
        if order_id: # if id has a value, this means you have existing data to use when creating this new object
            self.order_id = order_id
            
            if self.order_id in self.orders_id_cache:
                # if there is a ID clash then update the id
                print(f"[ Potential ID Clash ({self.order_id}) Averted ]")
                get_valid_order_id()
            else:
                self.order_id = order_id
                self.orders_id_cache.append(self.order_id)
            self.orders_list.append(self)
            print(f"#{self.order_id} {self.customer_name} - {self.customer_phone} - {self.order_status} - {self.customer_address} {courier_id} Loaded") # TO ADD A BOOL PARAM FOR SHOWING THIS PRINT STATEMENT?
        else:
            # you are creating from scratch, so you need a new, dynamically created order_id
            if self.orders_id_cache: # has items
                get_valid_order_id()
            else:
                # if the cache has no items then its the first ite, so if its a brand new courier their number will be one (ooooo lucky you huh)
                self.order_id = 1
                self.orders_id_cache.append(self.order_id)
            # append it to the "global" list and print back confirmation
            self.orders_list.append(self)
            print(f"Order #{self.order_id} Created\nCUSTOMER INFO\nName: {self.customer_name}, Phone: {self.customer_phone}, Address: {self.customer_address}\nORDER INFO") # TO ADD A BOOL PARAM FOR SHOWING THIS PRINT STATEMENT?
            print(f"Order Status: {self.order_status}, Assigned Courier: {courier_id}, Order Price: £{self.order_price}")
            print(f"Order Info For Restaurant : {self.products_ids}")
        #END IF
    #END INIT    

# PRINT FUNCTIONS

    # COURIERS - THIS NEEDS TO BE FIXED AGAIN BUT CBA
    # simple couriers print, code copied (could have just called the function knobhead!)
    def items_per_list_print_couriers(disp_size: int=22, rows = 3):
        #ipl = rows #da fuck

        usable_screen = int(disp_size) - 10
        ipl = usable_screen
        i_list = []
        # function
        # creates the initial lists with just ints of the order
        for g in range(ipl):
                x = g # if needs to be plus 1 then do here and also in x < len(main_co_list) + 1
                g_list = []
                for i in range(int(len(cour.Couriers.couriers_list)/ipl) + 1): # rows? needed (for X per line)
                    if x < len(cour.Couriers.couriers_list):
                        g_list.append(x)
                    x += ipl
                i_list.append(g_list)
                x += 1
                # END FOR
        # END FOR    
        # filling in the above for loop with the data you want

        for short_list in i_list: 
            print_string = ""
            for index in short_list:
                cr = cour.Couriers.couriers_list[index]  
                live_ords = get_live_orders_for_courier(index)
                current_string = (f"{index} {cour.Couriers.couriers_list[index].name} {cr.location} {live_ords}")
                spaces = 36 - (len(current_string))
                spaces_string = ""
                if int(index) + 1 == 10:
                    spaces -= 1
                for x in range(spaces):
                    spaces_string += " "
                print_string += (f"[ {int(index) + 1} ] {cr.name} {spaces_string} ({live_ords}) - {cr.location}      ")
            print(print_string)

    # ORDERS

    def print_orders(self):
        fm.format_display(then_text = " PRINT ORDERS ".center(60, '-'))
        # if the list is empty prompt user to load the default list (otherwise what you printing huh bud?)
        if len(self.orders_list) < 1:
            print("No Orders List - WTF?!") # you are prompted in here, if you say no then it returns an empty list
            fm.format_display()

        # if the orders list isn't empty do the print stuff below (you had a chance to just load a default one so this was ur call)
        if len(self.orders_list) >= 1: # yes this is if not elif intentionally, we want to check twice if the orders list is empty at the start
            print("")
            #fm.format_display()
            print("Printing Default Orders List [ {} Total Orders ]".format(len(self.orders_list)))
            fm.print_dashes()
            if len(self.orders_list) >= 3:
                print("[ 1 ] = Search For Order Number")
                fm.print_dashes()
            print("[ 2 ] = Scroll Orders List")
            fm.print_dashes()
            one_or_two = input("Your Selection : ")
            fm.print_dashes()

            # SEARCH - PROBS (LIKE PROBLY DEFO) NEEDS GET ATTR UPDATE WHICH IS FINE (not tested at all, expecting will error like fuck)
            if one_or_two == "1": 
                fm.format_display(end_with_dashes = True)
                wanted_order = int(input("Enter An Order Number [#1 - #{}] : ".format(len(self.orders_list))))
                fm.format_display() 
                print(" ORDER #{} FOR {} ".format(wanted_order, self.orders_list[wanted_order - 1]["customer_name"]).center(60, '-'))
                print("")
                print(" Customer Name = {}".format(self.orders_list[wanted_order - 1]["customer_name"]))
                print(" Customer Address = {}".format(self.orders_list[wanted_order - 1]["customer_address"]))
                print(" Customer Phone Number = {}".format(self.orders_list[wanted_order - 1]["customer_phone"]))
                print(" Courier Number = {}".format(self.orders_list[wanted_order - 1]["courier_number"]))
                print(" Order Status = {}".format(self.orders_list[wanted_order - 1]["order_status"]))
                print(" Order Price = {}".format(self.orders_list[wanted_order - 1]["order_price"]))
                print(" For Restaurant = {}".format(self.orders_list[wanted_order - 1]["products_ids"]))
                print("")
                faux_input = input("Press Enter To Continue : ")

            elif one_or_two == "2": # SCROLL
                # prints by scrolling through the items
                # could always add skip 5 if order list is say over 20
                for order_number, order in enumerate(self.orders_list):  
                    fm.format_display() 
                    print(" ORDER #{} ".format(order_number + 1).center(60, '-'))
                    print(f" ORDER #{getattr(order,'order_id')} FOR {getattr(order,'customer_name')}")
                    print("")
                    print(f" Customer Name = {getattr(order,'customer_name')}")
                    print(f" Customer Address = {getattr(order,'customer_address')}")
                    print(f" Customer Phone Number = {getattr(order,'customer_phone')}") 
                    print(f" Courier ID = {getattr(order,'courier_id')}")
                    print(f" Order Status = {getattr(order,'order_status')}")
                    print("")
                    #print_dashes(30)
                    fm.print_dashes(59, "not spaced")
                    print("")
                    faux_input = "" # storing the variable so it can be checked for an escape key (m)
                    if order_number + 1 < len(self.orders_list):
                        print("")
                        print("")
                        print("(enter m for menu)")
                        faux_input = input("Press Enter To Print Next Order ({}/{}): ".format(order_number + 1, len(self.orders_list)))
                    else:
                        fm.print_dashes()
                        print("NO MORE ORDERS ({}/{})".format(order_number + 1, len(self.orders_list)))
                        fm.print_dashes()
                        faux_input = input("Press Enter To Continue : ")
                    if faux_input == "M" or faux_input == "m":
                        # if the faux input is M then break (don't keep printing the loop)
                        break

        else:
            # it found no list checking first, it asked you to load one, you said no, so it aint guna do nutting duh!
            fm.print_dashes()
            print("Nothing To Print, You Don't Wanna Load...")
            fm.print_dashes()
            faux_input = input("Press Enter To Continue : ")


''' FOR THE GET_ATTR WAY

        for i, courier in enumerate(cour.Couriers.couriers_list):
            x = getattr(courier, "name")
            z = getattr(courier, "location")
            # BRUHHH THEN CAN ZIP WITH ORDERS INFO NAH DONT NEED TO ZIP JUST CHECK AGAINST AND GET THE INFO HERE, WELL HAVE A FUNCTION CALL TO DO THAT NOT IN LOOP BUT BOSH!
            print(f"[ {i} ] - {x}, Location - {z}")
'''


# print(f"Order #{self.order_id} Created\nCUSTOMER INFO\nName: {self.customer_name}, Phone: {self.customer_phone}, Address: {self.customer_address}\nORDER INFO") # TO ADD A BOOL PARAM FOR SHOWING THIS PRINT STATEMENT?
# print(f"Order Status: {self.order_status}, Assigned Courier: {courier_id}, Order Price: £{self.order_price}")
# print(f"Order Info For Restaurant : {self.products_ids}")


## MAIN PROGRAM ############################################################################################################################################################


## NEW DB PRINT STUFF ######################################################################################################################################################

def make_address_readable(an_address:str):
    # should add if no comma just clip it at X chars (like 15 or sumnt)
    if an_address:
        ndx = an_address.find(",")
        if ndx != -1:
            new_addy = an_address[:ndx]
            return(new_addy)
        elif len(an_address) > 18:
            return(an_address[:18])

def get_couriers_name_from_id(ndx:int):
    query = f"SELECT c.name FROM couriers c WHERE c.courier_db_id = {ndx}"
    result = str(get_from_db(query))
    ndx = result.find("'",3)
    final_result = result[3:ndx]
    return(final_result.strip())

def db_print_orders(disp_size: int=22, rows = 3):
    usable_screen = int(disp_size) - 15
    ipl = usable_screen
    length_of_couriers = get_from_db(f'SELECT * FROM orders')
    length_of_couriers = len(length_of_couriers)
    total_pages = int(length_of_couriers / ipl)
    if (length_of_couriers % ipl) != 0:
        total_pages += 1
    final_page = len(range(total_pages))
    print(f"FINAL PAGE : {final_page}")
    print(f"Total Pages = {total_pages}")
    pages_display = [f"[ {x+1} ]" for x in range(total_pages)]
    pages_display = " - ".join(pages_display)
    fm.format_display(disp_size)
    want_more_print = True
    current_page = 1
    dont_print = False
    query = f'SELECT * FROM orders LIMIT {ipl}'
    #print(f"display size = {disp_size}")
    #print(f"display size = {rows}")

    def create_spaces(string_to_space:str = "Some Default String", space_count:int = 30, just_return:int = None):
        if just_return:
            return_spaces = ""
            for _ in range(just_return):
                return_spaces += " "
            return(return_spaces)
        else:
            to_space = len(string_to_space)
            final_space_count = space_count - to_space 
            string_of_spaces = ""
            for x in range(final_space_count):
                string_of_spaces += " "
            return(string_of_spaces)

    while want_more_print: 
        #query = query
        result = get_from_db(query)
        if dont_print:
            pass
        else:
            print(f"{Style.BRIGHT}Customer {create_spaces(just_return=22)} Order Status{create_spaces(just_return=24)} Order Delivery{create_spaces(just_return=35)} Customer Contact{create_spaces(just_return=9)}For Restaurant (product number, quantity)")
            print(f"{fm.print_dashes(return_it=True)} {create_spaces(just_return=8)} {fm.print_dashes(return_it=True)} {create_spaces(just_return=13)} {fm.print_dashes(return_it=True)} {create_spaces(just_return=26)} {fm.print_dashes(amount_of_dashes=7, return_it=True)}{create_spaces(just_return=8)} {fm.print_dashes(return_it=True)}")
        for order_info in result:
            x = f"[ {order_info[0]} ] {order_info[1]}  {order_info[3]} {order_info[4]} {make_address_readable(order_info[2])} {order_info[5]} {get_couriers_name_from_id(order_info[7])}" #{order_info[8]}
            display1 = f"[ {order_info[0]} ] {order_info[1]}"
            display2 = f"- £{order_info[5]} : {order_info[4]}"  
            display3 = f"- {get_couriers_name_from_id(order_info[7])} - @ {make_address_readable(order_info[2])}"        
            display4 = f"@ {order_info[3]}"  
            spaces1 = create_spaces(display1, 30)
            spaces2 = create_spaces(display2, 30)
            spaces3 = create_spaces(display3, 48)
            spaces4 = create_spaces(display4, 25)
            #current_str = len(x)
            #spaces = 90 - current_str
            #spaces_string = ""
            #for x in range(spaces):
            #    spaces_string += " "
            #print(courier)
           

            if dont_print:
                pass
                #print("You've Entered The Wrong Page Number")
            else:
                print(f"{Fore.BLUE}[ {Fore.CYAN}{order_info[0]} {Fore.BLUE}] {Fore.RESET}{order_info[1]} {spaces1} £{order_info[5]} [PAID] - {order_info[4]} {spaces2} {get_couriers_name_from_id(order_info[7])} -> to {make_address_readable(order_info[2])} {spaces3} {order_info[3]} {spaces4} {order_info[8]}") # {order_info[8]}

        if dont_print:
            pass
        else:
            print(f"{fm.print_dashes(return_it=True)} {create_spaces(just_return=8)} {fm.print_dashes(return_it=True)} {create_spaces(just_return=13)} {fm.print_dashes(return_it=True)} {create_spaces(just_return=26)} {fm.print_dashes(amount_of_dashes=7, return_it=True)}{create_spaces(just_return=8)} {fm.print_dashes(return_it=True)}")
        print("")    
        #print(pages_display)

        page_numbs = [f"{x+1}" for x in range(total_pages)]
        #print(f"current_page = {current_page}") 
        #print(f"page_numbs = {page_numbs}") 
        
        highlight_page = lambda h : f"{Fore.BLUE}[[ {Fore.CYAN}{h}{Fore.BLUE} ]]" if h == str(current_page) else f"[ {h} ]" # language is so mad wtf            
        print(*[highlight_page(p) for p in page_numbs])
        print("")   
        paginate_action = (input("Enter A Page Number Or 0 To Quit : "))
        #print(current_page)
        #print(final_page)
        #print(paginate_action)
        fm.print_dashes()
        g = (int(paginate_action))
        if g > final_page:
            fm.format_display(disp_size)
            cour.return_one_line_art()
            current_page = int(paginate_action)
            dont_print = True
        elif paginate_action != "0":
            fm.format_display(disp_size)
            current_page = int(paginate_action)
            query = f'SELECT * FROM orders WHERE order_id > {(current_page - 1) * ipl} LIMIT {ipl}'
            dont_print = False
        else:
            #fm.format_display(disp_size)
            print("Ok Bye")
            want_more_print = False


############################################################################################################################################


def db_print_orders_for_every_courier(disp_size: int=22, rows = 3):
    usable_screen = int(disp_size) - 10
    ipl = usable_screen
    length_of_couriers = get_from_db(f'SELECT o.customer_name, o.customer_address, o.order_price, o.order_id, o.order_status, c.name, c.courier_db_id FROM orders o RIGHT JOIN couriers c ON o.courier_id = c.courier_db_id ORDER BY c.courier_db_id')
    length_of_couriers = len(length_of_couriers)
    total_pages = int(length_of_couriers / ipl)
    if (length_of_couriers % ipl) != 0:
        total_pages += 1
    final_page = len(range(total_pages))
    print(f"FINAL PAGE : {final_page}")
    print(f"Total Pages = {total_pages}")
    pages_display = [f"[ {x+1} ]" for x in range(total_pages)]
    pages_display = " - ".join(pages_display)
    fm.format_display(disp_size)
    want_more_print = True
    current_page = 1
    dont_print = False
    query = f'SELECT o.customer_name, o.customer_address, o.order_price, o.order_id, o.order_status, c.name, c.courier_db_id FROM orders o RIGHT JOIN couriers c ON o.courier_id = c.courier_db_id ORDER BY c.courier_db_id LIMIT {ipl}'
    #print(f"display size = {disp_size}")
    #print(f"display size = {rows}")

    def create_spaces(string_to_space:str = "Some Default String", space_count:int = 30, just_return:int = None):
        if just_return:
            return_spaces = ""
            for _ in range(just_return):
                return_spaces += " "
            return(return_spaces)
        else:
            to_space = len(string_to_space)
            final_space_count = space_count - to_space 
            string_of_spaces = ""
            for x in range(final_space_count):
                string_of_spaces += " "
            return(string_of_spaces)

    while want_more_print: 
        #query = query
        result = get_from_db(query)
        if dont_print:
            pass
        else:
            print(f"Courier {create_spaces(just_return=23)} Order Status{create_spaces(just_return=7)} Order Delivery{create_spaces(just_return=37)} Customer Contact")
            print(f"{fm.print_dashes(return_it=True)} {create_spaces(just_return=8)} {fm.print_dashes(amount_of_dashes=5, return_it=True)} {create_spaces(just_return=6)} {fm.print_dashes(return_it=True)} {create_spaces(just_return=28)} {fm.print_dashes(amount_of_dashes=7, return_it=True)}")
        for order_info in result:

            def none_order_status(is_it_none:str):
                if is_it_none is None:
                    return("No Bueno")
                else:
                    return(is_it_none)

            def dont_print_none(is_it_none:str, opt=4):
                if is_it_none is None and opt == 1:
                    return("X")
                elif is_it_none is None and opt == 2:
                    return("Nobody")
                elif is_it_none is None and opt == 3:
                    return("Nowhere")
                elif is_it_none is None and opt == 5:
                    return("zilch")
                elif is_it_none is None:
                    return("    ")
                else:
                    return(is_it_none)
            
            display1 = f"[ {order_info[5]} ] {order_info[6]}"
            display2 = f"{none_order_status(order_info[4])}"
            display3 = f"{dont_print_none(order_info[3], 1)} {dont_print_none(order_info[0], 2)} {dont_print_none(make_address_readable(order_info[1]), 3)}"  
            spaces1 = create_spaces(display1, 32)
            spaces2 = create_spaces(display2, 18)
            spaces3 = create_spaces(display3, 35)

            if dont_print:
                pass
            else:
                print(f"#{order_info[6]} {order_info[5]}  {spaces1} {none_order_status(order_info[4])} {spaces2} Order #{dont_print_none(order_info[3], 1)} For {dont_print_none(order_info[0], 2)} - @ {dont_print_none(make_address_readable(order_info[1]), 3)} {spaces3} £{dont_print_none(order_info[2], 5)}") 

        if dont_print:
            pass
        else:
            print(f"{fm.print_dashes(return_it=True)} {create_spaces(just_return=8)} {fm.print_dashes(amount_of_dashes=5, return_it=True)} {create_spaces(just_return=6)} {fm.print_dashes(return_it=True)} {create_spaces(just_return=28)} {fm.print_dashes(amount_of_dashes=7, return_it=True)}")
        print("")    
        #print(pages_display)

        page_numbs = [f"{x+1}" for x in range(total_pages)]
        #print(f"current_page = {current_page}") 
        #print(f"page_numbs = {page_numbs}") 
        
        highlight_page = lambda h : f"[[ {h} ]]" if h == str(current_page) else f"[ {h} ]" # language is so mad wtf            
        print(*[highlight_page(p) for p in page_numbs])
        print("")   
        paginate_action = (input("Enter A Page Number Or 0 To Quit : "))
        #print(current_page)
        #print(final_page)
        #print(paginate_action)
        fm.print_dashes()
        g = (int(paginate_action))
        if g > final_page:
            fm.format_display(disp_size)
            cour.return_one_line_art()
            current_page = int(paginate_action)
            dont_print = True
        elif paginate_action != "0":
            fm.format_display(disp_size)
            current_page = int(paginate_action)
            def if_minus(x):
                if x < 0:
                    return(0)
                else:
                    #print(f"IM RETURNING X = {x}")
                    return(x)
            if paginate_action == "1":
                query = f'SELECT o.customer_name, o.customer_address, o.order_price, o.order_id, o.order_status, c.name, c.courier_db_id FROM orders o RIGHT JOIN couriers c ON o.courier_id = c.courier_db_id ORDER BY c.courier_db_id LIMIT {ipl}'
            elif paginate_action == "2":
                query = f'SELECT o.customer_name, o.customer_address, o.order_price, o.order_id, o.order_status, c.name, c.courier_db_id FROM orders o RIGHT JOIN couriers c ON o.courier_id = c.courier_db_id ORDER BY c.courier_db_id LIMIT {ipl}, {ipl}'
            else:
                query = f'SELECT o.customer_name, o.customer_address, o.order_price, o.order_id, o.order_status, c.name, c.courier_db_id FROM orders o RIGHT JOIN couriers c ON o.courier_id = c.courier_db_id  WHERE c.courier_db_id > 2 ORDER BY c.courier_db_id LIMIT {if_minus((current_page-2)*ipl-1)}, {ipl}'
            dont_print = False
        else:
            #fm.format_display(disp_size)
            print("Ok Bye")
            want_more_print = False



############################################################################################################################################

def get_total_orders_for_courier(chosen_courier:int):
    chosen_courier += 1
    query = f"SELECT o.order_status FROM orders o INNER JOIN couriers c ON o.courier_id = c.courier_db_id WHERE c.courier_db_id = {chosen_courier} ORDER BY c.courier_db_id"
    result = get_from_db(query)
    return(len(result))


def get_completed_orders_for_courier(chosen_courier:int):
    chosen_courier += 1
    query = f"SELECT o.order_status FROM orders o INNER JOIN couriers c ON o.courier_id = c.courier_db_id WHERE c.courier_db_id = {chosen_courier} AND (o.order_status = 3 OR o.order_status = 4 OR o.order_status = 5) ORDER BY c.courier_db_id"
    result = get_from_db(query)
    return(len(result))


def db_print_courier_for_search(disp_size: int=22, rows = 3):
    usable_screen = int(disp_size) - 10
    ipl = usable_screen
    length_of_couriers = get_from_db(f'SELECT c.courier_db_id, c.name, c.location, c.phone_number FROM couriers c')
    length_of_couriers = len(length_of_couriers)
    total_pages = int(length_of_couriers / ipl)
    if (length_of_couriers % ipl) != 0:
        total_pages += 1
    final_page = len(range(total_pages))
    print(f"FINAL PAGE : {final_page}")
    print(f"Total Pages = {total_pages}")
    pages_display = [f"[ {x+1} ]" for x in range(total_pages)]
    pages_display = " - ".join(pages_display)
    fm.format_display(disp_size)
    want_more_print = True
    current_page = 1
    dont_print = False
    query = f'SELECT c.courier_db_id, c.name, c.location, c.phone_number FROM couriers c LIMIT {ipl}'
    #print(f"display size = {disp_size}")
    #print(f"display size = {rows}")

    def create_spaces(string_to_space:str = "Some Default String", space_count:int = 30, just_return:int = None):
        if just_return:
            return_spaces = ""
            for _ in range(just_return):
                return_spaces += " "
            return(return_spaces)
        else:
            to_space = len(string_to_space)
            final_space_count = space_count - to_space 
            string_of_spaces = ""
            for x in range(final_space_count):
                string_of_spaces += " "
            return(string_of_spaces)

    while want_more_print: 
        #query = query
        result = get_from_db(query)
        if dont_print:
            pass
        else:
            print(f"Courier [ID/Name]{create_spaces(just_return=14)} Location{create_spaces(just_return=11)} Contact Number{create_spaces(just_return=6)}Active Orders{create_spaces(just_return=4)}All Orders {create_spaces(just_return=5)} Finalised Orders")
            print(f"{fm.print_dashes(return_it=True)} {create_spaces(just_return=8)} {fm.print_dashes(amount_of_dashes=5, return_it=True)} {create_spaces(just_return=6)} {fm.print_dashes(amount_of_dashes=5, return_it=True)} {create_spaces(just_return=6)} {fm.print_dashes(amount_of_dashes=4, return_it=True)} {create_spaces(just_return=5)} {fm.print_dashes(amount_of_dashes=4, return_it=True)} {create_spaces(just_return=5)} {fm.print_dashes(amount_of_dashes=6, return_it=True)}")
        for order_info in result:

            # where dont print none was btw
            
            live_ords = get_live_orders_for_courier(order_info[0] - 1)
            total_ords = get_total_orders_for_courier(order_info[0] - 1)
            comp_ords = get_completed_orders_for_courier(order_info[0] - 1)

            display1 = f"#{order_info[0]} - {order_info[1]}"
            display2 = f"{order_info[2]}"
            display3 = f"{order_info[3]}"
            display4 = f"{live_ords} Live"
            display5 = f"{total_ords} Total"
            spaces1 = create_spaces(display1, 29)
            spaces2 = create_spaces(display2, 18)
            spaces3 = create_spaces(display3, 17)
            spaces4 = create_spaces(display4, 13)
            spaces5 = create_spaces(display5, 13)

            if dont_print:
                pass
            else:
                print(f"{order_info[0]}. - {order_info[1]}  {spaces1} {order_info[2]} {spaces2} 0{order_info[3]} {spaces3} {live_ords} - Live {spaces4} {total_ords} - Total {spaces5} {comp_ords} - Done") 

        if dont_print:
            pass
        else:
            print(f"{fm.print_dashes(return_it=True)} {create_spaces(just_return=8)} {fm.print_dashes(amount_of_dashes=5, return_it=True)} {create_spaces(just_return=6)} {fm.print_dashes(amount_of_dashes=5, return_it=True)} {create_spaces(just_return=6)} {fm.print_dashes(amount_of_dashes=4, return_it=True)} {create_spaces(just_return=5)} {fm.print_dashes(amount_of_dashes=4, return_it=True)} {create_spaces(just_return=5)} {fm.print_dashes(amount_of_dashes=6, return_it=True)}")
        print("")    
        # print(pages_display)

        page_numbs = [f"{x+1}" for x in range(total_pages)]
        # print(f"current_page = {current_page}") 
        # print(f"page_numbs = {page_numbs}") 
        
        highlight_page = lambda h : f"[[ {h} ]]" if h == str(current_page) else f"[ {h} ]" # language is so mad wtf            
        print(*[highlight_page(p) for p in page_numbs])
        print("")   
        paginate_action = (input("Select Page Number Then Use 0 To Search By Courier : "))
        # print(current_page)
        # print(final_page)
        # print(paginate_action)
        fm.print_dashes()
        g = (int(paginate_action))
        if g > final_page:
            fm.format_display(disp_size)
            cour.return_one_line_art()
            current_page = int(paginate_action)
            dont_print = True
        elif paginate_action != "0":
            fm.format_display(disp_size)
            current_page = int(paginate_action)
            query = f'SELECT c.courier_db_id, c.name, c.location, c.phone_number FROM couriers c LIMIT {(current_page-1) * ipl}, {ipl}'
            dont_print = False
        else:      
            # could totally print again on 'exit' for courier number select but meh is fine for now
            fm.format_display(disp_size)
            query = f'SELECT c.courier_db_id, c.name, c.location, c.phone_number FROM couriers c LIMIT {(current_page-1) * ipl}, {ipl}'
            result = get_from_db(query)
            print(f"Courier [ID/Name]{create_spaces(just_return=14)} Location{create_spaces(just_return=11)} Contact Number{create_spaces(just_return=6)}Active Orders{create_spaces(just_return=4)}All Orders {create_spaces(just_return=5)} Finalised Orders")
            print(f"{fm.print_dashes(return_it=True)} {create_spaces(just_return=8)} {fm.print_dashes(amount_of_dashes=5, return_it=True)} {create_spaces(just_return=6)} {fm.print_dashes(amount_of_dashes=5, return_it=True)} {create_spaces(just_return=6)} {fm.print_dashes(amount_of_dashes=4, return_it=True)} {create_spaces(just_return=5)} {fm.print_dashes(amount_of_dashes=4, return_it=True)} {create_spaces(just_return=5)} {fm.print_dashes(amount_of_dashes=6, return_it=True)}")
            for order_info in result:
                live_ords = get_live_orders_for_courier(order_info[0] - 1)
                total_ords = get_total_orders_for_courier(order_info[0] - 1)
                comp_ords = get_completed_orders_for_courier(order_info[0] - 1)
                display1 = f"#{order_info[0]} - {order_info[1]}"
                display2 = f"{order_info[2]}"
                display3 = f"{order_info[3]}"
                display4 = f"{live_ords} Live"
                display5 = f"{total_ords} Total"
                spaces1 = create_spaces(display1, 29)
                spaces2 = create_spaces(display2, 18)
                spaces3 = create_spaces(display3, 17)
                spaces4 = create_spaces(display4, 13)
                spaces5 = create_spaces(display5, 13)
                print(f"{order_info[0]}. - {order_info[1]}  {spaces1} {order_info[2]} {spaces2} 0{order_info[3]} {spaces3} {live_ords} - Live {spaces4} {total_ords} - Total {spaces5} {comp_ords} - Done") 
            print(f"{fm.print_dashes(return_it=True)} {create_spaces(just_return=8)} {fm.print_dashes(amount_of_dashes=5, return_it=True)} {create_spaces(just_return=6)} {fm.print_dashes(amount_of_dashes=5, return_it=True)} {create_spaces(just_return=6)} {fm.print_dashes(amount_of_dashes=4, return_it=True)} {create_spaces(just_return=5)} {fm.print_dashes(amount_of_dashes=4, return_it=True)} {create_spaces(just_return=5)} {fm.print_dashes(amount_of_dashes=6, return_it=True)}")
            print("")
            want_more_print = False

 
def db_join_by_chosen_courier(disp_size=22, rows=3): # here right join will give you all the couriers even if they dont have an order which is kinda kewl
    Orders.items_per_list_print_couriers(disp_size, rows)
    fm.print_dashes()
    chosen_courier = int(input("Enter Courier Number To Search Their Orders : "))
    # confirm its in range here tbf
    query = f"SELECT o.customer_name, o.order_price, o.order_id, o.order_status, c.courier_db_id FROM orders o INNER JOIN couriers c ON o.courier_id = c.courier_db_id WHERE courier_db_id = {chosen_courier} ORDER BY c.courier_db_id"
    result = get_from_db(query)
    for a_result in result:
        print(a_result)
    fm.fake_input()


# NEW ################################################################################################################


def db_join_by_chosen_courier_then_status(disp_size=22, rows=3): # then guess could do if init display list too big just show live, then else show something else... (or just paginate from the start duh!)
    fm.format_display(disp_size)
    print(f"Some Title Info\n{fm.print_dashes(return_it=True)}\n")
    #Orders.items_per_list_print_couriers(disp_size, rows)
    #
    #
    db_print_courier_for_search(disp_size, rows)
    #
    #
    chosen_courier = int(input("Enter Courier Number To Search Their Orders : "))
     # confirm its in range here tbf
    fm.print_dashes()
    query = f"SELECT o.customer_name, o.order_price, o.order_id, o.order_status, c.courier_db_id FROM orders o INNER JOIN couriers c ON o.courier_id = c.courier_db_id WHERE c.courier_db_id = {chosen_courier} ORDER BY c.courier_db_id"
    go_again = True
    chosen_status = 0
    max_length_of_all_couriers_orders = len(get_from_db(query)) # if this is too long change the query and obvs ensure it links up properly throughout that page is changed n shit

    def create_spaces(string_to_space:str = "DFLT", space_count:int = 30, just_return:int = None):
        if just_return:
            return_spaces = ""
            for _ in range(just_return):
                return_spaces += " "
            return(return_spaces)
        else:
            to_space = len(string_to_space)
            final_space_count = space_count - to_space 
            string_of_spaces = ""
            for x in range(final_space_count):
                string_of_spaces += " "
            return(string_of_spaces)

    while go_again:
        fm.format_display(disp_size)
        if chosen_status == 9:
            query = f"SELECT o.customer_name, o.order_price, o.order_id, o.order_status, c.courier_db_id FROM orders o INNER JOIN couriers c ON o.courier_id = c.courier_db_id WHERE c.courier_db_id = {chosen_courier} ORDER BY c.courier_db_id"
        elif chosen_status != 0:
            query = f"SELECT o.customer_name, o.order_price, o.order_id, o.order_status, c.courier_db_id FROM orders o INNER JOIN couriers c ON o.courier_id = c.courier_db_id WHERE c.courier_db_id = {chosen_courier} AND o.order_status = {chosen_status} ORDER BY c.courier_db_id"
            #fm.format_display(disp_size)
        result = get_from_db(query)

        def print_full_key_with_caps_for_current():
            status_dict = {1:"preparing", 2:"delivering", 3:"delivered", 4:"recieved", 5:"cancelled", 6:"scheduling", 9:"all"}
            print(f"Order Status Key\n{fm.print_dashes(return_it=True)}")
            if_current_make_bold = lambda x,y : f" {x.upper()} <<" if y == chosen_status or y == 0 else x
            for num, status in status_dict.items():
                print(f"[ {num} ] {if_current_make_bold(status.title(), num)}")

        def status_num_to_word(statnum:int):
            status_dict = {1:"preparing", 2:"delivering", 3:"delivered", 4:"recieved", 5:"cancelled", 6:"scheduling", 0:"all", 9:"all"}
            rv = status_dict.get(statnum)
            return(rv.title())
        
        #print(chosen_status)
        print_full_key_with_caps_for_current()
        #print(f"Order Status Key\n{fm.print_dashes(return_it=True)}\n[ 1 ] Preparing\n[ 2 ] Out For Delivery\n[ 3 ] Delivered\n[ 4 ] Recieved\n[ 5 ] Cancelled\n[ 6 ] Scheduling\n[ 9 ] All")
        print("")
        print(f"{status_num_to_word(chosen_status)} Orders")       
        print(f"Courier #{chosen_courier} - {get_couriers_name_from_id(chosen_courier)}")   
        print("")    
        fm.print_dashes()
        for order_info in result:
            display1 = f"#{order_info[2]} - {order_info[0]}"
            display2 = f"{order_info[3]}"
            display3 = f"{order_info[1]}"
            spaces1 = create_spaces(display1, 29)
            spaces2 = create_spaces(display2, 18)
            spaces3 = create_spaces(display3, 17)
            print(f"{order_info[2]} - {order_info[0]} {spaces1} {order_info[3]} {spaces2} £{order_info[1]} {spaces3}")

        if len(result) <= max_length_of_all_couriers_orders - 1:
            the_diff_to_add_lines = (max_length_of_all_couriers_orders - len(result))
            if len(result) == 0:
                the_diff_to_add_lines -= 1
            for _ in range(the_diff_to_add_lines):
                print("-")
            #x = ["\n" for _ in range(the_diff_to_add_lines)] probs needs minus 1 too if you wanna do it    
            #print(*x)
                
        if len(result) == 0:
            print(return_one_line_art())

        fm.print_dashes()
        print("")

        #print("If You Would Like To See Orders For A Specific Order Status Please Enter The Order Code")
        chosen_status = int(input("Enter A Status Number To Filter By It, OR 9 To View All, OR 0 To Exit : ")) # will type error if not an int so do convert outside and then can work it with below if statement
        if chosen_status != 1 and chosen_status != 2 and chosen_status != 3 and chosen_status != 4 and chosen_status != 5 and chosen_status != 6 and chosen_status != 9 and chosen_status != 0: #make it 9?
            chosen_status = 9
        # confirm its in range here?
        if (chosen_status != 0):
            print("And Go Again") # lol remove this knobhead
        else:
            print("Well End Function Then")
            go_again = False
            break
    

#####################################################################################################################################




def db_print_search_by_status(disp_size=22, rows=3): # then guess could do if init display list too big just show live, then else show something else... (or just paginate from the start duh!)
    fm.format_display(disp_size)
    print(f"Some Title Info\n{fm.print_dashes(return_it=True)}\n")
    # chosen_courier = int(input("Enter Courier Number To Search Their Orders : "))
    # confirm its in range here tbf
    fm.print_dashes()
    query = f"SELECT o.customer_name, o.order_price, o.order_id, o.order_status, o.customer_address, c.courier_db_id FROM orders o INNER JOIN couriers c ON o.courier_id = c.courier_db_id ORDER BY c.courier_db_id"
    go_again = True
    chosen_status = 0
    max_length_of_all_couriers_orders = len(get_from_db(query)) # if this is too long change the query and obvs ensure it links up properly throughout that page is changed n shit

    def create_spaces(string_to_space:str = "DFLT", space_count:int = 30, just_return:int = None):
        if just_return:
            return_spaces = ""
            for _ in range(just_return):
                return_spaces += " "
            return(return_spaces)
        else:
            to_space = len(string_to_space)
            final_space_count = space_count - to_space 
            string_of_spaces = ""
            for x in range(final_space_count):
                string_of_spaces += " "
            return(string_of_spaces)

    while go_again:
        fm.format_display(disp_size)
        if chosen_status == 9:
            query = f"SELECT o.customer_name, o.order_price, o.order_id, o.order_status, o.customer_address, c.courier_db_id FROM orders o INNER JOIN couriers c ON o.courier_id = c.courier_db_id ORDER BY c.courier_db_id"
        elif chosen_status != 0:
            query = f"SELECT o.customer_name, o.order_price, o.order_id, o.order_status, o.customer_address, c.courier_db_id FROM orders o INNER JOIN couriers c ON o.courier_id = c.courier_db_id AND o.order_status = {chosen_status} ORDER BY c.courier_db_id"
            #fm.format_display(disp_size)
        result = get_from_db(query)

        def print_full_key_with_caps_for_current():
            status_dict = {1:"preparing", 2:"delivering", 3:"delivered", 4:"recieved", 5:"cancelled", 6:"scheduling", 9:"all"}
            print(f"Order Status Key\n{fm.print_dashes(return_it=True)}")

            if_current_make_bold = lambda x,y : f" {x.upper()} <<" if y == chosen_status or y == 0 else x

            for num, status in status_dict.items():
                if num == chosen_status:
                    print(f"{Fore.GREEN}[ {num} ] {if_current_make_bold(status.title(), num)}")
                else:
                    print(f"{Fore.LIGHTBLACK_EX}[ {num} ] {if_current_make_bold(status.title(), num)}")

        def status_num_to_word(statnum:int):
            status_dict = {1:"preparing", 2:"out for delivery", 3:"delivered", 4:"recieved", 5:"cancelled", 6:"scheduling", 0:"all", 9:"all"}
            rv = status_dict.get(statnum)
            return(rv.title())
        
        # would be nice to fix for very first display but meh is ok dw
        print_full_key_with_caps_for_current()
        #print(f"Order Status Key\n{fm.print_dashes(return_it=True)}\n[ 1 ] Preparing\n[ 2 ] Out For Delivery\n[ 3 ] Delivered\n[ 4 ] Recieved\n[ 5 ] Cancelled\n[ 6 ] Scheduling\n[ 9 ] All")
        print("")
        print(f"Order Status : {status_num_to_word(chosen_status)} Orders [ {chosen_status} ]")       
        fm.print_dashes()
        print("\nOrder Number & Customer         Customer Address         Order Cost     Current Status")
        print(f"{fm.print_dashes(amount_of_dashes=10, return_it=True)}          {fm.print_dashes(amount_of_dashes=8, return_it=True)}       {fm.print_dashes(amount_of_dashes=4, return_it=True)}     {fm.print_dashes(amount_of_dashes=4, return_it=True)}")

        for order_info in result:
            display1 = f"#{order_info[2]} - {order_info[0]}"
            display2 = f"{make_address_readable(order_info[4])}"
            display3 = f"{order_info[1]}"
            spaces1 = create_spaces(display1, 31)
            spaces2 = create_spaces(display2, 20)
            spaces3 = create_spaces(display3, 12)
            print(f"{order_info[2]} - {order_info[0]} {spaces1} -> {make_address_readable(order_info[4])} {spaces2} £{order_info[1]} {spaces3} {order_info[3]}")

        if len(result) <= max_length_of_all_couriers_orders - 1:
            the_diff_to_add_lines = (max_length_of_all_couriers_orders - len(result))
            if len(result) == 0:
                the_diff_to_add_lines -= 1
            for _ in range(the_diff_to_add_lines):
                print("-")
            #x = ["\n" for _ in range(the_diff_to_add_lines)] probs needs minus 1 too if you wanna do it    
            #print(*x)
                
        if len(result) == 0:
            print(return_one_line_art())

        fm.print_dashes()
        print("")

        #print("If You Would Like To See Orders For A Specific Order Status Please Enter The Order Code")
        chosen_status = int(input("Enter A Status Number To Filter By It, OR 9 To View All, OR 0 To Exit : ")) # will type error if not an int so do convert outside and then can work it with below if statement
        if chosen_status != 1 and chosen_status != 2 and chosen_status != 3 and chosen_status != 4 and chosen_status != 5 and chosen_status != 6 and chosen_status != 9 and chosen_status != 0: #make it 9?
            chosen_status = 9
        # confirm its in range here?
        if (chosen_status != 0):
            print("And Go Again") # lol remove this knobhead
        else:
            print("Well End Function Then")
            go_again = False
            break
    




#####################################################################################################################################


def db_join_by_courier_only_live_orders(): # here right join will give you all the couriers even if they dont have an order which is kinda kewl
    query = f"SELECT o.customer_name, o.order_price, o.order_id, o.order_status, c.name, c.courier_db_id FROM orders o INNER JOIN couriers c ON o.courier_id = c.courier_db_id WHERE o.order_status = 1 OR o.order_status = 2 ORDER BY c.courier_db_id"
    #ORDER BY...
    result = get_from_db(query)
    for a_result in result:
        print(a_result)
    fm.fake_input()


def get_live_orders_for_courier(chosen_courier:int):
    chosen_courier += 1
    query = f"SELECT o.order_status FROM orders o INNER JOIN couriers c ON o.courier_id = c.courier_db_id WHERE c.courier_db_id = {chosen_courier} AND (o.order_status = 1 OR o.order_status = 2) ORDER BY c.courier_db_id"
    result = get_from_db(query)
    return(len(result))

    # OBVS JUST QUICKLY DO ONLY LIVE ORDERS FOR ALL COURIERS WILL BE EASY AF
    # SOME FORMAT ISSUES AND WANT TO DISPLAY THE STATUS PROPERLY (tbf idk how it displays rn lol)
    # THEN STRAIGHT AFTER DO ONLY LIVE ORDERS, THEN CONT - or option to input the code and it shows you for the code only ooo



## CREATE NEW ORDER FUNCTIONS ##############################################################################################################################################


def create_new_order(disp_size, rows): 
    """Create new order by calling appropriate functions (for vaildation) then creating new instance with the validated inputs"""
    lets_continue = True
    fm.format_display(disp_size)
    while lets_continue:
        # GET NAME
        name = get_name(disp_size, True)
        if name == "0":
            print("Escape Key Logged")
            lets_continue = False
            
        # GET NUMBER
        if lets_continue:
            phone_number = get_mobile(disp_size, name)
            if phone_number == "0":
                print("Escape Key Logged")
                lets_continue = False

        # GET ADDRESS
        if lets_continue:
            customer_address = get_address(disp_size, name, phone_number)
            if customer_address == "0":
                print("Escape Key Logged")
                lets_continue = False

        # GET PRODUCTS FOR ORDER, UPDATE QUANTITIES, & GET FINAL PRICE
        if lets_continue:
            order_prdcts, order_cost = get_and_add_products(disp_size, rows)
            if order_cost == "0":
                print("Escape Key Logged")
                lets_continue = False

        # GET COURIER
        if lets_continue:
            attached_courier = get_couriers_from_list_and_attach(disp_size, rows, name, phone_number, customer_address)
            if attached_courier == "0":
                print("Escape Key Logged")
                lets_continue = False

        # GET ORDER STATUS
        if lets_continue:
            order_status = add_order_status(None)
            if order_status == "0":
                print("Escape Key Logged")
                lets_continue = False
            else:
                break
            
    else:
        fm.print_dashes()
        print("Order Cancelled")
        fm.fake_input()
        return(False) # escape key logged, order cancelled, dont allow quick create by returning false (false - order not made)
    fm.print_dashes()
    # MAKE THE ORDER
    Orders(name, customer_address, phone_number, order_status, order_cost, None, attached_courier, order_prdcts)
    ord_uwuid = Orders.orders_list[-1].order_id
    # some kinda confirm before adding it to the db - like try except for the class init method or sumnt maybe idk?
    add_new_order_to_db(name, customer_address, phone_number, order_status, order_cost, ord_uwuid, attached_courier, order_prdcts)
    fm.format_display(disp_size)
    
    print(f"{Fore.GREEN}This Was A Triumph! - Order Made")
    fm.print_dashes()
    print(f"ORDER CONFIRMED")
    fm.print_dashes()
    print(f"Order ID (for your records) : {ord_uwuid}") #else use get attr
    fm.print_dashes()
    print(f"You've Successfully Been Charged {Fore.GREEN}£{order_cost}")
    fm.print_dashes()
    fm.fake_input()
    return(True) # if made new (true - order made succesfully)


def add_new_order_to_db(customer_name:str, customer_address:str, customer_phone:str, order_status:str, order_price:float, order_id:int, courier_id:int, products_ids:str):
    print(products_ids)
    query = f'INSERT INTO orders (customer_name, customer_address, customer_phone, order_status, order_price, order_uuid, courier_id, products_ids) VALUES ("{customer_name}","{customer_address}","{customer_phone}","{order_status}",{order_price},{order_id},{courier_id},"{products_ids}")'
    add_to_db(query)


def get_name(disp_size, first_run = False):  # v2 validation = needs try except to be acceptable
    """Get and return name of courier with simple regex validation, not used for update but should refactor for this?"""
    invalid_name = True
    # name_is_good = lambda x : re.match(r"[A-Za-z]{2,25}|\s|\.|[a-zA-Z]|[A-Za-z]{1,25}\w$", x) # actually wrote this myself so do think it works but also i mean fuck knows \D[a-zA-Z]+($\s{1}|.)
    while invalid_name:
        fm.format_display(disp_size)
        if first_run: print(f"Create New Order\n{fm.print_dashes(return_it=True)}\n")
        name = input("Enter Name (need to redo regex validation) : ")
        if name == "0":
            break
        elif len(name) >= 3:          # name_is_good(name):
            print(f"Name [{name}] Validated")
            break
        else:
            print("Try Again")
    return(name)


def get_mobile(disp_size, name:str = None): # v2 validation = needs try except to be acceptable
    invalid_mob = True
    mob_is_good = lambda x : re.match(r"^(07\d{8,12}|447\d{7,11})$", x) # lambda lets us keep expression outside of loop, allows 07 start or 447 start but not +
    while invalid_mob:
        fm.format_display(disp_size, True)
        if name: # not equal to none?
            print(f"Name : {name}\n{fm.print_dashes(return_it=True)}\n") # else print dashes?
        num = input("Enter Valid UK Mobile Number (no + symbol) : ")
        if num == "0":
            break
        elif len(num) > 1: #mob_is_good(num): (put it back, is just too long when testing frequently)
            print("Number Validated")
            break
        else:
            print("Try Again")
    return(num)


def get_address(disp_size, name=None, phone_number=None):  # v2 validation = needs try except to be acceptable
    """Get and return name of courier with simple regex validation, not used for update but should refactor for this?"""
    # COULD LEGIT DO IF ADDRESS CONTAINS VALID LOCATION ONLY SHOW VALID COURIERS, ELSE SHOW ALL
    invalid_addy = True
    # name_is_good = lambda x : re.match(r"[A-Za-z]{2,25}|\s|\.|[a-zA-Z]|[A-Za-z]{1,25}\w$", x) 
    while invalid_addy:
        fm.format_display(disp_size)
        if name is not None and phone_number is not None: # when comparing to None always use comparison not equality 
            print(f"{fm.print_dashes(return_it=True)}\nName : {name}\nMobile : {phone_number}\n{fm.print_dashes(return_it=True)}\n")
        address = input("Enter Address : ")
        if address == "0":
            break
        elif len(address) >= 5:          # name_is_good(name):
            print(f"[{address}] Validated")
            break
        else:
            print("Try Again")
    return(address)


def get_couriers_from_list_and_attach(disp_size, rows, name=None, phone_number=None, customer_address=None): # if take locations can create new function to update them (add/remove/rename), v3 validation = acceptable
    # print the couriers list, to improve obvs
    fm.format_display(disp_size)
    
    # main functionality
    not_cancelled = True
    while not_cancelled:

        # if name and phone_number and customer_address: (should work the same, test it)
        if name is not None and phone_number is not None and customer_address is not None: # when comparing to None always use comparison not equality 
            print(f"{fm.print_dashes(return_it=True)}\nName : {name}\nMobile : {phone_number}\nAddress : {customer_address}\n{fm.print_dashes(return_it=True)}\n") #might remove here 
        Orders.items_per_list_print_couriers(disp_size, rows)
        print("")
        try:
            user_input = int(input("Enter Your Selection : "))
        except ValueError:
            wrong_val = True

        if user_input > len(cour.Couriers.couriers_list) or user_input < 0: # error cases
            if wrong_val:
                print("Try Again - Wrong Value\n")
            else:
                print("Try Again - Wrong Selection\n")
        elif user_input == 0: # escape key, its already been int converted btw
            print("Uhhhh... I HATE zer0s") #... but you are zeros tho
            break
        else:
            fm.format_display(disp_size)
            fm.print_dashes()
            cr = cour.Couriers.couriers_list[user_input - 1]    
            print(f"You Selected Courier - {cr.name}, (ID : {cr.courier_id})")
            fm.print_dashes()
            print("Assigning This Courier To The Order Now") 
            break
    # END WHILE
    if user_input == 0:
        return ("0")
    else:
        return(user_input) #is an int
   

def get_and_add_products(disp_size, rows, basket_total:float = 0.0, order_basket:list = []):
    got_more = True
    while got_more:
        prdct.Product.paginated_print(prdct.Product, disp_size, rows, "Enter Page (step with .), To Select A Product First Hit '0' : ","Choose A Product To Add To The Order")
        product_to_add = int(input("Enter Product Number To Add It To The Order : "))
        prod = prdct.Product.products_list[product_to_add - 1]
        prod_price = getattr(prod, "price_gbp")
        prod_name = getattr(prod, "name")
        prod_numb = getattr(prod, "product_number")
        prod_quant = getattr(prod, "quantity")
        if int(prod_quant) == 0:
            print("Try Again - Reloop!") # TO DO THIS, is easy af ffs just cba
        else:
            fm.format_display(disp_size)
            print(f"Sure You Want To Add [{prod_numb}] - {prod_name} To The Order?\nPrice = £{prod_price}")
            print("Commit Confirm - assuming yes")
            fm.print_dashes()
            print("Ok how many?")
            quant_is_good = True # DUH SHIT LIKE THIS AS FUNCTION!!!
            while quant_is_good:
                how_many = int(input(f"Enter Amount ({prod_quant} available) : ")) 
                if how_many > prod_quant:
                    print("Something Doesn't Quite Add Up... Try Again")
                    fm.fake_input()
                    break     
                order_basket = product_basket(prod_numb, prod_name, prod_price, how_many, order_basket)
                total_basket_quant = 0
                for order in order_basket:
                    total_basket_quant += order[3]
                print(f"Order Basket = {order_basket}")
                basket_total += order_basket[-1][2] #last item added, the final price (multiplied by wanted quantity)
                fm.format_display(disp_size)
                print(f"Current Basket\n{fm.print_dashes(return_it=True)}")
                print(f"Price : £{basket_total:.2f}")
                print(f"Items : {total_basket_quant} total") # should really use the sum/count of how_many instead of len basket div 5 but meh
                fm.print_dashes()
                for product in order_basket:
                    print(f"{product[3]}x {product[1]}(#{product[0]}) @ £{(product[2] / product[3]):.2f} each - [£{product[2]} total]")
                # commit confirm
                fm.print_dashes()
                yesno = fm.get_user_yes_true_or_no_false(before_text=f"Want To Add More Items\n{fm.print_dashes(return_it=True)}\n", yes="Order More",no="I'm Done - Start Checkout")
                fm.fake_input() # DELETE THIS RIGHT?!?!?!!?
                if yesno == False:
                    got_more = False
                    break
                break
    # NESTED FUNCTION            
    def display_updated_basket(order_basket, original_order_basket):
        print(f"Looks Like Some Items Sold Out!\nWe've Updated Your Basket\nPlease Reconfirm Your Order\n{fm.print_dashes()}\nUpdated Basket\n{fm.print_dashes()}") # THIS WILL BE THE NEW UPDATED FINAL DISPLAY
        for product in order_basket:
            print(f"{product[3]}x {product[1]}(#{product[0]}) @ £{(product[2] / product[3]):.2f} each - [£{product[2]} total]")
    # END NESTED FUNCTION   
    print("Ok finalising your basket...")
    final_products_list = []
    original_order_basket = order_basket
    order_basket = update_quants_from_basket(order_basket)
    final_products_quants_list = []
    if order_basket is None:
        #print("order basket is none")
        order_basket = original_order_basket
        #print(f"replacing basket = {original_order_basket}")
        #print(f"order basket is now = {order_basket}")
    else:
        display_updated_basket(order_basket, original_order_basket) #display updated basket and confirm function
    for item_info in order_basket:
        final_products_list.append(item_info[0]) # FOR STRICT GENERATION PROJECT
        final_products_quants_list.append((item_info[0],item_info[3])) # NEW! -> TO RETURN 
    print(f"Final Basket Total\n{fm.print_dashes(return_it=True)}")
    new_basket_total = 0
    for product in order_basket:
        new_basket_total += product[2]
    basket_total = new_basket_total
    #print(f"The Item Numbers Being Sent Are = {final_products_quants_list}")
    if basket_total >= 12.99:    
        print(f"£{basket_total:.2f}")
        fm.print_dashes()
        print("COMMIT CONFIRM?")
        fm.fake_input()
        return(final_products_quants_list, basket_total) 
    else:
        print("Your Basket Is Under £12.99")
        fm.print_dashes()
        print(f"£{basket_total:.2f}")
        fm.print_dashes()
        print("So We're Adding A £2.99 Delivery Charge")
        fm.print_dashes()
        print(f"[ 1 ] Accept\n[ 2 ] Cancel\n[ 3 ] Order More\n{fm.print_dashes(return_it=True)}")  #(loop back to readd would be nice but urgh - maybe back out then back in but wouldnt save ur orders but meh)
        y_n_or_more = input("Enter Your Selection : ")
        
        if y_n_or_more == "1": # ACCEPT
            fm.format_display(disp_size)
            fm.print_dashes()
            print("Delivery Charge Added")
            print("Basket Updated")
            fm.print_dashes()
            basket_total += 2.99
            print("")
            fm.print_dashes()
            print(f"{Fore.GREEN}£{basket_total:.2f}")
            fm.print_dashes()
            print("")
            print("\(‾▿‾\) (/‾▿‾)/")
            print("")
            #print("Your Order Has Been Confirmed")
            print(final_products_quants_list)
            fm.fake_input()
            return(final_products_quants_list, basket_total)  # THE ACTUAL FUCK THO, MAYBE JUST RETURN ONE TUPLE OR LIST AND UNPACK THE VALUES THEN BUT IT WAS WORKING BEFORE SO WTF MAN!!!! AND IT FUCKING WORKS WITH ONE WHAT THE FUCKKKKKKKK
        elif y_n_or_more == "2": # CANCEL
            fm.print_dashes()
            print("Sorry It Had To End Like This")
            print("")
            print("(・_・;)")
            print("")
            fm.print_dashes()
            fm.fake_input()
            return("0", "0") 
        else: # ORDER MORE - so loop back
            get_and_add_products(disp_size, rows, basket_total) 
        # aite so believe this will work just sending them back here to the same function
        # but that isn't going to save your basket or the cost of your basket
        # but since we initialise those vars at the start defo is a work around
    

        
   

def product_basket(item_num_to_add:int, item_name_to_add:str, item_price_to_add:float, how_many:int, basket_list=None):
    if basket_list is None:
        basket_list = []
    final_price_to_add = item_price_to_add * how_many  # *= duh
    basket_list.append([item_num_to_add, item_name_to_add, final_price_to_add, how_many])
    print(f"Current Basket = {basket_list}")
    return(basket_list)


def update_quants_from_basket(order_basket):
    made_updates = False
    for i, item in enumerate(order_basket):
        how_many = int(order_basket[i][3]) # might be unnecessary to force conversion here
        final_quant = (prdct.Product.products_list[item[0]-1].quantity)-(how_many)
        if final_quant < 0:
            #print(f"Uh Oh, Looks Like We Need To {0 - final_quant} From {prdct.Product.products_list[item[0]-1].name}")  
            #print(f"Updating User Basket - {order_basket}")
            #print(f"Updating Item Total - {order_basket[i][3]} + {final_quant}")
            order_basket[i][3] + final_quant
            made_updates = True   
            order_basket.pop(i) 
            # if ok then commit the change and return the order (ONLY RETURN IF VALID THEN COULD CHECK IF IS NONE ON RETURN - ACTUALLY YES AS WANT TO CONFIRM ANY UPDATES WITH THE USER)
        if made_updates == False:
            prdct.Product.products_list[item[0]-1].quantity -= how_many
        #print(f"Updated Quantity = {prdct.Product.products_list[item[0]-1].quantity}")
    if made_updates:
        #print("Made Updates")
        return(order_basket) # new and necessary - must return as may update it now 
    else:
        return(None)


    # test
    # then print orders to make sure is working as expected, print via class btw!
    # then 
    # natty lang and rich lib
    # and remaining functions/functionality
    # then new server stuff
    # also new web scrape betting project idea


def add_order_status(the_code = None):
    '''adds order code as status to an order'''
    print_string = ["[ 1 ] = Preparing", "[ 2 ] = Out For Delivery", "[ 3 ] = Delivered", "[ 4 ] = Recieved", "[ 5 ] = Cancelled", "[ 6 ] = Scheduling"]
    if the_code == None: # for update not add
        print("Choose Status To Set To Order") # want order number? could be done easily enough
        fm.print_dashes()
        print(*print_string, sep="\n") # print("[ 7 ] = Custom Code")  #not doing (rn anyways) but could 
        fm.print_dashes()
        user_code = int(input("Choose A Code For The Order : "))
    else:
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
    elif user_code == 0:
        return("0") # escape key (tho when adding to db with no enum the status will be set to 0 which means error (which totally works tbf))
    else:
        return("Error") # guna return error for debugging but ig should return preparing as default


## MAIN MENU ############################################################################################################################################################


def main_orders(rows=3, disp_size=22):
    #disp_size = 20
    #rows = 3
    add_spaces = lambda x : x # take each line and add spaces appropriately should be easy might need full def tho
    menu_string = [f"ORDERS v3.01\n(using object oriented principles)\n{fm.print_dashes(return_it=True)}\n","[ 1 ] Create New", "[ 2 ] Print SubMenu", "[ 3 ] Format Display", "[ - ] -", "[ - ] -", "[ - ] -", "[ - ] -", "[ - ] -", "[ - ] -", "[ S ] -", "[ L ] -", "[ 0 ] Main Menu\n","- - - - - - - - - - -"]
    user_menu_input = 1
    print_again = True
    while user_menu_input != "0":
        if print_again: # for quick menu, returns the user to their place in this switch statement without printing the menu again
            # print menu, get user input
            fm.format_display(disp_size)
            print(*menu_string, sep="\n")
            user_menu_input = input("Enter Menu Selection : ")

    # [1] CREATE NEW ORDER
        if user_menu_input == "1":
            print("Create New Order")
            if create_new_order(disp_size, rows):
                # QUICK MENU / CREATE AGAIN
                print("Quick Create New Order?\n") #from a ux perspective would be un-needed here, but for testing and general use its helpful so including
                if fm.get_user_yes_true_or_no_false():
                    print_again = False
                    user_menu_input = "1"
                else:
                    print_again = True
                
    # [2] PRINT SUBMENU
        if user_menu_input == "2":
            print("Print SubMenu")
            print_sub_menu(disp_size, rows)

     # [3] FORMAT SCREEEN
        elif user_menu_input == "3":
            disp_size = format_screen(disp_size)
            fm.fake_input()
    
    return(rows, disp_size)


def print_sub_menu(disp_size, rows):
    menu_string = [f"ORDERS v3.01\n(using object oriented principles)\n{fm.print_dashes(return_it=True)}\n","[ 1 ] Print Orders List [DB, Paginated, Only Valid]", "[ 2 ] Print Orders By Courier [DB, Paginated, Inc None]", "[ 3 ] Search Orders By Courier [DB, Paginated, Only Valid]", "[ 4 ] Search Orders By Status [DB, Only Valid]", "[ 0 ] Back To Orders Menu\n","- - - - - - - - - - -"]
    user_menu_input = 1
    while user_menu_input != "0":
        fm.format_display(disp_size)
        print(*menu_string, sep="\n")
        user_menu_input = input("Enter Menu Selection : ")
            
        if user_menu_input == "1": # changed from if to elif, shouldnt cause problems, but commenting just incase
            db_print_orders(disp_size, rows)
            fm.fake_input()

        elif user_menu_input == "2":
            db_print_orders_for_every_courier(disp_size, rows)

        elif user_menu_input == "3":
            db_join_by_chosen_courier_then_status(disp_size, rows) #db_print_courier_for_search(disp_size, rows)

        elif user_menu_input == "4":
            db_print_search_by_status(disp_size, rows) #db_join_by_chosen_courier(disp_size, rows)


def format_screen(disp_size:int): 
    user_submenu_input = "1"
    while user_submenu_input != "0":
        hl_curr_disp = lambda x : f"{x}" if x != disp_size else f"{Fore.GREEN}{x} << CURRENT DISPLAY SIZE"
        print(*[hl_curr_disp(x+9) for x in reversed(range(45))], sep="\n")
        print(f"Current Display Size = {disp_size} < ENSURE THESE MATCH!  -> Tip! use 0 to reset the display)") 
        print("Recommended Display Size = 29+")
        print("Recommended Minimum Display Size = 16") ## 16 gets 30 items comfortably (per line) without overlap or need for pagination so start here (15 had mad overlap)
        fm.print_dashes()
        print("Adjust The Display Then Enter [ 0 ] To Reset The Display Counter To See The Numbers")
        print("The Very Top Number Will Be Your Display Size")
        fm.print_dashes()
        new_disp_size = int(input("Enter The Number For The Screen Size You Want : "))
        if new_disp_size > 0: # should make this be greater than the acceptable size but whatever
            print(f"New Screen Size = {new_disp_size}")
            return(new_disp_size)

        else:
            user_submenu_input = "1"

def set_display_rows(rows: int):
    # to improve that just make the amount of spaces dynamic and trim the end of long strings to fit uniformly
    # N0TE! - should trim the end of long strings anyway btw!
    fm.format_display()
    print("Choose How Many Columns To Display In Menus (1 - 3)")
    print(f"Max Columns = 3, Recommended Columns = 3, Current = {rows})") # used to be 5 until price etc so updating for those changes tho no really tested, hardly worth it
    rows = int(input("Enter A Number Between 1 and 3 : "))
    return(rows)


# can also use this for excepts/errors tbf lol
def return_one_line_art():
    one_line_ascii_art_list = ["̿' ̿'\̵͇̿̿\з=(◕_◕)=ε/̵͇̿̿/'̿'̿ ̿  NOBODY MOVE!","( ͡° ͜ʖ ͡°) *STARING INTENSIFIES*","(╯°□°)--︻╦╤─ - - - WATCH OUT HE'S GOT A GUN","(⌐■_■)--︻╦╤─ - - - GET DOWN MR PRESIDENT","┻━┻︵  \(°□°)/ ︵ ┻━┻ FLIPPIN DEM TABLES","(ノಠ益ಠ)ノ彡︵ ┻━┻︵ ┻━┻ NO TABLE IS SAFE","ʕつಠᴥಠʔつ ︵ ┻━┻ HIDE YO KIDS HIDE YO TABLES","(ಠ_ಠ)┌∩┐ BYE BISH","(ง •̀_•́)ง FIGHT ME FOKER!","[¬º-°]¬  [¬º-°]¬ ZOMBIES RUN!","(╭ರ_•́) CURIOUSER AND CURIOUSER","つ ◕_◕ ༽つ つ ◕_◕ ༽つ TAKE MY ENERGY","༼つಠ益ಠ༽つ ─=≡ΣO)) HADOUKEN!"]
    return(one_line_ascii_art_list[random.randint(0, len(one_line_ascii_art_list)-1)])
        

if __name__ == "__main__":
    main_orders()





#### SPEC
#
#
# 1 - PRINT ORDERS
# 2 - CREATE NEW ORDER [COMPLETE]