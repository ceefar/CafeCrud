# IMPORTS
# db
import pymysql
import os
from dotenv import load_dotenv
# general
import format_random_v2_00 as fm
import re # from re import match - why doesnt this work wtf?
import random
import pickle
import csv
# styling
import colorama
from colorama import Fore, Back, Style
from PyInquirer import prompt, Separator

# initialise colorama
colorama.init(autoreset=True)

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


def read_from_db(): # should really be called print from db and reeeeeeally shouldnt be using this lmao
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

    # CSV CONSTRUCTOR
    @classmethod
    def csv_constructor(cls, name:str, phone_number:str, location:str, courier_id:int = None, availability:list = []):
        # could strip them all here tbf (especially a to be sure and b because they probably do need it?)
        # TEST BY, check print (shouldnt print if not in global list), then do cls.append here to see if that works, THEN and regardless, just use actually constructor in the load loop lmao!
        return cls(name, phone_number, location, courier_id, availability)


## PRINT ################################

    # PRINT COURIERS - basic formatting, one line generator 
    def generate_index_name_string(self):
        return((f"{i+1}. {cr.name} (#{cr.courier_id}) {cr.location} {cr.phone_number}") for i,cr in enumerate(self.couriers_list))

## DELETE ###############################

# DELETE
    def select_and_delete(self, to_delete:int, mass_delete:bool =False): 
        if mass_delete: # implement more guard clauses
            z = len(Couriers.couriers_list) - to_delete
            del self.couriers_list[z:] 
        else:
            def get_zeros(x): return("0"*(4 - len(str(x))))
            cr = self.couriers_list[to_delete - 1]
            x = random.randint(1,10)
            if x >= 3:
                print(f"Deleting Courier #{get_zeros(cr)}{cr.courier_id} - {cr.name}")
            else:
                print(f"Deleting {self.couriers_list[to_delete - 1]}")
                print("yeah... no taking that one back")
            del self.couriers_list[to_delete - 1]
        # obvs dont do this lol (fun easter egg - have it happen randomly like once in every X, rare enough that it doesnt happen first time tho?)

## UPDATE ###############################

    # UPDATE COURIERS - attempting via loop sent the_key to update appropriate the_value
    def update_attr_by_key(self, to_update:int, the_key, disp_size): 
        current_value = getattr(self.couriers_list[to_update - 1], the_key)
        print(f"Prompt For {the_key}") # already have a function that will convert this to a "nice" name 
        if the_key == "name":
            new_value = get_name(disp_size)# send existing value so can display it beforehand? int(input(f"Update {current_value} To : "))
        elif the_key == "phone_number":
            new_value = get_mobile(disp_size) #get_price(self.products_list[to_update - 1].name)
        elif the_key == "location":
            new_value = get_location_from_list(disp_size)
        setattr(self.couriers_list[to_update-1], the_key, new_value)
        print(f"UPDATE couriers SET {the_key} = '{new_value}' WHERE courier_db_id = {int(to_update-1)}")
        add_to_db(f"UPDATE couriers SET {the_key} = '{new_value}' WHERE courier_db_id = {int(to_update)}")
        
        print(f"{the_key} Updated To {new_value}")

