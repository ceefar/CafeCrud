import format_random_v2_00 as fm
import csv
import re
import random
import csv


# CLASSES ########################################

# PRODUCTS CLASS ########################################

class Product:
    products_list = [] # list of all instances of each product, is this owned (as in stored) by every object of the class? (as it could get huge tho right)
    product_id_cache = []

# OBJECT (PRODUCT) METHODS ########################################

# INIT / CREATE NEW ########################################
    def __init__(self, name:str, price_gbp:float, quantity:int, product_number:int = None): # if you want vars to be unique for each instance/object of a class, put them in init, if putting them above init changing the var will change it for ALL instances of the class
        # initialising the variables for each object

        def get_valid_product_id():
            """ if the id you want to use is in the couriers_id_cache then create a new one """
            current_value = int(max(self.product_id_cache)) + 1 # plus one to the largest number in the id cache gives you the most valid number for the id (will not duplicate)      
            missing_elements = [ele for ele in range(max(self.product_id_cache)+1) if ele not in self.product_id_cache and ele != 0] # get the missing elements in the list and store in in a new (temp) list

            if missing_elements: # has items (so there are valid missing numbers we could use for IDs)
                self.product_number = missing_elements[0] # use the first (lowest numbered) item in that list (of missing elements)
            else: 
                self.product_number = current_value # if no missing elements then just the "highest" + 1

            self.product_id_cache.append(int(self.product_number)) # append the id to our cache, having cache means no duplicates, no duplicates means search by id number is plausible
            #END IF
        #END INLINE FUNCTION

        # varaibles, set regardless of load or create (so all except id/numb)
        self.name, self.price_gbp, self.quantity = name, price_gbp, quantity
        
        # for differences between loading existing and creating new
        if product_number: # if id/numb has a value, this means you have existing data to use when creating this new object

            self.product_number = int(product_number) # FUCKING BASTARD LINE, so what was happening was, when the self had no value and was being given the prod number value it was being given a string and that was causing hella issues

            if self.product_number in self.product_id_cache:
                # if there is a ID clash then update the id
                print(f"[ Potential ID Clash ({self.product_number}) Averted ]")
                get_valid_product_id()
            else:
                self.product_number = product_number
                self.product_id_cache.append(int(self.product_number))
            self.products_list.append(self)
            print(f"#{self.product_number} {self.name} ({self.quantity}) - £{self.price_gbp} Loaded") # TO ADD A BOOL PARAM FOR SHOWING THIS PRINT STATEMENT?
        else:
            # you are creating from scratch, so you need a new, dynamically created product_number/id
            if self.product_id_cache: # has items
                get_valid_product_id()
            else:
                # if the cache has no items then its the first ite, so if its a brand new courier their number will be one (ooooo lucky you huh)
                self.product_number = 1
                self.product_id_cache.append(int(self.product_number))
            # append it to the "global" list and print back confirmation
            self.products_list.append(self)
            print(f"#{self.product_number} {self.name} ({self.quantity}) - £{self.price_gbp} Created") # TO ADD A BOOL PARAM FOR SHOWING THIS PRINT STATEMENT?  
        #END IF
        #print(Product.product_id_cache)
    #END INIT


# PRINT PRODUCTS METHODS ######################################## 

