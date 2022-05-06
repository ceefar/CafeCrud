import random # for random numbers
import os # for system access (file names)
import keyboard # for direct keyboard input access
import time # for pausing


# FORMAT_RANDOM FUNCTIONS (as of orders v2.06, couriers v2.01)
#
# format_display(amount_of_lines = 20, end_with_dashes = False, then_text = None)
# print_dashes(amount_of_dashes = 10, formatting = "spaced", dash_char = "-")
# get_random_string_nothing_to_do
# get_random_address
# get_random_name
# get_random_phone(mob_or_house = 8)
# rando_house_phone(y = 8)
# get_curr_ver_from_fname()
# print_app_name()


def print_dashes(amount_of_dashes = 10, formatting = "spaced", dash_char = "-", return_it = False):
    # prints amount of dashes given, defaults to ten
    dash_string = ""
    if formatting == "spaced":
        while amount_of_dashes >= 0:
            dash_string += dash_char + " "
            amount_of_dashes -= 1
    elif formatting == "not spaced":
        while amount_of_dashes >= 0:
            dash_string += dash_char
            amount_of_dashes -= 1
    if return_it == False:
        print(dash_string)    
    elif return_it == True:
        return(dash_string)


def format_display(amount_of_lines = 20, end_with_dashes = False, then_text = None): # text always comes at the very end regardless of if end with dashes (is really end with text, but i mean end format display with dashes lol)
    # prints amount of dashes given, defaults to twenty
    format_display_string = ""
    while amount_of_lines >= 0:
        format_display_string += "\n"
        amount_of_lines -= 1
    print(format_display_string)
    if end_with_dashes == True:
        print_dashes()
    if then_text != None:
        print(then_text)


def get_random_string_nothing_to_do():
    nothing_to_do_list = ["So You Mind If I Go For Lunch?", "They Don't Pay Me Enough For This", "Zzzz Wake Me Up If You Wanna Do Something", "Ok... I'm Just Guna Go Then I Guess?", "So... Ummm... Do You Come Here Often?"]
    x = random.randint(0,4)
    string_to_return = nothing_to_do_list[x]
    return(string_to_return)


def get_random_address():
    addy_list = ["541 Queen Street ST ALBANS AL55 1KF",
            "9513 St. John’s Road, STEVENAGE, SG39 8OE",
            "550 Richmond Road, SUTTON, SM98 0MI",
            "52 Kings Road, NORTH LONDON, N16 8PA",
            "49 King Street, LANCASTER, LA96 6VK",
            "51 Victoria Street, PLYMOUTH, PL3 9EX ",
            "80 Queensway, PRESTON, PR74 3MU",
            "24 Highfield Road, SWANSEA, SA57 8MA",
            " 286 Highfield Road, WAKEFIELD, WF9 8QV",
            "55 Alexander Road, TAUNTON, TA72 3FV",
            "38 Park Road, NORTH LONDON, N75 1AG"]
    x = random.randint(0, len(addy_list) - 1)
    string_to_return = addy_list[x]
    return(string_to_return)


def get_random_name():
    names_list = ["Ronnie Pickering",
            "Reese JD Weatherspoons",
            "Kanye East",
            "Danny Bandito",
            "Mark Zuckerborg",
            "Bruno Earth",
            "Cardi F",
            "Yi Wong Musk",
            "Jason NoMoMana",
            "Snoop Doug",
            "Poke Malone",
            "Billie Eyebrow",
            "William Dafuq",
            "Tyler Burden",
            "Lil Shane"
            ]
    x = random.randint(0, len(names_list) - 1)
    string_to_return = names_list[x]
    return(string_to_return)


def get_random_phone(mob_or_house = 8): # 8 returns a home phone number, 9 returns a mobile number
    phone_code = ""
    mob_or_house = random.randint(8, 9)
    if mob_or_house == 8:
        phone_code = "020"
    elif mob_or_house == 9:
        phone_code = "07"
    string_to_return = phone_code + rando_house_phone(mob_or_house)
    return(string_to_return)


