# IMPORTS
# db
import pymysql
import os
from dotenv import load_dotenv
# styling
import colorama
from colorama import Fore, Back, Style
from PyInquirer import prompt, Separator
# general
import format_random_v2_00 as fm
import csv
import re
import random

# initialise colorama
colorama.init(autoreset=True)
 

# DB

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


def add_to_db(command):
    cursor = connection.cursor()
    cursor.execute(f"{command}") 
    connection.commit()
    #cursor.close()
    #connection.close()


def get_from_db(command):
    cursor = connection.cursor()
    cursor.execute(f"{command}") 
    myresult = cursor.fetchall()
    #.commit()
    #cursor.close()
    #connection.close()
    return(myresult)


############################################################################## CLASSES ##############################################################################

########################################################################## PRODUCTS CLASS ##########################################################################

class Product:
    # CLASS VARS
    products_list = [] # list of all instances of each product, is this owned (as in stored) by every object of the class? (as it could get huge tho right)
    product_id_cache = []

# CLASS METHODS 

# INIT / CREATE NEW 

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
        #END NESTED FUNCTION

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
            #print(f"#{self.product_number} {self.name} ({self.quantity}) - £{self.price_gbp:.2f} Created") # TO ADD A BOOL PARAM FOR SHOWING THIS PRINT STATEMENT?  
        #END IF
        #print(Product.product_id_cache)
    #END INIT