# v7 print - pagination by price to do eventually cba rn
    def paginated_print_by_price(self, disp_size: int=22, rows: int=4):
        def generate_index_price_string(self):
            return((f"{i+1}",f"{p.price_gbp}") for i,p in enumerate(self.products_list))
        x = generate_index_price_string(self)
        print(x)
        def print_all_products_by_index(self):
            full_list = []
            for i, p in enumerate(self.products_list):
                full_list.append(((i+1),(p.price_gbp)))
                #full_list.append(((f"[{i+1}]"),(f"{p.price_gbp}")))
            return(full_list)
        y = print_all_products_by_index(self)
        print(y)
        print("\n\n\nSORTED")
        final_sorted_price_tuple = sorted(y,key=lambda x:x[1], reverse=True)
        print(type(final_sorted_price_tuple[0]))
        print(type(final_sorted_price_tuple[1]))
        print(type(final_sorted_price_tuple[1][0]))
        print(type(final_sorted_price_tuple[1][1]))
        print(*(x for x, _ in final_sorted_price_tuple))
        ###### JUST DISPLAY AS LIST IN CHUNKS, DONE ENOUGH FANCY DISPLAY THATS ENOUGH LOL!


    # v6 print - pagination
    def paginated_print(self, disp_size: int=22, rows: int=3, disp_str = "Enter Page Number (or use . to step forward +1 page) : ", title_str=None): #just changed rows default arg from 4 to 3 btw
        try:
            user_wants_page = 1 # initialises the loop
            # whole method is this loop, obvs not ideal 
            while user_wants_page != "0":
                usable_screen = int(disp_size) - 11
                ipl = usable_screen # max amounts of items that can be in one vertical line
                ipp = ipl * rows # items per page = max amount of items on the page, the vertical list multiplied by the amount of rows
                #rows = 5 # var for readability and incase wanna change for smaller sized screens not baking into equation (ik actually is cols lol) - also is now a setting btw
                full_pages = int(len(self.products_list) / ipp) # amount of full pages (page full with items)
                remaining_items = len(self.products_list) % ipp # amount of remainder items (amount of items in the final page if not all full)
                is_remainder = True # if remainder page this = True, if no remainder page = False
                display_to_use = [] # list of lists of courier index per page but as display version (starts at 1 not zero) e.g. [[1,2,3,4,5][5,6,7,8,9,10] for ipp = 5]
                pages_print = [] # bottom pages display string
                pages_as_numbers_listed = [] # the amount of pages (e.g. 20 items with 5 items_per_page = [1,2,3,4], 66 items with 10 ipp = [1,2,3,4,5,6,7] (7th is the remainder which it includes here yes)
                last_page = [] # the single list with indexes of the last page (basically display_to_use but the end of it)
                # top printout
                fm.format_display(disp_size)
                if title_str is None:
                    print(f"Sexy AF Pagniation - Dynamic Page Size") 
                else:
                    print(f"{title_str}")
                print(f"Currently {ipp} Items Per Page, {len(self.products_list)} Total Products\n{fm.print_dashes(return_it=True)}") # note the reason to point out uses index notation is for deleting and displaying etc this is best, thats just what indexing is for, but product numbers is more like a unique identifier that isn't the name incase it was required which im sure there are irl cases for
                print(f"[Index] Product (quantity) - £Price\n")
                
                if remaining_items != 0: #print(f"usable_screen={usable_screen}\n,ipl={ipl}\n,ipp={ipp}\n,full_pages={full_pages}\n,remaining_items={remaining_items}\n,")
                    page_nos = full_pages + 1
                else:
                    page_nos = full_pages
                    is_remainder = False

                # for the amount of pages that we will need, create a list of the pages as ints and mays well make a display string now too
                for county in range(page_nos):
                    pages_as_numbers_listed.append(county + 1)
                    # append that number (1,2,3,4...) formatted ( [ 1 ], [ 2 ]...) to a list as a string which we will display back to the user later 
                    pages_print.append("[ " + str(county + 1) + " ]")
                # END FOR
                    # for the amount of full pages (starting at pos 0), create their lists, based on the items_per_page (variable you can change)
                for x in range(full_pages):
                    # list of the display indexes to use - we then add this to a "global list" when done looping
                    display_list = []
                    # for the ipp (amount of items per page), populate each page list (e.g 1 then 2 then 3) with items per page
                    for number in range(ipp):
                        # use the x value, one level up, which relates to the page numbers index starting at 0
                        # and multiply that value by the items per page, meaning if we are on page index 0 (so page 1)
                        # we do not multiply, well we do but by 0 so we get 0, so the numbers aren't modified (apart from adding 1 for the display)
                        # so if x == 0, the value is 0 so 0 + 0 (+1) = 1, 1 + 0 (+1) = 2, etc -> 1,2... then when x == 1, 1*ipp(5) = 5 so 0 + 5 (+1) = 6, 1 + 5 (+1) = 7...
                        y = x * ipp
                        # number starts at zero so need to also add 1 to the Y value (which is just increments of the ipp (ipp x 1, ipp x 2, ipp x 3...))
                        display_list.append(number + y + 1)
                    # append it to the "global" list
                    display_to_use.append(display_list)
                # END FOR
                # literally the same as above but with just the end items and so only need that final index amount 
                final_index = full_pages * ipp
                for number in range(remaining_items):
                        y = final_index
                        last_page.append(number + y + 1)

                current_page_number = (user_wants_page - 1) * ipp
                the_page = []
                # function
                # creates the initial lists with just ints of the order
                for g in range(ipl):
                        x = g + current_page_number # if needs to be plus 1 then do here and also in x < len(main_co_list) + 1
                        row_list = []
                        for row in range(rows): # rows? needed (for X per line)
                            if x < len(self.products_list):
                                row_list.append(x)
                            x += ipl
                        the_page.append(row_list)
                        x += 1
                        # END FOR
                # END FOR
                # legit the entire above section can be achieved in 1 list comprehension, similar to...
                # cpage = lambda x : x - 1)*60 ???
                # [(cpage(a)),(cpage(b)),(cpage(c)),(cpage(d)),(cpage(e)) for ] ??? whatever... returning lists for a,b,c... (1,)
                # filling in the above for loop with the data you want
                
                def is_sold_out(the_product):
                    if int(the_product) == 0:
                        return("GONE")
                    else:
                        return(the_product)

                for the_line in the_page: 
                    print_string = ""
                    for prdct in the_line:
                        prdct + current_page_number
                        

                        #
                        # IF ITS QUANT IS ZERO THEN USE A DIFF TING HERE!!
                        #
                        current_string = (f"{prdct} {self.products_list[prdct].name} {self.products_list[prdct].price_gbp} {is_sold_out(self.products_list[prdct].quantity)} ")
                        spaces = 48 - (len(current_string))
                        spaces_string = ""
                        if int(prdct) + 1 == 10: # adjust for the extra character in the display by minusing one from the spaces on the end
                            spaces -= 1
                        if int(prdct) + 1 == 100:
                            spaces -= 1
                        if int(prdct) + 1 == 1000:
                            spaces -= 1
                        if int(prdct) + 1 == 10000:
                            spaces -= 1
                        if int(prdct) + 1 == 100000:
                            spaces -= 1
                        for x in range(spaces - 5):
                            spaces_string += " "
                        print_string += (f"[ {int(prdct) + 1} ] {self.products_list[prdct].name} {spaces_string} ({self.products_list[prdct].quantity}) - £{self.products_list[prdct].price_gbp}       ")
                    print(print_string)
                    # yield back as tuples with index value, check as recieving yield, if index value not in the indexes that would be in the current page (0-59,60-119...)
                cpage = int((current_page_number + ipp) / ipp)
                # move this to format random
                def return_one_line_art():
                    one_line_ascii_art_list = ["̿' ̿'\̵͇̿̿\з=(◕_◕)=ε/̵͇̿̿/'̿'̿ ̿  NOBODY MOVE!","( ͡° ͜ʖ ͡°) *staring intensifies*","(╯°□°)--︻╦╤─ - - - WATCH OUT HE'S GOT A GUN","(⌐■_■)--︻╦╤─ - - - GET DOWN MR PRESIDENT","┻━┻︵  \(°□°)/ ︵ ┻━┻ FLIPPIN DEM TABLES","(ノಠ益ಠ)ノ彡︵ ┻━┻︵ ┻━┻ NO TABLE IS SAFE","ʕつಠᴥಠʔつ ︵ ┻━┻ HIDE YO KIDS HIDE YO TABLES","(ಠ_ಠ)┌∩┐ BYE BISH","(ง •̀_•́)ง FIGHT ME FOKER!","[¬º-°]¬  [¬º-°]¬ ZOMBIES RUN!","(╭ರ_•́) CURIOUSER AND CURIOUSER","つ ◕_◕ ༽つ つ ◕_◕ ༽つ TAKE MY ENERGY","༼つಠ益ಠ༽つ ─=≡ΣO)) HADOUKEN!"]
                    return(one_line_ascii_art_list[random.randint(0, len(one_line_ascii_art_list)-1)])
                # END NESTED FUNCTION that i should totally move 
                if cpage > len(pages_as_numbers_listed) : print(return_one_line_art()) ############### ascii art, could do if max go back to one but prefer the easter egg
                print("\n", end="PAGES ")
                #pages_print.insert(0,"PAGE NUMBERS :")
                highlight_page = lambda h : f"[[ {h} ]]" if h == cpage else f"[ {h} ]" # language is so mad wtf            
                print(*[highlight_page(p) for p in pages_as_numbers_listed])
                #print("^ page numbers ^")
                #
                #
                # UPDATING
                # user_wants_page = input("\nEnter Page Number (or use . to step forward +1 page) : ")
                #
                #
                user_wants_page = input(f"\n{disp_str}")
                if user_wants_page == "0":
                    break
                elif user_wants_page == ".":
                    user_wants_page = int((current_page_number + ipp) / ipp) + 1
                    #print(f"Page - {user_wants_page}")
                else:
                    user_wants_page = int(user_wants_page)
        except ValueError as e:
            print("STOP PRESSING ENTER! (or maybe this is bad ux duhhhh!") # "No... it's the children who are wrong" https://knowyourmeme.com/memes/am-i-so-out-of-touch
 

    # v5 print - items per line
    def items_per_list_print(self, disp_size: int=22):
        ipl = 4 # calling my screen size (disp size) 22, calling used up lines 10 for now, so 22 - 10 = 12
        usable_screen = int(disp_size) - 10
        ipl = usable_screen
        i_list = []
        # function
        # creates the initial lists with just ints of the order
        for g in range(ipl):
                x = g # if needs to be plus 1 then do here and also in x < len(main_co_list) + 1
                g_list = []
                for i in range(int(len(self.products_list)/ipl) + 1): # rows? needed (for X per line)
                    if x < len(self.products_list):
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
                current_string = (f"{index} {self.products_list[index].name}")
                spaces = 30 - (len(current_string))
                spaces_string = ""
                if int(index) + 1 == 10:
                    spaces -= 1
                for x in range(spaces):
                    spaces_string += " "
                print_string += (f"[ {int(index) + 1} ] {self.products_list[index].name} {spaces_string}")
            print(print_string)

    # v4 print - one line generator
    def generate_index_name_string(self):
        return((f"{i+1}. {p.name} - £{p.price_gbp}") for i,p in enumerate(self.products_list))

    # v3 print - generate/yield for loop
    def yield_back_index_name_string(self):  
        for i, p in enumerate(self.products_list):
            i += 1
            is_sold_out = lambda x : int(x) if int(x) > 0 else "[ SOLD OUT! ]"
            final_string = (f"[ {i} ] - {p.name} - £{p.price_gbp} ({is_sold_out(p.quantity)})") 
            yield(final_string)
            # END LOOP
        #END FOR
                
    # v2 print - basic, by index
    def print_all_products_by_index(self):
        for i, p in enumerate(self.products_list):
            print(f"[{i+1}] - {p.name} - £{p.price_gbp}")

    # print via class method test (using v2 print)
    @classmethod
    def print_via_class_method(cls):
        for i, p in enumerate(cls.products_list):
            print(f"[{i+1}] - {p.name} - £{p.price_gbp}")

    # v1 print - basic, by product name
    def print_all_products_by_name(self):
        for p in self.products_list:
            print(f"[{p.product_number}] - {p.name} - £{p.price_gbp}")

