import traceback # for error reporting
#import time # for pause terminal control
#import random # for random
#import os # for system access (file names)
import logging # for logs
import format_random_v2_00 as fm # for formatting display, getting random things
#import orders_v2_08 as ordr
#import main_menu_v2_01 as mm


#############################################################################################################################################################
## LOGGER ###################################################################################################################################################
#############################################################################################################################################################


# create and configure logger
#LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
#logging.basicConfig(filename = "couriers.log",
#                                level = logging.DEBUG,
#                                format = LOG_FORMAT,
#                                filemode = "w")
#logger = logging.getLogger()



#############################################################################################################################################################
## PRINT COURIERS FUNCTIONS #################################################################################################################################
#############################################################################################################################################################


# SUBMENU - select between to print all, print paginated, search by number
#
# 1A - basic_simple_print_couriers 
#       - not used
# 1B - print_simple_couriers
#       - prints entire list (regardless of size) with simple order totals for each courier 
# 1C - print_couriers
#       - paginated couriers
#
# TO IMPROVE
#   - would like to get order totals showing total orders and "live" orders (preparing or delivering?)
#   - 1C needs refactor, too many lines of code, was complicated task and first attempt so went for profiency over effiency 


def search_couriers_and_print_selection(main_couriers_list, main_orders_list):
    fm.format_display()
    print("Search For A Courier And Get Their Order Total")
    fm.print_dashes()
    print("Enter A Number Between [ 1 ] and [ {} ]".format(len(main_couriers_list)))
    fm.print_dashes()
    courier_for_counting = input("Enter A Courier Number : ") # theres a courier selector for this in orders! (does it return courier as int? if so use it???)
    # add validation for if search out of range!
    fm.print_dashes()
    live_o = count_couriers_live_orders(return_list_of_lists_of_couriernumber_plus_orderstatus(main_orders_list), int(courier_for_counting) - 1)
    tot_o = count_couriers_live_orders(return_list_of_lists_of_couriernumber_plus_orderstatus(main_orders_list), int(courier_for_counting) - 1, False)
    if live_o > 1:
        s = "s"
    else:
        s = ""
    print("Orders For Couriers #{} [{}] = {} LIVE Order{} ({} Total)".format(courier_for_counting, get_and_return_name_from_courier_number(main_couriers_list, int(courier_for_counting) - 1), live_o, s, tot_o))
    fm.print_dashes()
    fm.fake_input()


# sub menu to display view entire list, pagination, or single search (todo single search, be easy af tho) 
def print_couriers_sub_menu(main_couriers_list, main_orders_list):
    # nested function
    def get_user_submenu_and_go():
        # could make this a while loop for if not in range get again? nah?
        users_input = input("Enter Your Selection : ")
        # [1] PRINT ALL
        if users_input == "1":
            print_simple_couriers(main_couriers_list, main_orders_list)
        # [2] SEARCH THEN PRINT    
        elif users_input == "2":
            search_couriers_and_print_selection(main_couriers_list, main_orders_list)
        # [3] PRINT PAGINATED
        elif users_input == "3":
            print_couriers(main_couriers_list, main_orders_list)
        else:
            print("Incorrect Input - Try Again")

    # main function
    fm.format_display(then_text = " PRINT COURIERS ".center(68, '-'))
    print(" Choose How To Display The Current List of Couriers ".center(68, '-'))
    print("")
    print(" [ 1 ] Print All {} Couriers".format(len(main_couriers_list)))
    print(" [ 2 ] Search By Courier Number")
    # dont show this option if there is less than 5 couriers 
    if len(main_couriers_list) >= 5:
        print(" [ 3 ] View In Pages (5 per page)")
    fm.print_dashes()
    get_user_submenu_and_go()


# [1A] BASIC AF PRINT COURIERS 
def basic_simple_print_couriers(main_couriers_list):
    fm.format_display()
    print(*main_couriers_list, sep="\n")
    fm.fake_input()