# PRINT PRODUCTS METHODS ######################################## 

    # note this isnt just normal pagination, would have been easy to do via horizontal print, but notice print is ordered vertically
    # not (easy)
    # 1 > 2 > 3
    # 4 > 5 > 6
    # 7 > 8 > 9
    # but (hard)
    # 1 > 4 > 7
    # 2 > 5 > 8
    # 3 > 6 > 9
    # now also consider (harder)
    # that this is entirely dynamic, any amount can be added in real time and pages (notice the page number selector is dyanmic) + pagination will automatically adjust
    # plus (even harder)
    # it is dynamic to the amount of columns and height (screen size) that is selected by the user
    # seriously... it is my baby for a reason XD
    # very proud of it, basically just all maths, but thats all programming is anyways
    # oh and bonus (even harder fml)
    # you can step through the pages with "." and going to a page that is out of bounds will display cute ascii art to the user instead of breaking the display
    #
    # and also yes i know duplicated functions unnecessary, plus excessively long function, and probably redundant code throughout, but no time to refactor done alot already
    
    # v7 print - pagination (by price)
    def paginated_print_by_price(self, disp_size: int=22, rows: int=3, disp_str = "Enter Page Number (or use . to step forward +1 page) : ", title_str=None): #just changed rows default arg from 4 to 3 btw
        try:
            user_wants_page = 1 # initialises the loop
            # whole method is this loop, obvs not ideal 
            fm.format_display(disp_size)
            print(f"{Fore.CYAN}SORT BY PRICE{Fore.RESET}")
            fm.print_dashes()
            print("Do Want Ascending Or Descending Order?")
            fm.print_dashes()
            print(f"{Fore.GREEN}[A]{Fore.RESET}scending = Smallest To Largest (1 -> 100)")
            print(f"{Fore.CYAN}[D]{Fore.RESET}escending = Largest To Smallest (100 -> 1)") 
            fm.print_dashes()
            print("[ 1 ] - Ascending")
            print("[ 2 ] - Descending")
            fm.print_dashes()
            asc_or_desc = input(f"Enter Your Selection : ")
            if asc_or_desc == "A" or asc_or_desc == "a" or asc_or_desc == "1":
                is_ascending = True
            else:
                is_ascending = False
            fm.print_dashes()
            fm.fake_input()
            while user_wants_page != "0":
                a_query = f'SELECT COUNT(product_id) AS NumberOfProducts FROM products'
                the_result = get_from_db(a_query)
                len_of_items_from_db = int(the_result[0][0])
                usable_screen = int(disp_size) - 11
                ipl = usable_screen # max amounts of items that can be in one vertical line
                ipp = ipl * rows # items per page = max amount of items on the page, the vertical list multiplied by the amount of rows
                #rows = 5 # var for readability and incase wanna change for smaller sized screens not baking into equation (ik actually is cols lol) - also is now a setting btw
                full_pages = int(len_of_items_from_db / ipp) # amount of full pages (page full with items)
                remaining_items = len_of_items_from_db % ipp # amount of remainder items (amount of items in the final page if not all full)
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
                print(f"Currently {ipp} Items Per Page, {len_of_items_from_db} Total Products\n{fm.print_dashes(return_it=True)}") # note the reason to point out uses index notation is for deleting and displaying etc this is best, thats just what indexing is for, but product numbers is more like a unique identifier that isn't the name incase it was required which im sure there are irl cases for
                print(f"{Fore.BLUE}[ID] {Fore.CYAN}Product {Fore.BLACK}{Style.BRIGHT}(quantity){Style.RESET_ALL} - {Fore.GREEN}£Price{Fore.RESET}\n")
                
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
                            if x < len_of_items_from_db:
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
                
                def is_sold_out(the_product, want_colour = False): # IF YOU HAVE AN EXTRA PARAMATER HERE CAN WORK WITH COLOUR, 1 PARA DICTATES SIZE THEN NEXT FOR COLOUR 
                    if int(the_product) <= 0 and want_colour == False:
                        return("GONE")
                    elif int(the_product) <= 0 and want_colour == True:
                        return(f"{Fore.RED}GONE{Fore.RESET}")
                    elif int(the_product) <= 3 and want_colour == False:
                        return(f"ONLY {the_product}")
                    elif int(the_product) <= 3 and want_colour == True:
                        return(f"{Fore.RED}{Style.DIM}ONLY {the_product}{Fore.RESET}{Style.RESET_ALL}")
                    else:
                        return(the_product)

                # pull data from the db, yes pulls all the data from the table
                # yes would be ideal to just pull the current page (FROM products p LIMIT (ipl)) (or even the current item to print (or line whatever))
                # no not implementing here as have done elsewhere in the project i think, eitherway refactoring my baby aint happening, would take waaaaay too long lol
                if is_ascending:
                    query = f'SELECT p.product_name, p.product_price, p.product_quant, p.product_id FROM products p ORDER BY p.product_price'
                else:
                    query = f'SELECT p.product_name, p.product_price, p.product_quant, p.product_id FROM products p ORDER BY p.product_price DESC'
                result = list(get_from_db(query)) 
        
                for the_line in the_page: 
                    print_string = ""
                    for prdct in the_line:
                        prdct + current_page_number
                        
                        current_string = (f"{result[prdct][3]} {result[prdct][0]} {result[prdct][1]} {is_sold_out(result[prdct][2])}")
                        spaces = 49 - (len(current_string))
                        spaces_string = ""
                        if int(result[prdct][3]) == 10: # adjust for the extra character in the display by minusing one from the spaces on the end
                            spaces -= 0
                        if int(result[prdct][3]) == 100: # not needed now "index" (id) is taken directly from db
                            spaces -= 0
                        if int(result[prdct][3]) == 1000:
                            spaces -= 0
                        if int(result[prdct][3]) == 10000:
                            spaces -= 0
                        if int(result[prdct][3]) == 100000:
                            spaces -= 0
                        for x in range(spaces - 5):
                            spaces_string += " "
                        print_string += (f"{Fore.BLUE}[ {Style.DIM}{Fore.CYAN}{result[prdct][3]}{Style.RESET_ALL} {Fore.BLUE}]{Fore.RESET} {Fore.WHITE}{Style.BRIGHT}{result[prdct][0]}{Fore.RESET}{Style.RESET_ALL} {spaces_string} {Fore.BLACK}{Style.BRIGHT}({is_sold_out(result[prdct][2], want_colour=True)}{Fore.BLACK}{Style.BRIGHT}){Style.RESET_ALL} - {Fore.GREEN}£{result[prdct][1]}{Fore.RESET}       ")
                    print(print_string)
                    # yield back as tuples with index value, check as recieving yield, if index value not in the indexes that would be in the current page (0-59,60-119...)
                cpage = int((current_page_number + ipp) / ipp)
                # move this to format random
                def return_one_line_art():
                    one_line_ascii_art_list = ["̿' ̿'\̵͇̿̿\з=(◕_◕)=ε/̵͇̿̿/'̿'̿ ̿  NOBODY MOVE!","( ͡° ͜ʖ ͡°) *staring intensifies*","(╯°□°)--︻╦╤─ - - - WATCH OUT HE'S GOT A GUN","(⌐■_■)--︻╦╤─ - - - GET DOWN MR PRESIDENT","┻━┻︵  \(°□°)/ ︵ ┻━┻ FLIPPIN DEM TABLES","(ノಠ益ಠ)ノ彡︵ ┻━┻︵ ┻━┻ NO TABLE IS SAFE","ʕつಠᴥಠʔつ ︵ ┻━┻ HIDE YO KIDS HIDE YO TABLES","(ಠ_ಠ)┌∩┐ BYE BISH","(ง •̀_•́)ง FIGHT ME FOKER!",f"{Fore.GREEN}[¬º-°]¬  [¬º-°]¬{Fore.YELLOW}  ZOMBIES RUN!{Fore.RESET}","(╭ರ_•́) CURIOUSER AND CURIOUSER","つ ◕_◕ ༽つ つ ◕_◕ ༽つ TAKE MY ENERGY",f"༼つಠ益ಠ༽つ {Fore.RED}─=≡ΣO)){Fore.YELLOW} HADOUKEN!{Fore.RESET}"]
                    return(one_line_ascii_art_list[random.randint(0, len(one_line_ascii_art_list)-1)])
                # END NESTED FUNCTION that i should totally move 
                if cpage > len(pages_as_numbers_listed) : print(return_one_line_art()) ############### ascii art, could do if max go back to one but prefer the easter egg
                print("\n", end="PAGES ")
                #pages_print.insert(0,"PAGE NUMBERS :")
                highlight_page = lambda h : f"{Fore.BLUE}[[{Fore.CYAN} {h} {Fore.BLUE}]]{Fore.RESET}" if h == cpage else f"{Fore.BLACK}{Style.BRIGHT}[ {h} ]{Fore.RESET}{Style.RESET_ALL}" # language is so mad wtf            
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
            print("\nWell This Is Awkward...") # maybe this is bad ux tbf ??? "No... it's the children who are wrong" https://knowyourmeme.com/memes/am-i-so-out-of-touch
            fm.print_dashes()
            print("Returning To Main Menu")


    # v6 print - pagination
    def paginated_print(self, disp_size: int=22, rows: int=3, disp_str = "Enter Page Number (or use . to step forward +1 page) : ", title_str=None): #just changed rows default arg from 4 to 3 btw
        try:
            user_wants_page = 1 # initialises the loop
            # whole method is this loop, obvs not ideal 
            while user_wants_page != "0":
                a_query = f'SELECT COUNT(product_id) AS NumberOfProducts FROM products'
                the_result = get_from_db(a_query)
                len_of_items_from_db = int(the_result[0][0])
                usable_screen = int(disp_size) - 11
                ipl = usable_screen # max amounts of items that can be in one vertical line
                ipp = ipl * rows # items per page = max amount of items on the page, the vertical list multiplied by the amount of rows
                #rows = 5 # var for readability and incase wanna change for smaller sized screens not baking into equation (ik actually is cols lol) - also is now a setting btw
                full_pages = int(len_of_items_from_db / ipp) # amount of full pages (page full with items)
                remaining_items = len_of_items_from_db % ipp # amount of remainder items (amount of items in the final page if not all full)
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
                print(f"Currently {ipp} Items Per Page, {len_of_items_from_db} Total Products\n{fm.print_dashes(return_it=True)}") # note the reason to point out uses index notation is for deleting and displaying etc this is best, thats just what indexing is for, but product numbers is more like a unique identifier that isn't the name incase it was required which im sure there are irl cases for
                print(f"{Fore.BLUE}[ID] {Fore.CYAN}Product {Fore.BLACK}{Style.BRIGHT}(quantity){Style.RESET_ALL} - {Fore.GREEN}£Price{Fore.RESET}\n")
                
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
                            if x < len_of_items_from_db:
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
                
                def is_sold_out(the_product, want_colour = False): # IF YOU HAVE AN EXTRA PARAMATER HERE CAN WORK WITH COLOUR, 1 PARA DICTATES SIZE THEN NEXT FOR COLOUR 
                    if int(the_product) <= 0 and want_colour == False:
                        return("GONE")
                    elif int(the_product) <= 0 and want_colour == True:
                        return(f"{Fore.RED}GONE{Fore.RESET}")
                    elif int(the_product) <= 3 and want_colour == False:
                        return(f"ONLY {the_product}")
                    elif int(the_product) <= 3 and want_colour == True:
                        return(f"{Fore.RED}{Style.DIM}ONLY {the_product}{Fore.RESET}{Style.RESET_ALL}")
                    else:
                        return(the_product)

                # pull data from the db, yes pulls all the data from the table
                # yes would be ideal to just pull the current page (FROM products p LIMIT (ipl)) (or even the current item to print (or line whatever))
                # no not implementing here as have done elsewhere in the project
                query = f'SELECT p.product_name, p.product_price, p.product_quant, p.product_id FROM products p'
                result = list(get_from_db(query)) 
        
                for the_line in the_page: 
                    print_string = ""
                    for prdct in the_line:
                        prdct + current_page_number
                        
                        current_string = (f"{result[prdct][3]} {result[prdct][0]} {result[prdct][1]} {is_sold_out(result[prdct][2])}")
                        spaces = 49 - (len(current_string))
                        spaces_string = ""
                        if int(result[prdct][3]) == 10: # adjust for the extra character in the display by minusing one from the spaces on the end
                            spaces -= 0
                        if int(result[prdct][3]) == 100: # not needed now "index" (id) is taken directly from db
                            spaces -= 0
                        if int(result[prdct][3]) == 1000:
                            spaces -= 0
                        if int(result[prdct][3]) == 10000:
                            spaces -= 0
                        if int(result[prdct][3]) == 100000:
                            spaces -= 0
                        for x in range(spaces - 5):
                            spaces_string += " "
                        print_string += (f"{Fore.BLUE}[ {Style.DIM}{Fore.CYAN}{result[prdct][3]}{Style.RESET_ALL} {Fore.BLUE}]{Fore.RESET} {Fore.WHITE}{Style.BRIGHT}{result[prdct][0]}{Fore.RESET}{Style.RESET_ALL} {spaces_string} {Fore.BLACK}{Style.BRIGHT}({is_sold_out(result[prdct][2], want_colour=True)}{Fore.BLACK}{Style.BRIGHT}){Style.RESET_ALL} - {Fore.GREEN}£{result[prdct][1]}{Fore.RESET}       ")
                    print(print_string)
                    # yield back as tuples with index value, check as recieving yield, if index value not in the indexes that would be in the current page (0-59,60-119...)
                cpage = int((current_page_number + ipp) / ipp)
                # move this to format random
                def return_one_line_art():
                    one_line_ascii_art_list = ["̿' ̿'\̵͇̿̿\з=(◕_◕)=ε/̵͇̿̿/'̿'̿ ̿  NOBODY MOVE!","( ͡° ͜ʖ ͡°) *staring intensifies*","(╯°□°)--︻╦╤─ - - - WATCH OUT HE'S GOT A GUN","(⌐■_■)--︻╦╤─ - - - GET DOWN MR PRESIDENT","┻━┻︵  \(°□°)/ ︵ ┻━┻ FLIPPIN DEM TABLES","(ノಠ益ಠ)ノ彡︵ ┻━┻︵ ┻━┻ NO TABLE IS SAFE","ʕつಠᴥಠʔつ ︵ ┻━┻ HIDE YO KIDS HIDE YO TABLES","(ಠ_ಠ)┌∩┐ BYE BISH","(ง •̀_•́)ง FIGHT ME FOKER!",f"{Fore.GREEN}[¬º-°]¬  [¬º-°]¬{Fore.YELLOW}  ZOMBIES RUN!{Fore.RESET}","(╭ರ_•́) CURIOUSER AND CURIOUSER","つ ◕_◕ ༽つ つ ◕_◕ ༽つ TAKE MY ENERGY",f"༼つಠ益ಠ༽つ {Fore.RED}─=≡ΣO)){Fore.YELLOW} HADOUKEN!{Fore.RESET}"]
                    return(one_line_ascii_art_list[random.randint(0, len(one_line_ascii_art_list)-1)])
                # END NESTED FUNCTION that i should totally move 
                if cpage > len(pages_as_numbers_listed) : print(return_one_line_art()) ############### ascii art, could do if max go back to one but prefer the easter egg
                print("\n", end="PAGES ")
                #pages_print.insert(0,"PAGE NUMBERS :")
                highlight_page = lambda h : f"{Fore.BLUE}[[{Fore.CYAN} {h} {Fore.BLUE}]]{Fore.RESET}" if h == cpage else f"{Fore.BLACK}{Style.BRIGHT}[ {h} ]{Fore.RESET}{Style.RESET_ALL}" # language is so mad wtf            
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
            print("\nWell This Is Awkward...") # maybe this is bad ux tbf ??? "No... it's the children who are wrong" https://knowyourmeme.com/memes/am-i-so-out-of-touch
            fm.print_dashes()
            print("Returning To Main Menu")
            

    # v5 print - items per line
    def items_per_list_print(self, disp_size: int=22):
        ipl = 4 # calling my screen size (disp size) 22, calling used up lines 10 for now, so 22 - 10 = 12
        usable_screen = int(disp_size) - 11
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
        
        # pull the data from the products list 
        # unused as just realised guna use the paginated print from delete products (the only other place this is used except itself (in print submenu))
        query = f'SELECT p.product_name, p.product_price, p.product_quant FROM products p'
        result = list(get_from_db(query))  # unused, why?

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

    def save_all_products_as_csv(self, file_name:str = "z_products_list.csv"): # "x_main_products_list.csv"
        with open(file_name, "w", newline="") as csvfile:
            # set the headers for the csv
            fieldnames = ["product_number", "product_name", "price_gbp", "quantity"]
            # instruct the writer to write the headers
            writer = csv.DictWriter(csvfile, delimiter=',', fieldnames= fieldnames)
            writer.writeheader()
            query = f'SELECT * FROM products'
            result = list(get_from_db(query))  # unused, why?
            #fm.fake_input()
            # instruct the writer to write the row
            for prod in result:
                writer.writerow({"product_number":prod[0], "product_name":prod[1], "price_gbp":prod[2], "quantity":prod[3]})
            #fm.fake_input()
            #fm.fake_input()
            #for i, _ in enumerate(self.products_list):
            #    writer.writerow({"product_number":self.products_list[i].product_number, "product_name":self.products_list[i].name, "price_gbp":self.products_list[i].price_gbp, "quantity":self.products_list[i].quantity})

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