# UPDATE PRODUCTS METHODS ######################################## 

    # UPDATE SINGLE NAME
    def update_name(self, to_update:int): 
        print(f"Prompt For Update Name [Current : {self.products_list[to_update - 1].name}]") #print(f"Updating {self.products_list[to_update - 1]}") # displays the memory address
        new_name = input("Update The Name To : ")
        print("Commit Confirm?")
        self.products_list[to_update - 1].name = new_name
        print(f"Name Updated To {self.products_list[to_update - 1].name}")

    # UPDATE ATTRIBUTE (TESTING FOR PRICE & QUANTITY)
    def update_int_attr(self, to_update:int, the_key): 
        current_value = getattr(self.products_list[to_update - 1], the_key)
        print(f"Prompt For {the_key}") # already have a function that will convert this to a "nice" name 
        if the_key != "price_gbp":
            new_value = int(input(f"Update {current_value} To : "))
        elif the_key == "price_gbp":
            new_value = get_price(self.products_list[to_update - 1].name)
        setattr(self.products_list[to_update - 1], the_key, new_value)
        print(f"{the_key} Updated To {new_value}")

# DELETE PRODUCTS METHODS ######################################## 

    # DELETE
    def select_and_delete(self, to_delete:int): #should take the input?
        print(f"Deleting {self.products_list[to_delete - 1]}")
        del self.products_list[to_delete - 1]
        print("yeah... no taking that one back")