# [1B] SIMPLE PRINT COURIERS 
# prints a very simple couriers list, the entire list, with order totals 
def print_simple_couriers(main_couriers_list, main_orders_list):
    fm.format_display(then_text = " ALL COURIERS ".center(45, '-'))
    print("name                                   orders")
    print("                                 (live/total)")
    print("")
    for i, c in enumerate(main_couriers_list):
        live_o = count_couriers_live_orders(return_list_of_lists_of_couriernumber_plus_orderstatus(main_orders_list), i)
        tot_o = count_couriers_live_orders(return_list_of_lists_of_couriernumber_plus_orderstatus(main_orders_list), i, False)
        #o = get_orders_for_this_courier(main_orders_list, i)
        
        # do spaces formating here eventually
        #print("DEBUG : C = {}, length = {}".format(c, len(c)))
        spaces = 32 - len(c)
        if i + 1 >= 10 and i + 1 < 100:
            spaces -= 1
        elif i + 1 >= 100:
            spaces -= 2
        
        spaces_string = ""
        for y in range(spaces):
            spaces_string += " "
        
        display = (f"[ {i + 1} ] {c}{spaces_string}({live_o} / {tot_o})")
        print(display)
        fm.print_dashes(22)
    print("")    
    fm.fake_input()


# [1C] PAGINATED PRINT COURIERS 
# for paginated bottom display based on amount of users to display as size of list
# random note but since for this version anyway can only be 9 pages (as when 10 can't read 2 characters to get ascii, to get relevant int)
# so just divide the length of the main couriers list by 9 and that will give us the ipp (items per page)
def print_couriers(main_couriers_list, main_orders_list):
    # variables
    ipp = 5 # items per page, the amount of items to display per page (USE 10 TO TEST INITIALLY SINCE LAST PAGE STILL NOT FINALISED!)
    full_pages = int(len(main_couriers_list) / ipp) # amount of full pages (page full with items)
    remaining_items = len(main_couriers_list) % ipp # amount of remainder items (amount of items in the final page if not all full)
    is_remainder = True # if remainder page this = True, if no remainder page = False
    display_to_use = [] # list of lists of courier index per page but as display version (starts at 1 not zero) e.g. [[1,2,3,4,5][5,6,7,8,9,10] for ipp = 5]
    pages_print = [] # bottom pages display string
    pages_as_numbers_listed = [] # the amount of pages (e.g. 20 items with 5 items_per_page = [1,2,3,4], 66 items with 10 ipp = [1,2,3,4,5,6,7] (7th is the remainder which it includes here yes)
    last_page = [] # the single list with indexes of the last page (basically display_to_use but the end of it)
    
    # ig don't really need this can just do the check at the time when needed but meh
    if remaining_items != 0:
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
    # END FOR

    fm.format_display()
    print("CURRENT COURIERS                       page {}".format("1"))
    print("                                 (live/total)")
    # basically for page 1 (index page 0) since we will show page 1 first before they scroll or change pages
    # for the items (indexes as ints) in that page, print the number (item),
    # then print the name associated to the relevant index (-1 for true index) in the couriers list
    def print_page(page):
        fm.print_dashes(22)
        for item in display_to_use[page]:
            live_o = count_couriers_live_orders(return_list_of_lists_of_couriernumber_plus_orderstatus(main_orders_list), item - 1)
            tot_o = count_couriers_live_orders(return_list_of_lists_of_couriernumber_plus_orderstatus(main_orders_list), item - 1, False)

            def amount_of_spaces(): # nested, nested function - bruh
                spaces = 0

                x = len(str(main_couriers_list[item - 1]))
                if int(item) + 1 > 10 and int(item) + 1 < 99: 
                    spaces += 21 - x
                elif int(item) + 1 <= 10:
                    spaces += 22 - x
                else:
                    spaces += 20 - x
                spaces_string = ""
                for y in range(spaces):
                    spaces_string += " "
                return(spaces_string)

            print("[ {} ] {}{}   [orders : {}/{}]".format(int(item), main_couriers_list[item - 1], amount_of_spaces(), live_o, tot_o))
            fm.print_dashes(22)

    def print_final_page(page = last_page):
        # this prints from a single list, not a dicitonary as above, doesn't implicity use display_to_use so can be used for final_page (which is what its used for )
        fm.print_dashes(22)
        for item in page:
            #o = get_orders_for_this_courier(main_orders_list, item - 1)
            live_o = count_couriers_live_orders(return_list_of_lists_of_couriernumber_plus_orderstatus(main_orders_list), item - 1)
            tot_o = count_couriers_live_orders(return_list_of_lists_of_couriernumber_plus_orderstatus(main_orders_list), item - 1, False)
            chars = len(main_couriers_list[item - 1])
            if item >= 10 and item < 100:
                spaces = 2
            elif item >= 100:
                spaces = 3
            elif item < 10:
                spaces = 1
            spaces += 19 - chars

            spaces_string = ""
            for y in range(spaces):
                spaces_string += " "

            print("[ {} ] {}{}   [orders : {}/{}]".format(item, main_couriers_list[item - 1], spaces_string, live_o, tot_o))
            fm.print_dashes(22)
    
    # for the first time pass in 0 so it gets the first page duh
    print_page(0)
        
    # PAGES BOTTOM DISPLAY
    print("")
    new_pages_print = ["PAGES"]
    new_pages_print.extend(pages_print)
    print(*new_pages_print, sep = " - ")
    # can still append "current page x" to end btw!
    #pages_print.append("Pages")
    #print(*pages_print, sep = " - ")
    fm.print_dashes(22)

    user_wants_page = "1"
    current_page = 1

    while user_wants_page != "0":
        user_wants_page = input("Jump To Page ('0' to exit, '.' for next) : ")
        fm.format_display()
        if user_wants_page == ".":
            if current_page == pages_as_numbers_listed[-1]:
                print("CURRENT COURIERS                       page {}".format("1"))
                print("                                 (live/total)")
            else:
                print("CURRENT COURIERS                       page {}".format(current_page + 1))
                print("                                 (live/total)")
        else:
            print("CURRENT COURIERS                       page {}".format(user_wants_page))
            print("                                 (live/total)")
        if user_wants_page == ".":
            # if its a dot do this stuff
            if current_page == pages_as_numbers_listed[-2]:
                if is_remainder == False:
                    #print("INFO {}".format(pages_as_numbers_listed[-2]))
                    print_page(pages_as_numbers_listed[-2])
                else:
                    print_final_page()
                user_wants_page = pages_as_numbers_listed[-1]
            else:
                if current_page == pages_as_numbers_listed[-1]:
                    current_page = 0
                #END IF
                print_page(current_page) # is basically adding one since we dont minus it to match to what would be current_index
                user_wants_page = current_page + 1
        else:
            # if its not a dot do this stuff
            is_last_page = int(user_wants_page)
            if is_last_page == pages_as_numbers_listed[-1]:
                # if the page the user wanted is the same as the last page in the list (if they want the last page)
                    # IMPORTANT note in the case where it doesn't have is last page cause its not a remainder
                    # another if for (if last page is empty) then (pass the last list in display_to_use to print_final_page())
                if is_remainder == False:
                    print_page(pages_as_numbers_listed[-2])
                else:
                    print_final_page()    
            else:
            # use decimal for scroll! - if user_wants_page == "." (not implemented . yet, do also want like an "O" option for seeing attached orders)
                print_page(int(user_wants_page) - 1)
            # END IF ELSE
        
        print("")
        new_pages_print = ["PAGES"]
        new_pages_print.extend(pages_print)
        print(*new_pages_print, sep = " - ")
        fm.print_dashes(22)
        current_page = int(user_wants_page)
        