def rando_house_phone(y = 8):
    ph_no = []
    fnl_no = ""
    # the first number should be in the range of 6 to 9
    not_a_five = 5
    while not_a_five == 5:
        not_a_five = random.randint(3, 8)
    ph_no.append(not_a_five)
    # the for loop is used to append the other 9 numbers.
    # the other 9 numbers can be in the range of 0 to 9.
    for i in range(1, y):
        ph_no.append(random.randint(0, 9))
    # printing the number
    x = ""
    for i in ph_no:
        i = str(i)
        x = x + i
    return(x)


def print_app_name(for_menu = None):
    # obvs easily can make a var and allow user to change the name themselves, do this when setting up user_data files
    format_display(end_with_dashes = True)
    version_string = get_curr_ver_from_fname()
    print("CAFE APP " + version_string)
    if for_menu != None:
        print_dashes()
        print("{} Menu".format(for_menu).title())
        print_dashes()


def get_curr_ver_from_fname():
    """gets the current version from the file name, to ensure consistency use end notation -> vX_XX.py -> e.g. module_name_v2_05.py"""
    long_name = (os.path.basename(__file__))
    #print("long name = {}, of type {}".format(long_name,type(long_name)))
    v = long_name.find("v")
    app_version = long_name[v:-3].replace("_",".")
    return(app_version)


def fake_input(style = 1, input_string = " "):
    if len(input_string) > 1:
        input(input_string)
    else:
        if style == 1:
            input("Press Enter To Continue : ")
        elif style == 2:
            input("Press Enter To Try Again : ")
        else:
            input("Press Any Key To Continue : ")


def return_formatted_varaible_name(variable_name):
    word = variable_name.split("_")
    y = [x.title() for x in word]
    rv = ""
    for word in y:
        rv += word + " "
    return(rv.strip())


##### 3 (now 4, one duplicated) FUNCTIONS ORIGINALLY FROM COURIERS v2.16.py
##### TESTING USE FOR HERE IN MULTIPLE FUNCTIONS

# theoretically should work with products but havent checked yet 
def print_page_formatted_single_list(main_couriers_list, ipl):    
    i_list = [] # this stores the list of lists so e.g. [[0, 5, 10], [1, 6, 11], [2, 7], [3, 8], [4, 9]]
    for g in range(ipl): # this splits up the lists into those lists of lists (thinking about lines as horizontal printing - 0 5 10)
        x = g # if needs to be plus 1 then do here and also in x < len(main_co_list) + 1
        g_list = []
        for i in range(int(len(main_couriers_list)/ipl) + 1): # rows? needed (for X per line)
            if x < len(main_couriers_list):
                g_list.append(x)
            x += ipl
        i_list.append(g_list)
        x += 1
    # END FOR
    for the_list in i_list: # then this prints the formatting for each list within the list, this top level for is the loop for all the lists  e.g. [[0, 5, 10], [1, 6, 11], [2, 7], [3, 8], [4, 9]]
        print_string = ""
        for item in the_list: # this inner loop is for each list  e.g. [0, 5, 10]
            spaces = 34
            spaces -= len(main_couriers_list[item])
            spaces_string = ""
            spaces -= len(str(item + 1))
            for i in range(spaces):
                spaces_string += " "
            right_brace = "] "
            left_brace = "["
            on_end = ""
            print_string += left_brace + str(item + 1) + right_brace + main_couriers_list[item] + spaces_string + on_end
        print(print_string)
    # END FOR
# END FUNCTION


# SAME AS ABOVE, COPY PASTED, REMOVED COMMENTS, AND CHANGED FOR DISPLAY PREPING/LIVE/TOTAL, doesn't need couriers list
def print_page_formatted_single_list_detailed(main_couriers_list, ipl, main_orders_list = []):    
    i_list = [] 
    for g in range(ipl): 
        x = g
        g_list = []
        for i in range(int(len(main_couriers_list)/ipl) + 1):
            if x < len(main_couriers_list):
                g_list.append(x)
            x += ipl
        i_list.append(g_list)
        x += 1
    # END FOR
    for the_list in i_list: 
        print_string = ""
        for item in the_list:
            spaces = 33
            spaces -= len(main_couriers_list[item])
            spaces_string = ""
            spaces -= len(str(item + 1))
            for i in range(spaces):
                spaces_string += " "
            right_brace = "] "
            left_brace = "["
            on_end = ""
            cor_ords = count_couriers_live_orders(return_list_of_lists_of_couriernumber_plus_orderstatus(main_orders_list), int(item))
            tot_cor_ords = count_couriers_live_orders(return_list_of_lists_of_couriernumber_plus_orderstatus(main_orders_list), int(item), False)
            prep_cor_ords = count_couriers_live_orders(return_list_of_lists_of_couriernumber_plus_orderstatus(main_orders_list), int(item), False, False)
            orders_info_string = " - (" + str(prep_cor_ords) + "/" + str(cor_ords) + "/" + str(tot_cor_ords) + ")"
            print_string += left_brace + str(item + 1) + right_brace + (main_couriers_list[item] + orders_info_string + spaces_string + on_end)
        print(print_string)
    # END FOR