## SAVE LOAD ###############################
    
    ## PICKLES

    def save_objs_via_pickle(self):
        with open("x_main_couriers_pickle", "wb") as f:
            pickle.dump(len(self.couriers_list), f)
            for courier in self.couriers_list:
                pickle.dump(courier, f)
        # end context manager

    def load_via_pickle():
        data2 = []
        with open("x_main_couriers_pickle", "rb") as f:
            for _ in range(pickle.load(f)):
                data2.append(pickle.load(f))
        print(f"printing : {Couriers.couriers_list}")
        fm.fake_input()
        Couriers.couriers_list = data2
        #print(Couriers.couriers_list)

    ## CSVs

    def save_all_products_as_csv(self, file_name:str = "x_main_couriers_list.csv"):
        with open(file_name, "w", newline="") as csvfile:
            # set the headers for the csv            
            fieldnames = ["courier_id", "name", "phone_number", "location", "availability"] # name:str, phone_number:str, location:str, courier_id:int, availability:list
            # instruct the writer to write the headers
            #writer = csv.DictWriter(csvfile, delimiter=',')
            writer = csv.DictWriter(csvfile, delimiter=',', fieldnames= fieldnames)
            #writer.writeheader()
            # instruct the writer to write the row
            for i, _ in enumerate(self.couriers_list):
                writer.writerow({"courier_id":self.couriers_list[i].courier_id, "name":self.couriers_list[i].name, "phone_number":self.couriers_list[i].phone_number, "location":self.couriers_list[i].location, "availability":self.couriers_list[i].availability})


    def load_couriers_via_csv():
        templist = []
        # open csv and read as string
        with open("x_main_couriers_list.csv", "r") as file:
            reader = csv.reader(file, delimiter=",")
            for row in file:
                templist.append(row.strip())
                print(f"{row} LOADED SUCCESSFULLY")
        fm.format_display()
        #templist.pop(0) # pops the header off the temp list
        #Couriers.couriers_list = templist
        for index in range(len(templist)):
            x = templist[index].split(",")
            Couriers.csv_constructor(x[1], x[2], x[3], int(x[0]), x[4]) ## DUH TO TEST THIS WORKS PUT THAT CONVERT TO INT IN THE CSV CONSTRUCTOR (or duhhhhh DO THE SPLIT LOOP THERE JUST TO TEST ANYWAYS AND GIVE IT THE WHOLE TEMP LIST (then do the return loop in there and its sick, THEN could convert it to a generator and THEN ill finally figure out how to use that pickle generator lol)


## END CLASS #####################################################################################################################################################

####### NEW PRINT TEST
#"""
    # paginated print from products
    def paginated_couriers_print(disp_size: int=22, rows: int=3, disp_str = "Enter Page Number (or use . to step forward +1 page) : ", title_str=None): #just changed rows default arg from 4 to 3 btw
        try:
            user_wants_page = 1 # initialises the loop
            # whole method is this loop, obvs not ideal 
            while user_wants_page != "0":
                a_query = f'SELECT COUNT(courier_db_id) AS NumberOfCouriers FROM couriers'
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
                print(f"{Fore.BLUE}[ID] {Fore.CYAN}Courier {Fore.BLACK}{Style.BRIGHT}Location{Style.RESET_ALL} - {Fore.GREEN}[Phone Number]{Fore.RESET}\n")
                
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
                


                # pull data from the db, yes pulls all the data from the table
                # yes would be ideal to just pull the current page (FROM products p LIMIT (ipl)) (or even the current item to print (or line whatever))
                # no not implementing here as have done elsewhere in the project
                query = f'SELECT c.courier_db_id, c.name, c.location, c.phone_number FROM couriers c'
                result = list(get_from_db(query)) 
        
                for the_line in the_page: 
                    print_string = ""
                    for courr in the_line:
                        courr + current_page_number
                        
                        current_string = (f"{result[courr][3]} {result[courr][0]} {result[courr][1]} {(result[courr][2])}")
                        spaces = 49 - (len(current_string))
                        spaces_string = ""
                        if int(result[courr][3]) == 10: # adjust for the extra character in the display by minusing one from the spaces on the end
                            spaces -= 0
                        if int(result[courr][3]) == 100: # not needed now "index" (id) is taken directly from db
                            spaces -= 0
                        if int(result[courr][3]) == 1000:
                            spaces -= 0
                        if int(result[courr][3]) == 10000:
                            spaces -= 0
                        if int(result[courr][3]) == 100000:
                            spaces -= 0
                        for x in range(spaces - 5):
                            spaces_string += " "
                        print_string += (f"{Fore.BLUE}[ {Style.DIM}{Fore.CYAN}{result[courr][0]}{Style.RESET_ALL} {Fore.BLUE}]{Fore.RESET} {Fore.WHITE}{Style.BRIGHT}{result[courr][1]}{Fore.RESET}{Style.RESET_ALL} {spaces_string} {Fore.BLACK}{Style.BRIGHT}({(result[courr][2])}{Fore.BLACK}{Style.BRIGHT}){Style.RESET_ALL} - {Fore.GREEN}£{result[courr][3]}{Fore.RESET}       ")
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
#"""


# TEST DB PRINT ##########################################################################################################################################################