## END CLASS #############################################################################################################################################################


############################################################################# MAIN FUNCTIONS #############################################################################

## MENU FUNCTIONS ########################################################################################################################################################

def main_menu(rows=3, disp_size=22):
    user_menu_input = 1
    go_again = False
    while user_menu_input != "0":
        # This loop var either prints the menu and gets the users input, or skips the print and input and returns them to where they were (quick menu)
        if go_again != True: 
            # print the menu  
            fm.format_display(disp_size)
            print(f"{Fore.CYAN}{Style.BRIGHT}PRODUCTS MENU\n{Fore.RESET}{Style.RESET_ALL}{Fore.BLACK}{Style.BRIGHT}{fm.print_dashes(return_it=True)}{Style.RESET_ALL}\n")
            menu_string = [f"{Fore.CYAN}[ 1 ]{Fore.RESET} Create", f"{Fore.CYAN}[ 2 ]{Fore.RESET} View", f"{Fore.CYAN}[ 3 ]{Fore.RESET} Delete", f"{Fore.CYAN}[ 4 ]{Fore.RESET} Update", f"{Fore.CYAN}[ 5 ]{Fore.RESET} Settings\n", f"{Fore.BLACK}{Style.BRIGHT}{fm.print_dashes(return_it=True)}{Style.RESET_ALL}", f"{Fore.RED}[ 0 ]{Fore.RESET} Back To Main Menu",f"{Fore.BLACK}{Style.BRIGHT}{fm.print_dashes(return_it=True)}{Style.RESET_ALL}\n"] # f"{Fore.CYAN}[ 5 ]{Fore.RESET} Sexy Pagniation",
            print(*menu_string, sep="\n")
            # get users input
            user_menu_input = input("Enter Menu Selection : ")
        
        # [1] - CREATE NEW PRODUCT
        if user_menu_input == "1":
            create_new_product(disp_size) # return values are for quick menu / add again loop
            # QUICK MENU / CREATE AGAIN
            print("Quick Create Another Product?\n")
            if get_user_yes_true_or_no_false():
                go_again = True
                user_menu_input = "1"
            else:
                go_again = False

        # [2] - PRINT SUBMENU
        elif user_menu_input == "2":
            print_submenu(disp_size, rows)

        # [3] - DELETE PRODUCT
        elif user_menu_input == "3":
            delete_product_new(disp_size, rows)
                         
        # [4] - UPDATE PRODUCT (NEW)
        elif user_menu_input == "4":
            update_product_new(disp_size, rows)

        # [5] - SETTINGS SUB MENU
        elif user_menu_input == "S" or user_menu_input == "s" or user_menu_input == "5":
            disp_size, rows = settings_submenu(disp_size, rows)
        
        # [6] -
        elif user_menu_input == "6":
            pass

        # [7] -
        elif user_menu_input == "7":
            pass

        # [8] -
        elif user_menu_input == "8":
            pass

        # [9] - SEXY PAGINATED PRINT BY PRICE TEST [HIDDEN]
        elif user_menu_input == "9":
            Product.paginated_print_by_price(Product, disp_size, rows)
            print("") 
            fm.print_dashes()
            fm.fake_input()

        # [L] - LOAD (HIDDEN) - shouldnt be using either now tbf, more for use outside of this device
        elif user_menu_input == "L" or user_menu_input == "l":
            Product.load_products_via_csv()

        # [0] - QUIT THE MENU / LOOP
        elif user_menu_input == "0":
            print("Returning To Main Menu")
            break

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
        print(f"{Fore.CYAN}{Style.BRIGHT}SETTINGS SUBMENU\n{Fore.RESET}{Style.RESET_ALL}{Fore.BLACK}{Style.BRIGHT}{fm.print_dashes(return_it=True)}{Style.RESET_ALL}\n")
        menu_string = [f"{Fore.CYAN}[ 1 ]{Fore.RESET} Display - Set Screen Size", f"{Fore.CYAN}[ 2 ]{Fore.RESET} Display - Set Columns", f"{Fore.CYAN}[ 3 ]{Fore.RESET} Quick Add - 10 Default Products{Fore.BLACK}{Style.BRIGHT} [alpha]{Style.RESET_ALL}", f"{Fore.CYAN}[ 4 ]{Fore.RESET} {Fore.BLACK}{Style.BRIGHT}Quick Add - X Products [legacy]{Style.RESET_ALL}", f"{Fore.CYAN}[ 5 ]{Fore.RESET} {Fore.BLACK}{Style.BRIGHT}Load - From CSV File [legacy]{Style.RESET_ALL}\n", f"{Fore.BLACK}{Style.BRIGHT}{fm.print_dashes(return_it=True)}{Style.RESET_ALL}", f"{Fore.RED}[ 0 ]{Fore.RESET} Back To Product Menu", f"{Fore.BLACK}{Style.BRIGHT}{fm.print_dashes(return_it=True)}{Style.RESET_ALL}\n"]
        print(*menu_string, sep="\n")
        # GET THE USERS INPUT
        user_submenu_input = input("Enter Your Input : ")

    # [1] SETTINGS - FORMAT SCREEEN
        if user_submenu_input == "1":
            disp_size = format_screen(disp_size)
            fm.fake_input()

    # [2] SETTINGS - SET ROWS
        elif user_submenu_input == "2":
            rows = set_display_rows(disp_size, rows)

    # [3] QUICK ADD DEFAULT PRODUCTS
        elif user_submenu_input == "3":
            fm.format_display(disp_size)
            quick_add_ten_products(disp_size)
    
    # [4] QUICK ADD X PRODUCTS
        elif user_submenu_input == "4":
            fm.format_display(disp_size)
            print(f"Quick Add - X Products\nEnter Amount Of Products To Add (For Testing)\n{fm.print_dashes(return_it=True)}")
            inc_by = int(input("Enter Number (upto 100,000) : ")) 
            quick_add_some_products(inc_by)
            fm.fake_input()

    # [L] LOAD FROM FILE (hidden - for testing when no connection to db)
        elif user_submenu_input == "L" or user_submenu_input == "l":
            Product.load_products_via_csv()

    # [0] BACK / RETURN TO MAIN MENU
        elif user_submenu_input == "0":
            print("Returning To Products Menu")
            break
        else:
            print("Input Error - Returning To Products Menu")
            break

    print("Saving Settings...")
    return(disp_size, rows)