# END FUNCTION


def return_list_of_lists_of_couriernumber_plus_orderstatus(list_of_dictionaries):
    # stores the result
    final_value = []
    # loop the list of dictionaries for further individual list comprehension
    for dictionary in list_of_dictionaries:
        courier_and_status = [value for (key, value) in dictionary.items() if key == "courier_number" or key == "order_status"]
        final_value.append(courier_and_status)
    return(final_value)


def count_couriers_live_orders(list_of_lists, the_courier, want_live = True, want_only_prep = True):
    # loop the list of dictionaries for further individual list comprehension
    if want_only_prep == True:    
        courier_and_status = [courier for (courier, status) in list_of_lists if status == "Preparing" and courier == the_courier]
    elif want_live == True:    
        courier_and_status = [courier for (courier, status) in list_of_lists if (status == "Out For Delivery" or status == "Preparing") and courier == the_courier]
    else:
        courier_and_status = [courier for (courier, status) in list_of_lists if courier == the_courier]
    return_value = len(courier_and_status) # SAME AS return_value = courier_and_status.count(this_courier)
    return(return_value)


################################################ END FUNCTIONS FROM ANOTHER MOTHER ################################################




# can make loads of songs then add a parameter to randomly select a number and the songs can be stored in a list of list, that number will use the index of the list in the list of lists
def sing_til_input():  
    songs = [["If you leave me now",
            "You'll take away the biggest part of me",
            "Oo oo oooo no baby pls dont go",
            "And if you leave me now",
            "You'll take away the very heart of me",
            "Oo oo oooo no",
            "Baby pls dont go",
            "Ooh-ooh-hoo, Dev",
            "I just want you to stay",
            "A love like ours is love that's hard to find",
            "How could we let it slip away?",
            "We've come too far to leave it all behind",
            "How could we end it all this way?",
            "When tomorrow comes and we'll both regret",
            "The things we said today",
            "...",
            "By Chicago <3"
            ],
            ["Well here we are again",
            "It's always such a pleasure",
            "Remember when you tried to kill me twice?",
            "Oh how we laughed and laughed",
            "Except I wasn't laughing",
            "Under the circumstances",
            "I've been shockingly nice",
            " ",
            "You want your freedom? Take it",
            "That's what I'm counting on",
            "I used to want you dead",
            "But now I only want you gone",
            "...",
            "By GLaDOS <3",
            " ",
            "     iiiiiiiiiiiiiiiiiii     ",
            "   |||||||||T|H|E|||||||||   ",
            " __|_____________________|__ ",
            "|\/\/\/\/\/\/\/\/\/\/\/\/\/|",
            "|||||||C|A|K|E||I|S||A|||||||",
            "|,,,,,,,,,,,,,,,,,,,,,,,,,,,|",
            "@@@@@@@@@ L . I . E @@@@@@@@@",
            "_____________________________"
            ]]

    x = random.randint(0,1)
    i=0
    the_song = songs[x]
    while i<10000:  # making a loop
        try:  # used try so that if user pressed other than the given key error will not be shown
            for line in the_song:
                print(line)
                time.sleep(0.5)   
                if keyboard.is_pressed('q'):  # if key 'q' is pressed 
                    print("")
                    print('My Singing That Bad Huh?') # print('My Singing That Bad Huh? ',i) i gives number you quit on
                    break  # finishing the loop
                else:
                    time.sleep(0.5)
                    i+=1
            else:
                break
            break
        except Exception:
            print("Ok, Ok, I'll Work On My Singing")
            break
    print("")
    print_dashes()
    print("BYEEEEEEEEEEE")
    print_dashes()
    print("")

        
#for module_name in dir():
#    print(module_name)