#############################################################################################################################################################
## CREATE COURIER FUNCTION ##################################################################################################################################
#############################################################################################################################################################


# [2] CREATE NEW COURIER 
def create_new_courier(main_couriers_list):
    # loop var
    add_again = True

    while add_again == True:
        initial_size_of_list = len(main_couriers_list)
        fm.print_dashes()
        fm.format_display(then_text = " CREATE NEW COURIER ".center(68, '-'))
        print(" Input The Courier's First Name To Add It To The Couriers List ".center(68, '-'))
        print("")
        #fm.print_dashes()
        users_input = input("Enter Courier's First Name : ")
        # note - here is where products list shuld check for duplicate product (and check if similar and then commit confirm!)
        if users_input == "1":
            users_input = fm.get_random_name()
            fm.print_dashes()
            print("Using Randomly Generated Name")
            fm.print_dashes()
        print("Add [ {} ] As A New Courier?".format(users_input))
        print("")
        yes_or_no = get_user_yes_true_or_no_false()
        if yes_or_no == True:
            main_couriers_list.append(users_input.title())
            fm.print_dashes()
            print("[ {} ] added to Couriers List".format(users_input.title()))
            fm.print_dashes()
            fm.fake_input()
        else:
            # if is already in display error message
            fm.print_dashes()
            print("Ok, [ {} ] NOT added to Couriers List".format(users_input.title()))
            fm.print_dashes()
            fm.fake_input()
        # for add again quick menu 
        if initial_size_of_list != len(main_couriers_list):
            # if list didn't change size, dont prompt to add again (can obvs remove this but to me it takes sense, dont display if cancelled maybe they entered the wrong menu by accident so don't show excessive prompts or displays)
            fm.format_display()
            print("QUICK MENU")
            fm.print_dashes()
            print("Add Again?")
            fm.print_dashes()
            add_again = get_user_yes_true_or_no_false()
        else:
            add_again = False
            #break
    # END WHILE
    return(main_couriers_list)