## PRINT SUBMENU #######################################################################################################################################################

# PUT THESE ALL INTO THEIR OWN FUNCTIONS PLSSSS
def print_submenu(disp_size, rows):
    user_submenu_input = "1"
    while user_submenu_input != "0":
        # PRINT THE SUB MENU  
        fm.format_display(disp_size)
        print(f"{Fore.CYAN}{Style.BRIGHT}PRINT SUBMENU\n{Fore.RESET}{Style.RESET_ALL}{Fore.BLACK}{Style.BRIGHT}{fm.print_dashes(return_it=True)}{Style.RESET_ALL}\n")
        menu_string = [f"{Fore.CYAN}[ 1 ]{Fore.RESET}{Style.BRIGHT} Print All Products{Style.RESET_ALL}",f"{Fore.CYAN}[ 2 ]{Fore.RESET}{Style.BRIGHT} Print All Products - By Price{Style.RESET_ALL}", f"{Fore.CYAN}[ 3 ]{Fore.RESET} {Fore.BLACK}{Style.BRIGHT}Print By Product Number - legacy{Style.RESET_ALL}", f"{Fore.CYAN}[ 4 ]{Fore.RESET} {Fore.BLACK}{Style.BRIGHT}Print By Index - legacy{Style.RESET_ALL}", f"{Fore.CYAN}[ 5 ]{Fore.RESET} {Fore.BLACK}{Style.BRIGHT}Print By Yield - legacy{Style.RESET_ALL}", f"{Fore.CYAN}[ 6 ]{Fore.RESET} {Fore.BLACK}{Style.BRIGHT}Print By One Line Generator - legacy{Style.RESET_ALL}", f"{Fore.CYAN}[ 7 ]{Fore.RESET} {Fore.BLACK}{Style.BRIGHT}Print By Items Per Line - legacy{Style.RESET_ALL}\n", f"{Fore.BLACK}{Style.BRIGHT}{fm.print_dashes(return_it=True)}{Style.RESET_ALL}", f"{Fore.RED}[ 0 ]{Fore.RESET} Back To Product Menu", f"{Fore.BLACK}{Style.BRIGHT}{fm.print_dashes(return_it=True)}{Style.RESET_ALL}\n"] 
        print(*menu_string, sep="\n")
        # GET THE USERS INPUT
        user_submenu_input = input("Enter Your Input : ")

        # [1] - SEXY PAGINATED PRINT
        if user_submenu_input == "1":
            Product.paginated_print(Product, disp_size, rows, title_str = f"{Fore.CYAN}VIEW ALL PRODUCTS{Fore.RESET}")
            print("") 
            fm.print_dashes()
            fm.fake_input()

        # [2] - SEXY PAGINATED PRINT BY PRICE ASC/DESC
        if user_submenu_input == "2":
            Product.paginated_print_by_price(Product, disp_size, rows, title_str = f"{Fore.CYAN}VIEW ALL PRODUCTS - SORTED BY PRICE{Fore.RESET}")
            print("") 
            fm.print_dashes()
            fm.fake_input()

        # [3] - SIMPLE PRINT PRODUCTS, ALL 1 VERTICAL LINE, LONG PRODUCT NUMBERS (legacy)
        if user_submenu_input == "3":
            fm.format_display(disp_size)
            print(f"Print by Product Number\n{fm.print_dashes(return_it=True)}\n")
            print(f"Amount of Products = {len(Product.products_list)}\n") # amount is length of products list, also print(f"{Product.count_products_list(Product)} Total Products") which using return value 
            Product.print_all_products_by_name(Product)
            print("")
            fm.print_dashes()
            fm.fake_input()

        # [4] PRINT BY INDEX
        elif user_submenu_input == "4":
            fm.format_display(disp_size)
            print(f"Print by Index of Object in List\n{fm.print_dashes(return_it=True)}\n")
            print(f"Amount of Products = {len(Product.products_list)}\n")
            Product.print_all_products_by_index(Product)
            print("")
            fm.print_dashes()
            fm.fake_input()

        # [5] PRINT BACK GENERATOR
        elif user_submenu_input == "5":
            fm.format_display(disp_size)
            print(f"Print by Print Formatted String From Generator\n(also uses index notation)\n{fm.print_dashes(return_it=True)}\n")
            print(f"Amount of Products = {len(Product.products_list)}\n")
            print(*(Product.yield_back_index_name_string(Product)), sep="\n")
            print("")
            fm.print_dashes()
            fm.fake_input()

        # [6] IMPROVED GENERATOR
        elif user_submenu_input == "6":
            fm.format_display(disp_size)
            print(f"Print by Print Formatted String From Generator\n(also uses index notation)\n{fm.print_dashes(return_it=True)}\n")
            print(f"Amount of Products = {len(Product.products_list)}\n")
            print(*(Product.generate_index_name_string(Product)), sep="\n")
            print("") 
            fm.print_dashes()
            fm.fake_input()

        # [7] ITEMS PER LINE
        elif user_submenu_input == "7":
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