def db_print_test(disp_size: int=22, rows = 3):
    usable_screen = int(disp_size) - 10
    ipl = usable_screen
    length_of_couriers = get_from_db(f'SELECT * FROM couriers')
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
    query = f'SELECT * FROM couriers LIMIT {ipl}'
    print(f"{disp_size = }")
    print(f"{rows = }")
    while want_more_print: 
        #query = query
        result = get_from_db(query)
        for courier in result:
            x = f"{courier[0]} ] - {courier[1]} - {courier[3]} [0{courier[2]}"
            current_str = len(x)
            spaces = 55 - current_str
            spaces_string = ""
            for x in range(spaces):
                spaces_string += " "
            #print(courier)
            if dont_print:
                pass
                #print("You've Entered The Wrong Page Number")
            else:
                print(f"[ {courier[0]} ] {courier[1]} {spaces_string} {courier[3]} - [0{courier[2]}]")

        fm.print_dashes()
        print("")    
        print(pages_display)

        #highlight_page = lambda h : f"[[ {h} ]]" if h == cpage else f"[ {h} ]" # language is so mad wtf            
        #print(*[highlight_page(p) for p in pages_as_numbers_listed])
        
        paginate_action = (input("Enter A Page Number Or 0 To Quit : "))
        #print(current_page)
        #print(final_page)
        #print(paginate_action)
        fm.print_dashes()
        g = (int(paginate_action))
        if g > final_page:
            fm.format_display(disp_size)
            return_one_line_art()
            current_page = int(paginate_action)
            dont_print = True
        elif paginate_action != "0":
            fm.format_display(disp_size)
            current_page = int(paginate_action)
            query = f'SELECT * FROM couriers WHERE courier_db_id > {(current_page - 1) * ipl} LIMIT {ipl}'
            dont_print = False
        else:
            #fm.format_display(disp_size)
            print("Ok Bye")
            want_more_print = False



## DELETE COURIER FUNCTIONS #######################################################################################################################################################


def delete_courier(disp_size):
    fm.format_display(disp_size)
    print(f"Delete A Courier\n{fm.print_dashes(return_it=True)}")
    print(*(Couriers.generate_index_name_string(Couriers)), sep="\n")  
    to_delete = int(input(f"{fm.print_dashes(return_it=True)}\nEnter Number To Delete : "))
    fm.format_display(disp_size)
    # NEED COMMIT CONFIRM AND AN ESCAPE CHARACTER (0/m) pls & validatio that it is a valid number duh!!!!
    Couriers.select_and_delete(Couriers, to_delete)
    fm.print_dashes()


def delete_mass_couriers(disp_size):
    fm.format_display(disp_size)
    print(f"Deletes X Couriers From The Bottom Of The List\n(for testing purposes)\n{fm.print_dashes(return_it=True)}")
    print(*(Couriers.generate_index_name_string(Couriers)), sep="\n")  
    to_delete = int(input(f"{fm.print_dashes(return_it=True)}\nEnter Amount To Delete : "))
    fm.format_display(disp_size)
    # NEED COMMIT CONFIRM AND AN ESCAPE CHARACTER (0/m) pls & validatio that it is a valid number duh!!!!
    Couriers.select_and_delete(Couriers, to_delete, True)
    fm.print_dashes()


## UPDATE COURIER FUNCTIONS #######################################################################################################################################################


def update_courier(disp_size):
    fm.format_display(disp_size)
    print(*(Couriers.generate_index_name_string(Couriers)), sep="\n")
    #db_print_test()
    to_update = int(input("Enter A Number To Update")) # 0 escape key pls)
    keys_list = ["name", "phone_number", "location"]
    for the_key in keys_list:
        fm.format_display()
        if get_user_yes_true_or_no_false(before_text=f"Want To Update {the_key.replace('_',' ').title()}?\n{fm.print_dashes(return_it=True)}"): # ig this is a great example of good code, needed 1 additional line to add an amazing amount of functionality, going from just looping all the attributes and forcing the user to change them, to commit confirm with relevant information displayed beforehand, again 1 line, and as an easy addition, not preplanned per se, but more implementing good habits consistently so things do "just work"
            Couriers.update_attr_by_key(Couriers, to_update, the_key, disp_size)
    #print(f"Courier #{getattr(Couriers.couriers_list[to_update-1], 'courier_id')} Successfully Updated")
    #try:
    #    for the_key in keys_list:
    #        print(f"{the_key.replace('_',' ').title()} : {getattr(Couriers.couriers_list[to_update], the_key)}")
    #except IndexError:
    #    print("Blame The Database Not Me Jeez")
    fm.print_dashes()
    fm.fake_input()
    

## CREATE NEW COURIER FUNCTIONS ###############################################################################################################################################