#############################################################################################################################################################
## UPDATE COURIER FUNCTION ##################################################################################################################################
#############################################################################################################################################################


# REMOVING TRY EXCEPT, see v2.14 for previous version, causing issues with testing M escape key
# [3] UPDATE EXISTING COURIER 
def update_existing_courier(main_couriers_list, main_orders_list):
    #logger.info("ENTER - update_existing_courier()\n - {}\n -{}".format(main_couriers_list, main_orders_list))

    fm.format_display(then_text = " UPDATE NEW COURIER ".center(68, '-'))
    #print(" Choose A Courier Who's Name You Want To Update ".center(68, '-'))
    #print("")
    if len(main_couriers_list) < 10:
        # this language is so nuts wtf, literally leaving here because its so nuts lol    
        print(*("[ " + str(item_index + 1) + " ] - " + list_item for item_index, list_item in enumerate(main_couriers_list)), sep="\n")    
        #does the same as these three lines, including the print statement, as its a generator/tuple comprehension? and then you unpack it in print
        #for item_index, list_item in enumerate(main_couriers_list):
            #    item_index = item_index + 1
            #    print("[{}] - {}".format(item_index, list_item))
    else:
        ipl = 5 # items per line, can change to update dynamically
        ipl = set_items_per_line(main_couriers_list)

    the_remainder = len(main_couriers_list) % ipl
    the_pages = int(len(main_couriers_list) / ipl)
    if the_remainder > 0:
        the_pages += 1
    the_spacs = the_pages * 28
    format_spaces = ""
    for m in range(the_spacs):
        format_spaces += " "

    print("UPDATE EXISTING COURIER      "+format_spaces+"[1 - {}]".format(len(main_couriers_list)))
    print("courier orders"+"   "+format_spaces+"(preping/live/total)")
    fm.print_dashes(int(the_spacs) - 24)
    print("")

    #fm.print_page_formatted_single_list(main_couriers_list, ipl)
    fm.print_page_formatted_single_list_detailed(main_couriers_list, ipl, main_orders_list) 
    #print_formatted_list(main_couriers_list, ipl)

    print("")
    fm.print_dashes()
    user_select = input("Enter Courier Number To Update (m for menu) : ") # 0 loops to the end of the list, pls fix this
    # makes M/m an initial escape key, should really add to add name below too but meh (also below should add isinstance of str but figure out how this works first)
    # handling escape key
    if (user_select == "m" or user_select == "M"):
        # if users input is not a string, or is M or m
        # quit this function and go to couriers menu
        print("Returning To Menu")
        fm.fake_input()
        return(main_couriers_list)
    # handling wrong inputs
    elif user_select == "0" or int(user_select) > len(main_couriers_list):
        print("Selection Is Invalid (out of range)")
        print("Returning To Menu")
        fm.print_dashes()
        fm.fake_input()
        return(main_couriers_list)
    # END IF
    else:
        fm.print_dashes()
        cor_ords = fm.count_couriers_live_orders(return_list_of_lists_of_couriernumber_plus_orderstatus(main_orders_list), int(user_select) -1)
        tot_cor_ords = fm.count_couriers_live_orders(return_list_of_lists_of_couriernumber_plus_orderstatus(main_orders_list), int(user_select) -1, False)
        print("You Selected Courier #{} - {}".format(user_select, main_couriers_list[int(user_select) - 1]))
        print(" - [{} LIVE Orders, {} Total Orders]".format(cor_ords, tot_cor_ords))
        fm.print_dashes()
        new_courier_name = input("Enter A New Name For [ {} ] (0 for random) : ".format(main_couriers_list[int(user_select) - 1]))
        if new_courier_name == "0":
            new_courier_name = fm.get_random_name()
            fm.print_dashes()
            print("Generating Random Name [{}]".format(new_courier_name))
            fm.print_dashes()
        # END IF
        old_courier_name = main_couriers_list[int(user_select) - 1]
        print("")
        print("Commit Confirm This Change?")
        if get_user_yes_true_or_no_false() == True:
            main_couriers_list[int(user_select) - 1] = new_courier_name
            fm.print_dashes()
            print("Courier {} UPDATED TO {}".format(old_courier_name, main_couriers_list[int(user_select) - 1]))
        else:
            fm.print_dashes()
            print("Courier {} NOT UPDATED".format(old_courier_name, main_couriers_list[int(user_select) - 1]))
        # END IF ELSE
        fm.print_dashes()
        fm.fake_input()
        return(main_couriers_list)