## PYINQ UPDATE MENU ###########################################################

def update_product_new(disp_size:int, rows:int):
    Product.paginated_print(Product, disp_size, rows, disp_str = "Enter Page (step with .), To Update A Product First Hit '0' : ", title_str = f"{Fore.CYAN}UPDATE PRODUCTS{Fore.RESET}") # dashes and endl?
    print(" ")
    fm.print_dashes()
    to_update = int(input("Enter Number To Update : "))
    update_more = True
    while update_more:
        query = f'SELECT p.product_name, p.product_price, p.product_quant FROM products p WHERE product_id = {to_update}'
        result = (get_from_db(query))
        fm.format_display(disp_size)
        print_cutlery()
        print("")
        fm.print_dashes(20)
        print(f"{Fore.BLUE}[ {Style.DIM}{Fore.CYAN}{int(to_update) + 1}{Style.RESET_ALL} {Fore.BLUE}]{Fore.RESET} {Fore.WHITE}{Style.BRIGHT}{result[0][0]}{Fore.RESET}{Style.RESET_ALL}    {Fore.BLACK}{Style.BRIGHT}({result[0][2]}){Style.RESET_ALL} - {Fore.GREEN}£{result[0][1]}{Fore.RESET}       ")
        fm.print_dashes(20)
        print("")
        answer = print_pyinq(to_update)
        if answer == False:
            break    
    fm.print_dashes()
    print(f"{Fore.GREEN}Update Complete{Fore.RESET}")
    fm.print_dashes()
    fm.fake_input()