# SAVE/LOAD PRODUCTS METHODS #####################################

    # based on the exact requirements of the specification
    def save_all_products_as_txt(self, file_name:str = "x_main_products_list.txt"):
        # need if empty or None validation
        f = open(file_name, "w")
        for i, _ in enumerate(self.products_list):
            f.write(str(self.products_list[i].product_number) + "," + self.products_list[i].name + "," + str(self.products_list[i].price_gbp) + "," + str(self.products_list[i].quantity) + "\n")
        f.close

    def save_all_products_as_csv(self, file_name:str = "x_main_products_list.csv"):
        with open(file_name, "w", newline="") as csvfile:
            # set the headers for the csv
            fieldnames = ["product_number", "product_name", "price_gbp", "quantity"]
            # instruct the writer to write the headers
            writer = csv.DictWriter(csvfile, delimiter=',', fieldnames= fieldnames)
            writer.writeheader()
            # instruct the writer to write the row
            for i, _ in enumerate(self.products_list):
                writer.writerow({"product_number":self.products_list[i].product_number, "product_name":self.products_list[i].name, "price_gbp":self.products_list[i].price_gbp, "quantity":self.products_list[i].quantity})

    def load_list_from_file(init_load):
        list_copier = []
        f = open("x_main_products_list.txt", "r")
        for lines in f:
            list_copier.append(lines.strip())
        f.close()
        for amount in range(len(list_copier)):
            x = list_copier[amount].split(",")
            #print(f"0 = {x[0]}, type={type(x[1])}")
            #print(f"1 = {x[1]}, type={type(x[1])}")
            #print(f"2 = {x[2]}, type={type(x[1])}")
            #print(f"3 = {x[3]}, type={type(x[1])}")
            Product(x[1], x[2], x[3], x[0]) #print(f"{x} <- x")
        print("Loaded Successfully") # actually 100% is not true, would need to do properly just want some feedback from the function for now
        if init_load == False:
            fm.fake_input()

    def load_products_via_csv():
        templist = []
        # open csv and read as string
        with open("x_main_products_list.csv", "r") as file:
            reader = csv.reader(file, delimiter=",")
            for row in file:
                templist.append(row.strip())
                print(f"{row} LOADED SUCCESSFULLY")
        fm.format_display()
        templist.pop(0) # pops the header off the temp list
        #Product.products_list = templist
        try:
            for index in range(len(templist)):
                x = templist[index].split(",")
                Product(x[1], float(x[2]), int(x[3]), int(x[0]))
        except IndexError:
            fm.print_dashes()    

