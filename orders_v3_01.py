import format_random_v2_00 as fm
import re
import couriers_v3_01 as cour
import products_v1_02 as prdct

import pymysql
import os
from dotenv import load_dotenv

## END IMPORTS


# Load environment variables from .env file
load_dotenv()
host = os.environ.get("mysql_host")
user = os.environ.get("mysql_user")
password = os.environ.get("mysql_pass")
database = os.environ.get("mysql_db")

# Establish a database connection
connection = pymysql.connect(
    host,
    user,
    password,
    database
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
    # print(an_address)
    ndx = an_address.find(",")
    new_addy = an_address[:ndx]
    return(new_addy)

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
            print(f"Customer {create_spaces(just_return=22)} Order Status{create_spaces(just_return=24)} Order Delivery{create_spaces(just_return=35)} Customer Contact{create_spaces(just_return=9)}For Restaurant (product number, quantity)")
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
                print(f"[ {order_info[0]} ] {order_info[1]} {spaces1} £{order_info[5]} [PAID] - {order_info[4]} {spaces2} {get_couriers_name_from_id(order_info[7])} -> to {make_address_readable(order_info[2])} {spaces3} {order_info[3]} {spaces4} {order_info[8]}") # {order_info[8]}

        if dont_print:
            pass
        else:
            print(f"{fm.print_dashes(return_it=True)} {create_spaces(just_return=8)} {fm.print_dashes(return_it=True)} {create_spaces(just_return=13)} {fm.print_dashes(return_it=True)} {create_spaces(just_return=26)} {fm.print_dashes(amount_of_dashes=7, return_it=True)}{create_spaces(just_return=8)} {fm.print_dashes(return_it=True)}")
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
            query = f'SELECT * FROM orders WHERE order_id > {(current_page - 1) * ipl} LIMIT {ipl}'
            dont_print = False
        else:
            #fm.format_display(disp_size)
            print("Ok Bye")
            want_more_print = False


def db_join_by_courier(): # here right join will give you all the couriers even if they dont have an order which is kinda kewl
    print("Printing All Couriers Orders (Even If None)")
    fm.fake_input()
    query = f"SELECT o.customer_name, o.order_price, o.order_id, o.order_status, c.name, c.courier_db_id FROM orders o RIGHT JOIN couriers c ON o.courier_id = c.courier_db_id ORDER BY c.courier_db_id"
    #ORDER BY...
    result = get_from_db(query)
    for a_result in result:
        print(a_result)
    fm.fake_input()


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


def db_join_by_chosen_courier_then_status(disp_size=22, rows=3): # here right join will give you all the couriers even if they dont have an order which is kinda kewl
    fm.format_display(disp_size)
    print(f"Some Title Info\n{fm.print_dashes(return_it=True)}\n")
    Orders.items_per_list_print_couriers(disp_size, rows)
    #
    #
    #
    #
    #
    #
    # JUST CALL THE OTHER ONE THATS BETTER & PAGINATED DUH, JUST PARAMETER FOR FINAL FORMATTING (is a bit excess but meh)
    # - OR MAYBE IT CALLS THE PAGINATED BASED ON LEN OOO
    #
    #
    #
    #
    #
    #
    chosen_courier = int(input("Enter Courier Number To Search Their Orders : "))
    # confirm its in range here tbf
    fm.print_dashes()
    print("By Default You Will See Only Live Orders (Preparing/Out For Delivery)")
    print("If You Would Like To See Orders For A Specific Order Status Please Enter The Order Code")
    print("Or Enter 0 For Default Settings")
    fm.print_dashes()
    chosen_status = int(input("Enter A Valid Status Number or 0 To Continue : "))
    # confirm its in range here?
    if (chosen_status != 3 and chosen_status != 4 and chosen_status != 5 and chosen_status != 6): # if chosen_status not in valid_status_list (e.g. [3,4,5,6])
        query = f"SELECT o.customer_name, o.order_price, o.order_id, o.order_status, c.courier_db_id FROM orders o INNER JOIN couriers c ON o.courier_id = c.courier_db_id WHERE c.courier_db_id = {chosen_courier} AND (o.order_status = 1 OR o.order_status = 2) ORDER BY c.courier_db_id"
    else:
        query = f"SELECT o.customer_name, o.order_price, o.order_id, o.order_status, c.courier_db_id FROM orders o INNER JOIN couriers c ON o.courier_id = c.courier_db_id WHERE c.courier_db_id = {chosen_courier} AND o.order_status = {chosen_status} ORDER BY c.courier_db_id"
    
    result = get_from_db(query)
    for a_result in result:
        print(a_result)
    fm.fake_input()


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
    print(f"Order ID (for your records) : {ord_uwuid}") #else use get attr
    # some kinda confirm before adding it to the db - like try except for the class init method or sumnt maybe idk?
    add_new_order_to_db(name, customer_address, phone_number, order_status, order_cost, ord_uwuid, attached_courier, order_prdcts)
    print("This Was A Triumph! - Order Made")
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
   

def get_and_add_products(disp_size, rows):
    basket_total = 0.0 
    order_basket = [] 
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
                fm.fake_input()
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
    print(f"£{basket_total:.2f}")
    fm.print_dashes()
    #
    #
    #
    # IF BASKET < 10, ADD 3.99 DELIVERY CHARGE, CONFIRM WITH USER (can skip confirm and just tell them tbf)
    #
    #
    #
    print("COMMIT CONFIRM?")
    fm.fake_input()
    return(final_products_quants_list, basket_total) 
   

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


def main_orders(): #rows=3, disp_size=22
    disp_size = 20
    rows = 3
    menu_string = [f"ORDERS v3.01\n(using object oriented principles)\n{fm.print_dashes(return_it=True)}\n","[ 1 ] Create New", "[ 2 ] Print Orders From DB", "[ 3 ] Print Join Cour X Ord From DB (alpha)", "[ 4 ] Print Join Cour X Ord From DB, Search By Courier ID", "[ 5 ] ... Then Status", "[ 6 ] Only Live Orders", "[ - ] -", "[ - ] -", "[ S ] -", "[ L ] -", "[ 0 ] Main Menu\n","- - - - - - - - - - -"]
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

        if user_menu_input == "2":
            db_print_orders(disp_size, rows)
            fm.fake_input()

        if user_menu_input == "3":
            db_join_by_courier()

        if user_menu_input == "4":
            db_join_by_chosen_courier(disp_size, rows)
        
        if user_menu_input == "5":
            db_join_by_chosen_courier_then_status(disp_size, rows)

        if user_menu_input == "6":
            db_join_by_courier_only_live_orders()
        
        ## REMOVE BELOW STUFF PLS
        
        if user_menu_input == "9":
            print(*(cour.Couriers.generate_index_name_string(cour.Couriers)), sep="\n") 
            fm.fake_input()


if __name__ == "__main__":
    main_orders()





#### SPEC
#
#
# 1 - PRINT ORDERS
# 2 - CREATE NEW ORDER [COMPLETE]