def print_cutlery():
    print("                |\          ")
    print("          ||||  | l   __    ")
    print("     |||| ||||  | l  // \   ")
    print("     |||| |  |  | l  || |   ")
    print("     |  | \  /  | l  \\  /  ")
    print("      \/   ||   | /   \/    ")
    print("      ||   ||   ||    ||    ")
    print("      ||   ||   ||    ||    ")
    print("      ||   ||   ||    ||    ")
    print("      ||   ||   ||    ||    ")
    print("      ||   ||   ||    ||    ")
    print("      \/   \/   \/    \/    ")


def validate_quant(result):
    quant_update = 0
    print_counter = 0
    while quant_update < 1:
        if print_counter > 0:
            fm.format_display() # DISP HEIGHT WOULD BE NICE - NEED TO SORT PROPER FUNCTION LAYOUT FIRST THO OBVS!
            print(f"{Fore.RED}Invalid Quantity{Fore.RESET} - Try Again")
            fm.print_dashes()
        quant_update = int(input(f"Please Enter The Updated Quantity (Current = {result[0][2]}) : "))
        print_counter += 1
    return(quant_update)


def validate_price(result): # REGEX VALIDATON BEST!!
    price_update = 0
    print_counter = 0
    while price_update < 1:
        if print_counter > 0:
            fm.format_display() # DISP HEIGHT WOULD BE NICE - NEED TO SORT PROPER FUNCTION LAYOUT FIRST THO OBVS!
            print(f"{Fore.RED}Invalid Price {Fore.RESET} - Try Again")
            fm.print_dashes()
        price_update = float(input(f"Please Enter The Updated Price (Current = £{result[0][1]}) : £"))
        print_counter += 1
    return(str(price_update))