# RANDOM PRODUCT METHODS #########################################

    def count_products_list(self):
        return(len(self.products_list))

    # for initial display only
    def get_last_product_number(self):
        return(self.products_list[-1].product_number)

    # REDUNDANT BUT LEAVING FOR LEARNING
    def print_products(self):
        print(*[p for p in self.products_list])
        # <__main__.Product object at 0x000002A32EF23FD0> <__main__.Product object at 0x000002A32EF23DC0> <__main__.Product object at 0x000002A32EF23A30> <__main__.Product object at 0x000002A32EF21270>
        # because PRODUCT as an object is just a position in memory, like without my name I am just atoms in the universe

## END CLASS ############################################################################################################################################################


## MAIN FUNCTIONS #######################################################################################################################################################

## MENU FUNCTIONS #######################################################################################################################################################

def main_menu(rows=3, disp_size=22):
    #disp_size = 20
    #rows = 3
    # MAKE A SCREEN SIZE DISPLAY AND FUNCTION THAT PRINTS LINES, USERS SELECTS COMFORT, AND THEN LINES ARE SET TO THIS (display as a class holy shit)
    user_menu_input = 1
    go_again = False
    while user_menu_input != "0":
        # IF LOOP VAR NOT TRUE PRINT MENU, GET INPUT, ELSE SET INPUT ON LEAVE FUNCTION TO SKIP PRINT & INPUT
        if go_again != True: 
            # PRINT THE MENU  
            fm.format_display(disp_size)
            print(f"PRODUCTS v1.02\n(using object oriented principles)\n{fm.print_dashes(return_it=True)}\n")
            menu_string = ["[ 1 ] Create New", "[ 2 ] Select & Delete (alpha)", "[ 3 ] Print Sub Menu", "[ 4 ] Update Product Name", "[ 5 ] Sexy Pagniation", "[ 6 ] Update Attributes (alpha af)", "[ - ] -", "[ S ] Settings Sub Menu", "[ L ] Load Products To Classes (alpha)", "[ 0 ] Main Menu\n","- - - - - - - - - - -"]
            print(*menu_string, sep="\n")
            # GET THE USERS INPUT
            user_menu_input = input("Enter Menu Selection : ")
        
        # [1] CREATE NEW PRODUCT
        if user_menu_input == "1":
            create_new_product(disp_size) # return values are for quick menu / add again loop
            # QUICK MENU / CREATE AGAIN
            print("Quick Create Another Product?\n")
            if get_user_yes_true_or_no_false():
                go_again = True
                user_menu_input = "1"
            else:
                go_again = False

        # [2] DELETE PRODUCT (by index, using v5 print)
        elif user_menu_input == "2":
            fm.format_display(disp_size)
            print(f"Print by Print Formatted String From Generator\n(also uses index notation)\n{fm.print_dashes(return_it=True)}")
            print(f"Amount of Products = {len(Product.products_list)}")
            Product.items_per_list_print(Product, disp_size)
            #print(*(Product.generate_index_name_string(Product)), sep="\n")
            fm.print_dashes()
            to_delete = int(input("Enter Number To Delete : "))
            Product.select_and_delete(Product, to_delete)
            fm.print_dashes()
            fm.fake_input()
            print("Quick Delete Another Product?\n")
            if get_user_yes_true_or_no_false():
                go_again = True
                user_menu_input = "2"
            else:
                go_again = False
            
        # [3] - PRINT SUBMENU
        elif user_menu_input == "3":
            print_submenu(disp_size)

        # [4] - UPDATE PRODUCT
        elif user_menu_input == "4":
            fm.format_display(disp_size)
            print(f"Update Product Name\n(also uses index notation)\n{fm.print_dashes(return_it=True)}")
            print(f"Amount of Products = {len(Product.products_list)}\n")
            Product.paginated_print(Product, disp_size, rows)
            print(" ")
            fm.print_dashes()
            to_update = int(input("Enter Number To Update : "))
            Product.update_name(Product, to_update)
            fm.print_dashes()
            fm.fake_input()
            
        # [5] SEXY PAGINATED PRINT
        elif user_menu_input == "5":
            Product.paginated_print(Product, disp_size, rows)
            print("") 
            fm.print_dashes()
            fm.fake_input()
                        
        # [6] TEST UPDATE ATTR
        elif user_menu_input == "6":
            print(f"Update Quantity\n{fm.print_dashes(return_it=True)}")
            print(f"Amount of Products = {len(Product.products_list)}\n")
            Product.paginated_print(Product, disp_size, rows)
            print(" ")
            fm.print_dashes()
            to_update = int(input("Enter Number To Update : "))
            Product.update_int_attr(Product, to_update, "quantity")
            fm.print_dashes()
            print("Now Update The Price")
            Product.update_int_attr(Product, to_update, "price_gbp")
            fm.print_dashes()
            print("Update Complete")
            fm.fake_input()
            
        # [7] -  
        elif user_menu_input == "7":
            Product.paginated_print_by_price(Product, disp_size, rows)

        # [8] -
        elif user_menu_input == "8":
            pass

        # [S] SETTINGS SUB MENU
        elif user_menu_input == "S" or user_menu_input == "s":
            disp_size, rows = settings_submenu(disp_size, rows)

        # [L] L - LOAD (HIDDEN)
        elif user_menu_input == "L" or user_menu_input == "l":
            Product.load_products_via_csv()
            #Product.load_list_from_file(False)

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
    Product.save_all_products_as_txt(Product)
    Product.save_all_products_as_csv(Product)
    print("SAVING...")
    return(rows, disp_size)