#############################################################################################################################################################
## DELETE COURIER FUNCTION ##################################################################################################################################
#############################################################################################################################################################


# [4] DELETE A COURIER 
def delete_selected_courier(main_couriers_list, main_orders_list):
    fm.format_display(then_text = " DELETE A COURIER ".center(68, '-'))
    print(" Choose A Courier To Delete, Get Order Info Before Deletion ".center(68, '-'))
    print("")

    # note doesn't have the same if/else top condition as update, only really kept that as it has one line print enum list

    ipl = 5 # items per line, can change to update dynamically
    # ideally dynamically decide the ipl (items per line by dividing based on the size of the list to the size of max displayable)   
    ipl = set_items_per_line(main_couriers_list)

    #fm.print_page_formatted_single_list(main_couriers_list, ipl)
    fm.print_page_formatted_single_list_detailed(main_couriers_list, ipl, main_orders_list) 
    #print_formatted_list(main_couriers_list, ipl)

    print("")
    fm.print_dashes()
    user_select = input("Enter Courier Number To Delete (m for menu): ") # 0 loops to the end of the list, pls fix this
    if (user_select == "m" or user_select == "M"):
        # if users input is not a string, or is M or m
        # quit this function and go to couriers menu
        print("Returning To Menu")
        fm.fake_input()
        return(main_couriers_list)
    else:
        fm.print_dashes()
        print("You Selected Courier #{} - {}".format(user_select, main_couriers_list[int(user_select) - 1]))
        
        cos_ords = count_couriers_live_orders(return_list_of_lists_of_couriernumber_plus_orderstatus(main_orders_list), int(user_select) -1)
        tot_cos_ords = count_couriers_live_orders(return_list_of_lists_of_couriernumber_plus_orderstatus(main_orders_list), int(user_select) -1, False)

        # if has orders then prompt, really needs to be live orders tho so implement asap
        if cos_ords > 0:
            fm.print_dashes()
            if cos_ords > 1:
                s = "s"
            else:
                s = ""
            print("This Courier Has [ {} ] LIVE Order{} - {} total".format(cos_ords, s, tot_cos_ords))
        # END IF
        fm.print_dashes()
        if tot_cos_ords > 0:
            if tot_cos_ords > 1:
                s = "s"
            else:
                s = ""
            print("Are You Sure You Want To Delete {} ({} total order{})".format(main_couriers_list[int(user_select) - 1], tot_cos_ords, s))
        else:
            print("Are You Sure You Want To Delete {} ({} total orders)".format(main_couriers_list[int(user_select) - 1], tot_cos_ords))
        print("")
        yes_or_no = get_user_yes_true_or_no_false()
        fm.print_dashes()
        if yes_or_no == True:
            print("Ok, Courier {} Deleted".format(main_couriers_list[int(user_select) - 1]))
            main_couriers_list.pop(int(user_select) - 1)
        else:
            print("Ok, Deletion Cancelled")
        fm.print_dashes()
        fm.fake_input()
        # dont think again or menu is necessary here, in theory sure but you shouldnt be mass deleting couriers should you so meh


#############################################################################################################################################################
## GET / RANDOM FUNCTIONS ###################################################################################################################################
#############################################################################################################################################################


