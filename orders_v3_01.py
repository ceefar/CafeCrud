import format_random_v2_00 as fm
import re
import csv
import couriers_v3_01 as cour
import products_v1_02 as prdct

## END IMPORTS

# CLASSES ##################################################################################################################################################################
# COURIERS CLASS #################################


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
                current_string = (f"{index} {cour.Couriers.couriers_list[index].name}")
                spaces = 30 - (len(current_string))
                spaces_string = ""
                if int(index) + 1 == 10:
                    spaces -= 1
                for x in range(spaces):
                    spaces_string += " "
                cr = cour.Couriers.couriers_list[index]    
                print_string += (f"[ {int(index) + 1} ] {cr.name} - {cr.location} {spaces_string}")
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

            if one_or_two == "1": # SEARCH - PROBS NEEDS GET ATTR UPDATE WHICH IS FINE
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
    print("This Was A Triumph! - Order Made")
    fm.fake_input()
    return(True) # if made new (true - order made succesfully)


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
        return("0") # escape key
    else:
        return("Error") # guna return error for debugging but ig should return preparing as default


## MAIN MENU ############################################################################################################################################################


def main_orders(): #rows=3, disp_size=22
    disp_size = 20
    rows = 3
    menu_string = [f"ORDERS v3.01\n(using object oriented principles)\n{fm.print_dashes(return_it=True)}\n","[ 1 ] Create New", "[ 2 ] Print All Orders v1", "[ - ] -", "[ - ] -", "[ - ] -", "[ - ] -", "[ - ] -", "[ - ] -", "[ S ] -", "[ L ] -", "[ 0 ] Main Menu\n","- - - - - - - - - - -"]
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
            Orders.print_orders(Orders)
            fm.fake_input()

        if user_menu_input == "3":
            print(*(cour.Couriers.generate_index_name_string(cour.Couriers)), sep="\n")
            fm.fake_input()


if __name__ == "__main__":
    main_orders()