## SETTINGS SUBMENU #######################################################################################################################################################

def settings_submenu(disp_size, rows):
    user_submenu_input = "1"
    while user_submenu_input != "0":
        # PRINT THE SUB MENU  
        fm.format_display(disp_size)
        print(f"SETTINGS SUBMENU - products v1.02\n(using object oriented principles)\n{fm.print_dashes(return_it=True)}\n")
        menu_string = ["[ 1 ] Quick Add - 10 Default Products", "[ 2 ] Quick Add - X Products", "[ 3 ] Display - Format Screen", "[ 4 ] Display - Set Rows", "[ 5 ] Load - From Default File", "[ - ] -", "[ 0 ] Back To Main Menu\n","- - - - - - - - - - -"]
        print(*menu_string, sep="\n")
        # GET THE USERS INPUT
        user_submenu_input = input("Enter Your Input : ")
        # VALIDATE NATURAL LANGUAGE (NEW! - ALPHA)
        if grab_natural_lang(user_submenu_input) == False:
            print("do valid thing")
            fm.fake_input()
            break

    # [1] QUICK ADD DEFAULT PRODUCTS
        if user_submenu_input == "1":
            fm.format_display(disp_size)
            quick_add_ten_products(disp_size)
    
    # [2] QUICK ADD X PRODUCTS   
        elif user_submenu_input == "2":
            fm.format_display(disp_size)
            print(f"Quick Add - X Products\nEnter Amount Of Products To Add (For Testing)\n{fm.print_dashes(return_it=True)}")
            inc_by = int(input("Enter Number (upto 100,000) : ")) # so far run for 1k, 2k, 10k?, need more tho 
            quick_add_some_products(inc_by)
            fm.fake_input()

    # [3] FORMAT SCREEEN
        elif user_submenu_input == "3":
            disp_size = format_screen(disp_size)
            fm.fake_input()

    # [4] SETTINGS - SET ROWS
        elif user_submenu_input == "4":
            rows = set_display_rows(rows)

    # [5] LOAD FROM FILE
        elif user_submenu_input == "5":
            Product.load_products_via_csv()
            #Product.load_list_from_file(False)

    # [0] BACK / RETURN TO MAIN MENU
        elif user_submenu_input == "0":
            print("Returning To Products Menu")
            #return(disp_size, rows)
            break
        else:
            print("Input Error - Returning To Products Menu")
            #return(disp_size, rows)
            break
    print("Saving Settings...")
    return(disp_size, rows)

## PRINT SUBMENU #######################################################################################################################################################