# UPDATE QUANTITY
def update_quant_new(to_update:int):
    query = f'SELECT p.product_name, p.product_price, p.product_quant FROM products p WHERE product_id = {to_update}'
    result = (get_from_db(query))
    #quant_update = input(f"Ok How Many To Update (Current = {result[0][2]}) : ")
    quant_update = validate_quant(result)
    add_query = f'UPDATE products SET product_quant = "{int(quant_update)}" WHERE product_id = {to_update}'
    add_to_db(add_query)


# UPDATE NAME
def update_name_new(to_update:int):
    query = f'SELECT p.product_name, p.product_price, p.product_quant FROM products p WHERE product_id = {to_update}'
    result = (get_from_db(query))
    name_update = input(f"Please Enter The New Name For {result[0][0]} : ")
    add_query = f'UPDATE products SET product_name = "{name_update}" WHERE product_id = {to_update}'
    add_to_db(add_query)


# UPDATE PRICE
def update_price_new(to_update:int):
    query = f'SELECT p.product_name, p.product_price, p.product_quant FROM products p WHERE product_id = {to_update}'
    result = (get_from_db(query))
    price_update = validate_price(result)
    #price_update = input(f"Please Enter The New Price? (Current = £{str(result[0][1])}) : £")
    add_query = f'UPDATE products SET product_price = "{float(price_update)}" WHERE product_id = {to_update}'
    add_to_db(add_query)


# PYINQUIRER UPDATE MENU
def print_pyinq(to_update:int):
    questions = [ {
            'type': 'list',
            'name': 'update_product',
            'message': 'What Would You Like To Update?',
            'choices': ['Quantity', 'Price', 'Name', 'Quit'],
            'filter': lambda val: val.title()
                } ]
    query = f'SELECT p.product_name FROM products p WHERE product_id = {to_update}'
    result = (get_from_db(query))
    print(f"Updating {Fore.YELLOW}{result[0][0]}{Fore.RESET}")
    fm.print_dashes(20)
    answers = prompt(questions)
    if answers['update_product'] == 'Quantity':
        update_quant_new(to_update)
    elif answers['update_product'] == 'Price':
        update_price_new(to_update)
    elif answers['update_product'] == 'Name':
        update_name_new(to_update)    
    elif answers['update_product'] == 'Quit':
        return(False)


## DELETE - NEW ####################################################################################################################################################

def delete_product_new(disp_size, rows):
    Product.paginated_print(Product, disp_size, rows, disp_str = "Enter Page (step with .), To Delete A Product First Hit '0' : ", title_str = f"{Fore.CYAN}DELETE PRODUCTS{Fore.RESET}") # dashes and endl?
    print(" ")
    fm.print_dashes()
    to_update = int(input("Enter Number To Delete : "))
    query = f'SELECT p.product_name, p.product_price, p.product_quant FROM products p WHERE product_id = {to_update}'
    result = (get_from_db(query))
    fm.format_display(disp_size)
    print("")
    fm.print_dashes(20)
    print(f"{Fore.BLUE}[ {Style.DIM}{Fore.CYAN}{int(to_update)}{Style.RESET_ALL} {Fore.BLUE}]{Fore.RESET} {Fore.WHITE}{Style.BRIGHT}{result[0][0]}{Fore.RESET}{Style.RESET_ALL}    {Fore.BLACK}{Style.BRIGHT}({result[0][2]}){Style.RESET_ALL} - {Fore.GREEN}£{result[0][1]}{Fore.RESET}       ")
    fm.print_dashes(20)
    print("")
    print(f"{Fore.YELLOW}{result[0][0]}{Fore.RESET} Selected For Termination")
    fm.print_dashes(20)
    print("Are You Sure You Want To Un-Alive This Product?")
    print(f"{Fore.BLACK}{Style.BRIGHT}(This Process Cannot Be Undone){Fore.RESET}{Style.RESET_ALL}")
    fm.print_dashes()
    yesno = input(f"{Fore.RED}Confirm Deletion{Fore.RESET} [y/n] : ")
    if yesno == "y" or yesno == "Y":
        delete_query = f'DELETE FROM products WHERE product_id = {to_update}' # SINCE ID's CHANGE WHEN DELETION (obvs would do this properly if wasnt merging db from lots of existing work on pagination etc)
        add_to_db(delete_query)
        print("")
        fm.print_dashes()
        print(f"{Fore.RED}Product Terminated{Fore.RESET}")
        fm.print_dashes()
        fm.fake_input()
    else:
        fm.print_dashes()
        print("")
        fm.print_dashes()
        print("Deletion Cancelled")
        fm.print_dashes()
        fm.fake_input()


## CREATE NEW FUNCTIONS ############################################################################################################################################

# Create new product instance, add to db
def create_new_product(disp_size:int):
    fm.format_display(disp_size)
    len_query = f'SELECT COUNT(product_id) AS NumberOfProducts FROM products'
    len_result = get_from_db(len_query)
    print(f"{Fore.CYAN}Create New Product{Fore.RESET}\n{fm.print_dashes(return_it=True)}")
    name = input(f"Enter A Name For Product {len_result[0][0]} : ")
    price_in_pounds = get_price()
    fm.print_dashes()
    quantity = input(f"Enter The Quantity For {name.title()} : ")
    fm.format_display(disp_size)
    Product(name, price_in_pounds, quantity)
    add_query = f'INSERT INTO products (product_name, product_price, product_quant) VALUES ("{name}", "{price_in_pounds}", "{int(quantity)}")' 
    add_to_db(add_query)
    get_zeros = lambda x : "0"*(4 - len(str(x))) # yes i do realise these are supposed to be anonymous, still tryna nail them tbf
    print(f"Product #{get_zeros(len_result[0][0])}{len_result[0][0]}\n{fm.print_dashes(return_it=True)}\n{Fore.YELLOW}{name}\n{Fore.GREEN}Created Sucessfully{Fore.RESET}")
    fm.print_dashes()

    
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
    print(f"Generating Dummy Products...\n{fm.print_dashes(return_it=True)}\n")
    Product("Holy Hand Grenade",4.99,100)
    Product("Crowbar",2.99,100)
    Product("Master ball",8.50,100)
    Product("Potato GLaDOS",101.01,100)
    Product("Gravity Gun",499.99,100)
    Product("Energy Sword",54.99,100)
    Product("Pokedex",14.29,100)
    Product("Diamond Pickaxe",21.99,100)
    Product("The Golden Gun",700.00,100)
    Product("Needler",41.10,100)
    print("")
    print("10 New Dummy Products Were Added")
    print(f"{len(Product.products_list)} Products Total\n")
    fm.print_dashes()
    fm.fake_input()