def set_items_per_line(main_couriers_list):
    ipl = 5 # items per line, can change to update dynamically
    if len(main_couriers_list) >= 40: # some logic (still to implement properly) that gives dyanmic ipl based on amount of couriers, done but very rudimentary
        return(10)
    elif len(main_couriers_list) >= 24:
        return(8)
    elif len(main_couriers_list) > 10:
        return(5)
    else:
        return(4)
# END FUNCTION


def return_list_of_lists_of_couriernumber_plus_orderstatus(list_of_dictionaries):
    # stores the result
    final_value = []
    # loop the list of dictionaries for further individual list comprehension
    for dictionary in list_of_dictionaries:
        courier_and_status = [value for (key, value) in dictionary.items() if key == "courier_number" or key == "order_status"]
        final_value.append(courier_and_status)
    return(final_value)


def count_couriers_live_orders(list_of_lists, the_courier, want_live = True): #as in want LIVE ORDERS
    # loop the list of dictionaries for further individual list comprehension
    if want_live == True:    
        courier_and_status = [courier for (courier, status) in list_of_lists if (status == "Out For Delivery" or status == "Preparing") and courier == the_courier]
    else:
        courier_and_status = [courier for (courier, status) in list_of_lists if courier == the_courier]
    return_value = len(courier_and_status) # SAME AS return_value = courier_and_status.count(this_courier)
    return(return_value)


def get_and_return_name_from_courier_number(main_couriers_list, courier_to_count): 
    the_courier = main_couriers_list[int(courier_to_count)]
    return(the_courier)


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


def get_default_list_if_main_is_empty(main_couriers_list): 
    fm.format_display(end_with_dashes = True)
    if len(main_couriers_list) >= 1:
        print("You Already Have A Usable Couriers List")
        fm.print_dashes()
        print("Returning To Menu")
        fm.print_dashes()
        faux_input = input("Press Enter To Continue : ")
        return(main_couriers_list)
    else:
        main_couriers_list = get_default_couriers_list()
        if len(main_couriers_list) >= 1:
            print("Default List Loaded")
            fm.print_dashes()
            faux_input = input("Press Enter To Continue : ")
            return(main_couriers_list)
        else:
            return(main_couriers_list)


def get_default_couriers_list(go_live = True): # really just for testing
    #default_courier_list = ["Jesus","Mary","Jane","Joseph","Mary Jane","Sweet Baby Jesus","The Ghost Of Harambe","Sentient SmartFridge","X Æ A-12","A Super Minion","My Will To Live","Groot","Patrick Bateman","Some Videotapes","Patrick Starr","Crippling Anxiety","A Bad Sense Of Humor","Smite Yuumi Top"]
    default_courier_list = ["The Ghost Of Harambe","Sentient SmartFridge","X Æ A-12","Smite Yuumi Top","My Will To Live","Baby Groot","Patrick Bateman","Some Videotapes","Patrick Starr","Crippling Anxiety","A Bad Sense Of Humor","A Super Minion"]
    print("")
    print("No couriers found!".upper())
    fm.print_dashes()
    print("Do you want to load in the default couriers list".title())
    if go_live == True:
        print("(it will become the live list)")
    fm.print_dashes()
    temp_input = get_user_yes_true_or_no_false()
    if temp_input == True:
        return(default_courier_list)
    else:
        return([]) # an empty list


#############################################################################################################################################################
## MAIN FUNCTIONS ###########################################################################################################################################
#############################################################################################################################################################
    