# PUT THESE ALL INTO THEIR OWN FUNCTIONS PLSSSS
def print_submenu(disp_size):
    user_submenu_input = "1"
    while user_submenu_input != "0":
        # PRINT THE SUB MENU  
        fm.format_display(disp_size)
        print(f"PRINT SUBMENU - products v1.02\n(using object oriented principles)\n{fm.print_dashes(return_it=True)}\n")
        menu_string = ["[ 1 ] Print By Product Number", "[ 2 ] Print By Index", "[ 3 ] Print By Yield", "[ 4 ] Print By One Line Generator", "[ 5 ] Print By Items Per Line", "[ 0 ] Back To Main Menu\n","- - - - - - - - - - -"]
        print(*menu_string, sep="\n")
        # GET THE USERS INPUT
        user_submenu_input = input("Enter Your Input : ")

        # [1] SIMPLE PRINT PRODUCTS, ALL 1 VERTICAL LINE, LONG PRODUCT NUMBERS
        if user_submenu_input == "1":
            fm.format_display(disp_size)
            print(f"Print by Product Number\n{fm.print_dashes(return_it=True)}\n")
            print(f"Amount of Products = {len(Product.products_list)}\n") # amount is length of products list, also print(f"{Product.count_products_list(Product)} Total Products") which using return value 
            Product.print_all_products_by_name(Product)
            print("")
            fm.print_dashes()
            fm.fake_input()

        # [2] PRINT BY INDEX
        elif user_submenu_input == "2":
            fm.format_display(disp_size)
            print(f"Print by Index of Object in List\n{fm.print_dashes(return_it=True)}\n")
            print(f"Amount of Products = {len(Product.products_list)}\n")
            Product.print_all_products_by_index(Product)
            print("")
            fm.print_dashes()
            fm.fake_input()

        # [3] PRINT BACK GENERATOR
        elif user_submenu_input == "3":
            fm.format_display(disp_size)
            print(f"Print by Print Formatted String From Generator\n(also uses index notation)\n{fm.print_dashes(return_it=True)}\n")
            print(f"Amount of Products = {len(Product.products_list)}\n")
            print(*(Product.yield_back_index_name_string(Product)), sep="\n")
            print("")
            fm.print_dashes()
            fm.fake_input()

        # [4] IMPROVED GENERATOR
        elif user_submenu_input == "4":
            fm.format_display(disp_size)
            print(f"Print by Print Formatted String From Generator\n(also uses index notation)\n{fm.print_dashes(return_it=True)}\n")
            print(f"Amount of Products = {len(Product.products_list)}\n")
            print(*(Product.generate_index_name_string(Product)), sep="\n")
            print("") 
            fm.print_dashes()
            fm.fake_input()

        # [5] ITEMS PER LINE
        elif user_submenu_input == "5":
            fm.format_display(disp_size)
            print(f"Print Items Per Line \n(also uses index notation)\n{fm.print_dashes(return_it=True)}\n")
            print(f"Amount of Products = {len(Product.products_list)}\n")
            Product.items_per_list_print(Product, disp_size)
            print("") 
            fm.print_dashes()
            fm.fake_input()
        elif user_submenu_input == "0":
            print("Returning To Products Menu")
            break
        else:
            print("Input Error - Returning To Products Menu")
            break


## CREATE NEW FUNCTIONS #######################################################################################################################################################

def create_new_product(disp_size):
    fm.format_display(disp_size)
    print(f"Create New Product\n{fm.print_dashes(return_it=True)}")
    name = input(f"Enter A Name For Product {Product.count_products_list(Product) + 1} : ")
    # CONVERT PRICE IN POUNDS TO FLOAT, IF DOESNT WORK THEN GO AGAIN
    price_in_pounds = get_price()
    quantity = input(f"Enter The Quantity For {name.title()} : ")
    fm.format_display(disp_size)
    # CREATE NEW INSTANCE OF PRODUCT WITH USER GIVEN NAME (runs print confirms to user, etc)
    Product(name, price_in_pounds, quantity)
    # FOR PRINTING BACK 0s TO THE USER, USES THE LEN OF THE STR OF THE LEN OG PRODUCT NUMBERS AND USES IT AS AN INDEX TO SLICE FROM THE END OF THE STRING
    get_zeros = lambda x : "0"*(4 - len(str(x)))
    print(f"Product #{get_zeros(Product.get_last_product_number(Product))}{Product.get_last_product_number(Product)} Added Sucessfully")
    #################
    # UPDATED AS ZEROS REMOVED
    # trim_by = lambda x : 4 - len(str(len(x)))
    # print(f"Product #{str(Product.get_last_product_number(Product)[trim_by(Product.products_list):])} Added Sucessfully")
    #################
    fm.print_dashes()

# both so validation, both so reusable
# get quantity
# get name
    
def get_price():
    the_price = "1"
    while the_price != "0":
        #print("Please Use This Format - £12 or £12.9 or £12.90") - got it working with "12." (which is treated as 12.0) so removed
        fm.print_dashes()
        price_in_pounds = input(f"Enter The Price (In GBP - e.g 12.99) For Product {Product.count_products_list(Product) + 1} : £")
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
    #print(f"Returning {x}{type(x)}")
    return(float(price_in_pounds))



## NEW TEST SHIT 
## imo is overcomplicated, just search for the delimiter and then validate if the attached word has an action...

def action_logger(action:str, is_done:bool):
    #just have them relate to ints in a simple switch?
    actions_list = []
    if is_done == False:
        print("logged {}")
        actions_list.append(action)
    else:
        fm.fake_input()
        print('finalise the actions and route') #its own function!


def grab_natural_lang(input_string:str):
    action_counter = 0

    if is_natural_rows(input_string): # or natural language x or ....
        action_logger("rows", False)
        action_counter += 1 

    if action_counter != 0:    
        valid_natural_lang_input = True
    else:
        valid_natural_lang_input = False

    if valid_natural_lang_input:
        print("take the actions list and go places!")
        fm.fake_input()
        return(False)
    else:
        return(input_string) 
        # because there was no triggered input you can just return the string to do what it was doing...
        # you do this check on the string before a big menu input, if it validates, you skip the menu entirely!!!!!!