def quick_add_some_products(inc_by:int):
    for i in range(inc_by):
        Product(f"A [{i}] Product",10.10,101)
    fm.format_display(30)

def format_screen(disp_size:int): 
    user_submenu_input = "1"
    while user_submenu_input != "0":
        # hl_current_page = lambda x : f"{x}" if x != disp_size else f"{Fore.GREEN}{x}{Style.DIM}{Fore.WHITE}<<{Fore.RESET}{Fore.GREEN} CURRENT SCREEN SIZE{Fore.RESET}{Style.RESET_ALL}"
        # hl_current_page = lambda x : f"{Fore.GREEN}{x}{Style.BRIGHT}{Fore.BLACK} <<{Fore.RESET}{Fore.GREEN} CURRENT SCREEN SIZE{Fore.RESET}{Style.RESET_ALL}" if x == disp_size else (f"{Fore.RED}{x}{Style.BRIGHT}{Fore.BLACK} <<{Fore.RESET}{Fore.RED} MIN SCREEN SIZE{Fore.RESET}{Style.RESET_ALL}" if x == 16 else f"{x}")
        # above was just testing if elif else in lambda (is supposed to only take if else, can be forced to take if elif else, can't take anymore tho?)
        def highlight_current_page(height_num:str):
            if height_num == disp_size: 
                return(f"{Fore.YELLOW}{height_num}{Style.BRIGHT}{Fore.BLACK} <<{Fore.RESET}{Fore.YELLOW} CURRENT SCREEN SIZE{Fore.RESET}{Style.RESET_ALL}")
            elif height_num == 16:
                return(f"{Fore.RED}{height_num}{Style.BRIGHT}{Fore.BLACK} <<{Fore.RESET}{Fore.RED} MIN SCREEN SIZE{Fore.RESET}{Style.RESET_ALL}")
            elif height_num == 28:
                return(f"{Fore.GREEN}{height_num}{Style.BRIGHT}{Fore.BLACK} <<{Fore.RESET}{Fore.GREEN} ^ RECOMMENEDED SCREEN SIZE ^{Fore.RESET}{Style.RESET_ALL}")
            elif height_num > 28:
                return(f"{Fore.GREEN}{height_num}{Fore.RESET}")
            else:
                return(height_num)

        print(*[highlight_current_page(x) for x in range(45, 6, -1)], sep="\n")
        print(f"{Fore.BLACK}{Style.BRIGHT}{fm.print_dashes(return_it=True)}{Style.RESET_ALL}")
        #print(f"Current Display Size = {disp_size} < ENSURE THESE MATCH! (remember 0 to reset)") 
        print(f"Screen Sizes : {Fore.RED}[16] {Fore.WHITE}Not Recommended, {Fore.YELLOW}[{disp_size}] {Fore.WHITE}Current Size, {Fore.GREEN}[28+] {Fore.WHITE}Recommended Size")
        print(f"{Fore.BLACK}{Style.BRIGHT}{fm.print_dashes(return_it=True)}{Style.RESET_ALL}")
        print("Use [ 0 ] To Reset The Display Counter After Adjusting The Terminal Height")
        print(f"{Fore.BLACK}{Style.BRIGHT}{fm.print_dashes(return_it=True)}{Style.RESET_ALL}")
        new_disp_size = int(input("Enter The Number For The Screen Size You Want : "))
        if new_disp_size > 0: # should make this be greater than the acceptable size but whatever
            print(f"New Screen Size = {new_disp_size}")
            return(new_disp_size)
        else:
            user_submenu_input = "1"

def set_display_rows(disp_size:int, rows: int):
    # mostly used for if you want to go pure vertical display
    if rows == 0: rows = 3 
    fm.format_display(disp_size)
    print(f"{Fore.CYAN}Choose How Many Columns To Display{Fore.RESET}")
    print(f"{Fore.BLACK}{Style.BRIGHT}{fm.print_dashes(return_it=True)}{Style.RESET_ALL}")
    print(f"Max Columns = 3\nRecommended Columns = 3\nCurrent = {rows}") # used to be 5 until price etc so updating for those changes tho no really tested, hardly worth it
    print(f"{Fore.BLACK}{Style.BRIGHT}{fm.print_dashes(return_it=True)}{Style.RESET_ALL}")
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

# [4] - UPDATE NAME (LEGACY)
        elif user_menu_input == "5":
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



# OLD NATTY LANG WHICH DO WANNA IMPLEMENT TBF BUT NO TIME THO OOF 
# (would have had time if given spec and didnt have to rewrite this 4 times from scratch but whatever is in the past now)
 
"""


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


# LEGACY DELETE

    fm.format_display(disp_size)
    print(f"Print by Print Formatted String From Generator\n(also uses index notation)\n{fm.print_dashes(return_it=True)}")
    print(f"Amount of Products = {len(Product.products_list)}")
    Product.paginated_print(Product, disp_size, rows)
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



"""