def create_new_courier(disp_size):  # v2 validation, from inherent calls = needs testing + try except to be acceptable
    """Create new courier by calling appropriate functions (for validatoin) then creating new instance with the validated inputs"""
    fm.format_display(disp_size)
    name = get_name(disp_size, True)
    phone_number = get_mobile(disp_size, name)
    location = get_location_from_list(disp_size, name, phone_number)
    Couriers(name.strip(), str(phone_number), str(location))
    fm.format_display()
    get_zeros = lambda x : "0"*(4 - len(str(x)))
    cr = Couriers.couriers_list[-1] # the instances's address in memory
    add_new_courier_to_db(name,int(phone_number),location,int(cr.courier_id))
    print(f"{cr.name.title()} - Created Sucessfully\n{fm.print_dashes(return_it=True)}\nCourier #{get_zeros(cr.courier_id)}{cr.courier_id}\nLocation : {cr.location}\nMobile : {cr.phone_number}")
    fm.print_dashes()


def get_name(disp_size, first_run = False):  # v2 validation = needs try except to be acceptable
    """Get and return name of courier with simple regex validation, not used for update but should refactor for this?"""
    invalid_name = True
    name_is_good = lambda x : re.match(r"[A-Za-z]{2,25}|\s|\.|[a-zA-Z]|[A-Za-z]{1,25}\w$", x) # actually wrote this myself so do think it works but also i mean fuck knows \D[a-zA-Z]+($\s{1}|.)
    while invalid_name:
        fm.format_display(disp_size)
        if first_run: print(f"Create New Courier\n{fm.print_dashes(return_it=True)}\n")
        name = input("Enter Name (1 or 2 words, no special characters) : ")
        if name_is_good(name):
            print(f"Name [{name}] Validated")
            break
        else:
            print("Try Again")
    return(name)


def get_location_from_list(disp_size, name=None, phone_number=None): # if take locations can create new function to update them (add/remove/rename), v3 validation = acceptable
    locations_list = ["London","Manchester","Birmingham","Bristol","Nottingham","Sheffield","Leeds","Newcastle"]
    fm.format_display(disp_size)
    while locations_list:
        wrong_val = False # in loop else doesnt reset display error info accurately
        if name is not None and phone_number is not None: # when comparing to None always use comparison not equality 
            print(f"{fm.print_dashes(return_it=True)}\nName : {name}\nMobile : {phone_number}\n{fm.print_dashes(return_it=True)}\n")
        print(f"Choose Location For Courier\n{fm.print_dashes(return_it=True)}") 
        print(*(f"[{i+1}] - {location}" for i, location in enumerate(locations_list)), sep="\n")
        try:
            user_code = int(input(f"{fm.print_dashes(return_it=True)}\nSelect A Location : "))
        except ValueError:
            wrong_val = True
        if user_code > len(locations_list) or user_code <= 0: # possible edge case * (tbc)
            fm.format_display(disp_size)
            if wrong_val:
                print("Try Again - Wrong Value\n")
            else:
                print("Try Again - Wrong Selection\n")
        else:
            break
    #END WHILE
    return(locations_list[user_code - 1])
    

def get_mobile(disp_size, name:str = None): # v2 validation = needs try except to be acceptable
    invalid_mob = True
    mob_is_good = lambda x : re.match(r"^(07\d{8,12}|447\d{7,11})$", x) # lambda lets us keep expression outside of loop, allows 07 start or 447 start but not +
    while invalid_mob:
        fm.format_display(disp_size, True)
        if name: # not equal to none?
            print(f"Name : {name}\n{fm.print_dashes(return_it=True)}\n") # else print dashes?
        num = input("Enter Valid UK Mobile Number (no + symbol) : ")
        if mob_is_good(num):
            print("Number Validated")
            break
        else:
            print("Try Again")
    return(num)


def add_new_courier_to_db(name:str,phone:int,locate:str,uwuid:int):
    query = f'INSERT INTO couriers (name, phone_number, location, courier_uuid) VALUES ("{name}",{phone},"{locate}",{uwuid})'
    add_to_db(query)


## MAIN MENU FUNCTIONS #######################################################################################################################################################


