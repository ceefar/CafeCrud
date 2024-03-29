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
    def __init__(self, customer_name:str, customer_address:str, customer_phone:str, order_status:int, order_price:float, order_id:int, courier_id:int = None, products_ids:list = []): 
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
            print(f"#{self.order_id} {self.customer_name} - {self.customer_phone} - {self.order_status} {courier_id} Loaded") # TO ADD A BOOL PARAM FOR SHOWING THIS PRINT STATEMENT?
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
            print(f"#{self.order_id} - {self.customer_name} - {self.customer_phone} - {self.order_status} {courier_id} Created") # TO ADD A BOOL PARAM FOR SHOWING THIS PRINT STATEMENT?  
        #END IF
    #END INIT    


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


''' FOR THE GET_ATTR WAY

        for i, courier in enumerate(cour.Couriers.couriers_list):
            x = getattr(courier, "name")
            z = getattr(courier, "location")
            # BRUHHH THEN CAN ZIP WITH ORDERS INFO NAH DONT NEED TO ZIP JUST CHECK AGAINST AND GET THE INFO HERE, WELL HAVE A FUNCTION CALL TO DO THAT NOT IN LOOP BUT BOSH!
            print(f"[ {i} ] - {x}, Location - {z}")
'''


# customer name, address, phone
# courier number (index or id idc)
# product - items (product ids)
# order - status, price



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

        # GET COURIER
        if lets_continue:
            attached_courier = get_couriers_from_list_and_attach(disp_size, rows, name, phone_number, customer_address)
            if attached_courier == "0":
                print("Escape Key Logged")
                lets_continue = False

        # GET PRODUCTS FOR ORDER, UPDATE QUANTITIES, & GET FINAL PRICE
        if lets_continue:
            order_prdcts, order_cost = get_and_add_products(disp_size, rows)
            if order_cost == "0":
                print("Escape Key Logged")
                lets_continue = False
            else:
                break
            
    #location = get_location_from_list(disp_size, name, phone_number)
    #Couriers(name.strip(), str(phone_number), str(location))
    #fm.format_display()
    #get_zeros = lambda x : "0"*(4 - len(str(x)))
    #cr = Couriers.couriers_list[-1] # the instances's address in memory
    #print(f"{cr.name.title()} - Created Sucessfully\n{fm.print_dashes(return_it=True)}\nCourier #{get_zeros(cr.courier_id)}{cr.courier_id}\nLocation : {cr.location}\nMobile : {cr.phone_number}")
    
    else:
        fm.print_dashes()
        print("Order Cancelled")
        fm.fake_input()
        return(False) # escape key logged, order cancelled, dont allow quick create by returning false (false - order not made)
    fm.print_dashes()
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
                    
            # got more moved     
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
                
    
    def display_updated_basket(order_basket, original_order_basket):
        print("Looks Like Some Items Sold Out, We've Updated Your Order") # THIS WILL BE THE NEW UPDATED FINAL DISPLAY
        for product in order_basket:
            #a, b, c, d = product
            print(f"{product[3]}x {product[1]}(#{product[0]}) @ £{(product[2] / product[3]):.2f} each - [£{product[2]} total]")
            #print(a,b,c,d)
        #
        ### COMMIT CONFIRM THEN CLEAN UP THIS WHOLE SECTION A TAD, THEN ITS JUST -> ADD ORDER STATUS, SHUFFLE COURIERS AND RETURN PROPERLY AND IS DONE
       ####################
       ####################
       ####################
       ####################
       ####################
       ####################
       ####################
       ####################
       ####################
       ####################
       ####################
       ####################
    

    print("Ok finalising your basket...")
    final_products_list = []
    original_order_basket = sum(order_basket, [])
    #print(original_order_basket)
    #print(order_basket)
    order_basket = update_quants_from_basket(order_basket)

    
    

    final_products_quants_list = []

    if order_basket is None:
        print("order basket is none")
        order_basket = original_order_basket
    else:
        display_updated_basket(order_basket, original_order_basket) #display updated basket and confirm function
    for item_info in order_basket:
        final_products_list.append(item_info[0]) # FOR STRICT GENERATION PROJECT
        final_products_quants_list.append((item_info[0],item_info[3])) # NEW! -> TO RETURN 
    
    #print(final_products_list)
    #print(final_products_quants_list)
    print("Basket Total")
    new_basket_total = 0
    #print(basket_total)
    for product in order_basket:
        new_basket_total += product[2]
    basket_total = new_basket_total
    #print(basket_total)

    print(f"The Item Numbers Being Sent Are = {final_products_quants_list}") #print(f"Return Value (tbc) = {order_basket[-1][0]}")   
    print(f"Total Final Price For Your Order = £{basket_total:.2f}")
    
    # it that works we're gravy here for now just cont (status then done?! could move courier select but meh, also do need to confirm the quantity is updating)
    print("Returning as tuple! - dont forget to unpack on receipt")
    return(final_products_quants_list, basket_total) # this is just the last one (being product number) added (needs to be a list), simple for loop (or comprehension!) will do the trick
    
    # create only products list quickly and return it PLUS final price
    # get status
    # fyi feel like attaching courier should come after the ordering process but whatever do in future
    # needs to return the list of all product ids
    # THE BASKET WILL BE COMPLETED AT THIS POINT SO YES THIS IS FINE IG - MAKE THIS (list of products) A LIST IN HERE THO FOR SURE

    # UPDATE QUANTITIES FROM BASKET NEW FUNCTION 100!
    # once confirmed, make live order (remaining things - create list thats only the products for order init, get status, get final price (have rn! save on confirm order here ig?))
    # then update quantity
        
        
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
        #print(order_basket)
        #print(item)
        #print(prdct.Product.products_list[item[0]-1])
        how_many = int(order_basket[i][3]) # might be unnecessary to force conversion here
        #print(f"Updating Quantity For {prdct.Product.products_list[item[0]-1].name}")
        #print(f"Current Quantity = {prdct.Product.products_list[item[0]-1].quantity}")
        #print(f"User Wants = {how_many}")
        final_quant = (prdct.Product.products_list[item[0]-1].quantity)-(how_many)
        #print(f"Final Quantity Will Be = {final_quant}") 
        if final_quant < 0:
            print(f"Uh Oh, Looks Like We Need To {0 - final_quant} From {prdct.Product.products_list[item[0]-1].name}")  
            print(f"Updating User Basket - {order_basket}")
            print(f"Updating Item Total - {order_basket[i][3]} + {final_quant}")
            order_basket[i][3] + final_quant
            made_updates = True   
            order_basket.pop(i) 
            # if ok then commit the change and return the order (ONLY RETURN IF VALID THEN COULD CHECK IF IS NONE ON RETURN - ACTUALLY YES AS WANT TO CONFIRM ANY UPDATES WITH THE USER)
        if made_updates == False:
            prdct.Product.products_list[item[0]-1].quantity -= how_many
        print(f"Updated Quantity = {prdct.Product.products_list[item[0]-1].quantity}")
    if made_updates:
        print("Made Updates")
        return(order_basket) # new and necessary - must return as may update it now 
    else:
        return(None)
 


    # WILL NEED TO RESET THIS BASKET ON ORDER COMPLETE - just have some kinda bool param i can pass to wipe the list within
    
    # make basket own function duhhh!

    # PRICING STUFF ooooo, will need to get quan from user here too!
    # should allow to review at the end ig (quick pops to remove unwanted items, ability to add more quant and go back and add more too? maybe not last one tbf)
    # WILL NEED TO SETATTR QUAN WHEN ORDER IS LIVE OOOO!
    #
    # honestly faf around with displays later just continue to take input, validation, etc now have the list attrs no probs!
    #





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
            Orders.items_per_list_print(disp_size, rows)
            fm.fake_input()

        if user_menu_input == "3":
            print(*(cour.Couriers.generate_index_name_string(cour.Couriers)), sep="\n")
            fm.fake_input()


if __name__ == "__main__":
    main_orders()