def is_natural_rows(input_string:str):
    if "rows" in input_string or "row" in input_string or "rw" in input_string or "rws" in input_string:
        try: 
            x = input_string.split()
            da_int = int(x[1])
            if da_int >= 4:
                print("sorry thats too problematic")
                fm.fake_input()
            else:
                print(da_int)
                return da_int
                fm.fake_input()
        except(ValueError):
            print("where int?")
            fm.fake_input()
            return False
        except(IndexError):
            print("where int tho?")
            fm.fake_input()
            return False
        return True # ?! will go from "sorry..."?
    else:
        return False # or true obvs depending on if answers question

#to achieve this do sequentially, check for X,
#                                 if find X check for its modifier, 
#                                                     if no modifier, if is still valid,
#                                                                                     do thing, 
#                                                                                 else,
#                                                                                     break fully
#                                                    if modifier
#                                                           check if modifier is valid (i.e. 20 for rows lol), 
#                                                                   if valid,
#                                                                        log it
#                                                                   if not valid (display and try again or just break (which just redisplays the current menu so yeah!))
# 
#   then once end
#           unpack the actions and route in proper order, any settings actions then user actions then print actions
#   then complete them
#   then display it to the user (using natty lang v0.1) 
#
# (will have a list unpacker that puts them into the appropriate order at the end then executes just log for now duh)
#                                            



## GENERAL FUNCTIONS #######################################################################################################################################################

def get_user_yes_true_or_no_false():
    # needs try except validation probably as tho this should cover some cases it won't cover all/enough?
    print("[ 1 ] = Yes")
    print("[ 2 ] = No\n")
    fm.print_dashes()
    user_input = input("Your Selection : ".upper())
    if user_input == "1":
        return(True)
    else:
        return(False)

def quick_add_ten_products(disp_size):
    fm.format_display(disp_size)
    print(f"Generating Asscream...\n{fm.print_dashes(return_it=True)}\n")
    Product("Asscream",1.99,100)
    Product("Jumbo Size Asscream",2.99,100)
    Product("Limited Edition Asscream",1.50,100)
    Product("Asscream 4 Pack",1.00,100)
    Product("Asscream Sport",4.99,100)
    Product("Asscream FOR KIDS!",6.99,100)
    Product("Asscream Lite",2.29,100)
    Product("Asscream ProGlide",1.15,100)
    Product("Asscream Luxe",31.10,100)
    Product("Asscream Mini",1.10,100)
    print("")
    print("10 Asscreams Added")
    print(f"{len(Product.products_list)} Asscreams Total\n")
    fm.print_dashes()
    fm.fake_input()

def quick_add_some_products(inc_by:int):
    for i in range(inc_by):
        Product(f"Ass[{i}]Cream",6.09,609)
    fm.format_display(20)

def format_screen(disp_size:int): 
    user_submenu_input = "1"
    while user_submenu_input != "0":
        print(*[x+9 for x in reversed(range(45))], sep="\n")
        print(f"Current Display Size = {disp_size} < ENSURE THESE MATCH! (remember 0 to reset)") 
        print("Recommended Display Size = 30+")
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

# DRIVER
# should set display on start?

def driver():
    Product.load_products_via_csv()
    #Product.load_list_from_file(True)
    main_menu()


if __name__ == "__main__":
    driver()

# NOTES
#
# DEFO DEFO do want quantity and price in gbp (as price will be interesting way to use stuff like map) (and then possibly type as cool for sorting)
# - could make something like special offer like this too right? special offer has multiple products etc

# make it a class? give it states (based on where it is and what is valid) (even privileges)

## OLD INIT CODE SAVING FOR NOW JUUUUUST INCASE - can del after testing 

'''
        if product_number != None:
            self.name, self.price_gbp, self.quantity, self.product_number = name, price_gbp, quantity, product_number
            self.products_list.append(self)
            print(f"#{self.product_number} {self.name} £{self.price_gbp} ({self.quantity}) Loaded")
        else:
            self.name = name
            self.price_gbp = price_gbp
            self.quantity = quantity
            def generate_initial_product_numbers():
                # to store 1000 comfortably, 10,000 total size. (w/ pagination now stores 10,000 comfortably, 100,000 total size - in regards to terminal display)
                p_len = lambda x : 5 - len(str(len(self.products_list)+1))
                get_zeros = lambda : "0" * p_len(len(self.products_list)+1)
                return(get_zeros())
            # complete the product number with the inital zeros and then the current product number (leng of the list = 1 since not yet initialised the object)
            if len(self.products_list) == 0: # if zero size list (so first time)
                self.product_number = generate_initial_product_numbers() + str(len(self.products_list) + 1)
            else:
       
                self.product_number = generate_initial_product_numbers() + str(self.products_list.index(self.products_list[-1]) + 2) 
                #
            self.products_list.append(self)
            print(f"#{self.product_number} - {self.name} £{self.price_gbp} Stored With {self.quantity} Items")       
    # END __INIT__  

'''