def main(rows=3, disp_size=22): 
    #disp_size = 20
    #rows = 3
    menu_string = [f"COURIERS v3.01\n(using object oriented principles)\n{fm.print_dashes(return_it=True)}\n","[ 1 ] Create New", "[ 2 ] Print All Couriers", "[ 3 ] Update Courier", "[ 4 ] Delete A Courier", "[ 5 ] Mass Delete Couriers", "[ - ] -", "[ 8 ] Quick Add 30", "[ 9 ] Test Paginated Print", "[ S ] -", "[ L ] -", "[ 0 ] Quit\n","- - - - - - - - - - -"]
    user_menu_input = 1
    print_again = True
    while user_menu_input != "0":
        if print_again: # for quick menu, returns the user to their place in this switch statement without printing the menu again
            # PRINT THE MENU & GET MENU INPUT  
            fm.format_display(disp_size)
            #print(f"display size = {disp_size}")
            #print(f"display size = {rows}")
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
            fm.format_display(disp_size)
            db_print_test(disp_size, rows)
            print(f"display size = {disp_size}")
            print(f"display size = {rows}")
            #print(*(Couriers.generate_index_name_string(Couriers)), sep="\n")
            fm.fake_input()

        # [3] UPDATE COURIERS (need to do as submenu?)
        elif user_menu_input == "3":
            update_courier(disp_size)
            
        # [4] DELETE SINGLE COURIER  
        elif user_menu_input == "4":
            delete_courier(disp_size)
            # QUICK MENU / DELETE AGAIN
            print("Quick Delete Another Courier?")
            if get_user_yes_true_or_no_false():
                print_again = False
                user_menu_input = "4"
            else:
                print_again = True

        # [5] DELETE MASS COURIERS  
        elif user_menu_input == "5":
            delete_mass_couriers(disp_size)

        # [6] DB TEST READ
        elif user_menu_input == "6":
            read_from_db()
            fm.fake_input()

        # [7] DB GET TEST
        elif user_menu_input == '7':
            db_print_test(disp_size, rows)
            fm.fake_input()

        # [8] - QUICK ADD 30
        elif user_menu_input == "8":
            quick_add_30_couriers()

        # [9] - TESTING
        elif user_menu_input == "9":
            Couriers.paginated_couriers_print(disp_size, rows)

        # [S] SETTINGS SUB MENU
        elif user_menu_input == "S" or user_menu_input == "s":
            return_one_line_art()

        # [L] L - LOAD (HIDDEN)
        elif user_menu_input == "L" or user_menu_input == "l":
            print("load all")
            #Couriers.load_via_pickle()
            fm.fake_input()
        
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
    Couriers.save_all_products_as_csv(Couriers)
    Couriers.save_objs_via_pickle(Couriers)
    print("SAVING...")
    return(rows, disp_size)


## OTHER FUNCTIONS #######################################################################################################################################################


def get_user_yes_true_or_no_false(before_text:str = "", after_text:str = ""):
    # needs try except validation probably as tho this should cover some cases it won't cover all/enough?
    print(f"{before_text}\n[ 1 ] = Yes\n[ 2 ] = No\n{after_text}")
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


# can also use this for excepts/errors tbf lol
def return_one_line_art():
    one_line_ascii_art_list = ["̿' ̿'\̵͇̿̿\з=(◕_◕)=ε/̵͇̿̿/'̿'̿ ̿  NOBODY MOVE!","( ͡° ͜ʖ ͡°) *STARING INTENSIFIES*","(╯°□°)--︻╦╤─ - - - WATCH OUT HE'S GOT A GUN","(⌐■_■)--︻╦╤─ - - - GET DOWN MR PRESIDENT","┻━┻︵  \(°□°)/ ︵ ┻━┻ FLIPPIN DEM TABLES","(ノಠ益ಠ)ノ彡︵ ┻━┻︵ ┻━┻ NO TABLE IS SAFE","ʕつಠᴥಠʔつ ︵ ┻━┻ HIDE YO KIDS HIDE YO TABLES","(ಠ_ಠ)┌∩┐ BYE BISH","(ง •̀_•́)ง FIGHT ME FOKER!","[¬º-°]¬  [¬º-°]¬ ZOMBIES RUN!","(╭ರ_•́) CURIOUSER AND CURIOUSER","つ ◕_◕ ༽つ つ ◕_◕ ༽つ TAKE MY ENERGY","༼つಠ益ಠ༽つ ─=≡ΣO)) HADOUKEN!"]
    print(one_line_ascii_art_list[random.randint(0, len(one_line_ascii_art_list)-1)])


if __name__ == "__main__":
    # DRIVER
    Couriers.load_couriers_via_csv()
    the_rows = 3
    the_display = 22
    main(the_rows, the_display)