def main_couriers(main_couriers_list, main_orders_list):
    # ORDERS MENU
    # INITIALISING VARIABLES
    #main_couriers_list = []
    #main_orders_list = []
    user_menu_input = 1
    try:
        # FUNCTION
        while user_menu_input != "0":
            # PRINT THE MENU & GET THE USERS INPUT
            print_couriers_menu(main_couriers_list) 
            user_menu_input = input("Enter Menu Selection : ")
            # PRINT COURIERS
            if user_menu_input == "2":
                print_couriers_sub_menu(main_couriers_list, main_orders_list)
                #print_couriers(main_couriers_list, main_orders_list)
            # CREATE NEW COURIER
            elif user_menu_input == "1":
                main_couriers_list = create_new_courier(main_couriers_list)
            # UPDATE COURIER    
            elif user_menu_input == "3":                
                main_couriers_list = update_existing_courier(main_couriers_list, main_orders_list)
            # DELETE COURIER    
            elif user_menu_input == "4":                
                delete_selected_courier(main_couriers_list, main_orders_list)
            # LOAD COURIERS
            elif user_menu_input == "9":
                main_couriers_list = get_default_list_if_main_is_empty(main_couriers_list)
            # QUIT THE MENU
            elif user_menu_input == "0":
                # randomised leaving message function here pls
                print("TODO - Randomised Leaving Messages")
                break
            # HANDLING ERRORED INPUTS
            elif int(user_menu_input) >= 5:
                error_input = ["ERROR - INPUT MORE THAN VALID RANGE","- - - - - - - - - - -","WTF Are You Doing?"]
                print(*error_input, sep="\n")
                fm.fake_input(2)
            elif int(user_menu_input) <= -1:
                error_input = ["ERROR - INPUT LESS THAN VALID RANGE","- - - - - - - - - - -","Wow, Negative Numbers Huh","You Tryna Kill Me? WTF!"]
                print(*error_input, sep="\n")
                fm.fake_input(2)
            elif user_menu_input.isdecimal() == False:
                error_input = ["ERROR - WAIT...SERIOUSLY WORDS!...BRUH!","- - - - - - - - - - -","y u do dis?"]
                print(*error_input, sep="\n")
                fm.fake_input(2)
            else:
                error_input = ["ERROR - NOT A VALID INPUT","- - - - - - - - - - -","Seriously WTF Are You Doing!?"]
                print("ERROR - NOT A VALID INPUT")
                fm.print_dashes()
                print(*error_input, sep="\n")
                fm.fake_input(2)
    except Exception as e:
        fm.print_dashes()
        print("ERROR - There Has Been A Fatal Error".upper())
        e.traceback = traceback.format_exc()
        error = 'Unhandled exception in asyn call:\n{}'.format(e.traceback)
        print(error)
        fm.print_dashes()  
    # END WHILE LOOP 
    return(main_couriers_list)


def print_couriers_menu(main_couriers_list):
    fm.print_app_name("Couriers")    
    menu_string = ["[ 1 ] to Create New Courier", "[ 2 ] to Print Couriers List", "[ 3 ] to Update Existing Couriers", "[ 4 ] to Delete Existing Couriers", "[ 9 ] to Load The Default Couriers List", "[ 0 ] for Main Menu","- - - - - - - - - - -"]
    if len(main_couriers_list) < 1:
        # if its empty don't make it look like its selectable (it still will be tho) by using the default i value ("-")
        print(*menu_string[:1], sep="\n")
        print(*menu_string[4:], sep="\n")
    else:
        print(*menu_string, sep="\n")


# DRIVER
#print_couriers_menu()
#main_couriers_list = main_couriers()
def driver():
    clist = []
    xlist= []
    main_couriers(clist,xlist)

#driver()





#############################################################################################################################################################
## VERSION HISTORY / CHANGE LOG / NOTES / SYSTEM FUNCTIONS ##################################################################################################
#############################################################################################################################################################
#
# v2.14
# - FUNCTIONALITY
#   - randomly selectable name for Update Couriers using key "0"
#   - update function completed to beta (call next (whatever name) then launch with those being a blend of no bugs, no errors (proper validation and testing), no new features (to the function))
#   - large refactoring of many functions, still lots more to do in long functions
#   - orders and live orders displays
#
# - UI/UX
#   - pagination for print couriers
#   - improved display for update and delete
#   - orders and live orders displays
#
#
########
#
#  v2.15
# - FUNCTIONALITY
#   - commit confirm added to update orders
#   - m escape key for top level delete and update couriers to escape to couriers menu
#   - more orders for testing
#   - randomise for update and new courier added and working fine
#
# - UI/UX
#   - formatting in update and delete couriers, for items 1-9 now displaying 2 spaces to adjust for options 10 and over
#   - some menu consistency additions (delete and update couriers now consistent to beta)
#
# - BUGFIXES / IMPROVEMENTS
#   - search by courier (from print) now in its own function, sub menu now more appropriate
#
#
########
#
#  v2.16
# - FUNCTIONALITY
#   - refactored print items in update and delete to be own function/s 
#       - et_items_per_line(main_couriers_list)
#       - print_formatted_list(main_couriers_list, ipl)
# 
# - now doing format and consistency?, and then products
#
#


##################### PRINT ALL FUNCTIONS
#for module_name in dir():
#    print("#"+module_name)
