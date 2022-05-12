import version_storage_orders.orders_v2_10 as ord
import version_storage_couriers.couriers_v2_17 as cour
import format_random_v2_00 as fm # for formatting display, getting random things
import json
import time



def load_all():
    # main_couriers_list = []
    main_couriers_list = load_default_couriers_list_to_global()
    if len(main_couriers_list) < 1:
        main_couriers_list = cour.get_default_couriers_list()
    main_orders_list = load_orders_json_simple()
    if len(main_couriers_list) < 1:
        # if list is empty, load the default list
        main_orders_list = ord.get_default_order_list()
    #print(main_orders_list)
    fm.format_display()
    main_menu(main_couriers_list, main_orders_list)


def main_menu(main_couriers_list, main_orders_list):
    user_menu_input = 1
    while user_menu_input != "0":
        # PRINT THE MENU & GET THE USERS INPUT
        print_main_menu() 
        user_menu_input = input("Enter Menu Selection : ")
        # GO TO COURIERS
        if user_menu_input == "1":
            main_couriers_list = cour.main_couriers(main_couriers_list, main_orders_list)
        # GO TO ORDERS
        elif user_menu_input == "2":
            main_orders_list = ord.main_orders(main_couriers_list, main_orders_list)
        elif user_menu_input == "3":
            main_couriers_list = cour.print_couriers(main_couriers_list)
        elif user_menu_input == "4":
            main_couriers_list = ord.print_orders(main_orders_list)
        elif user_menu_input == "0":
            break
        else:
            print("Some Wrong Input Error Message")
    # END WHILE
    print("SAVING...")
    fm.print_dashes()
    save_entire_couriers_list_simple(main_couriers_list)
    time.sleep(0.5)
    print("COURIERS LIST SAVED...")
    time.sleep(0.5)
    save_orders_list(main_orders_list)
    print("ORDERS LIST SAVED...")
    time.sleep(0.5)
    fm.print_dashes()
    print("CLOSING APPLICATION...")
    print("")
    fm.sing_til_input()
    #print("GOODBYE...\n")
    # goodbye messsage



def print_main_menu():
    fm.print_app_name("MAIN")
    #menu_string = ["[ 1 ] for Couriers", "[ 2 ] for Orders", "[ 3 ] to Print Couriers", "[ 4 ] to Print Orders", "[ 0 ] to Quit","- - - - - - - - - - -"]
    menu_string = ["[ 1 ] for Couriers", "[ 2 ] for Orders", "[ 0 ] to Quit","- - - - - - - - - - -"]
    print(*menu_string, sep="\n")



def load_orders_json_simple():
    with open('x_main_orders_list.json') as f:
        g = json.load(f)
    return(g)



# based on the exact requirements of the specification
def save_entire_couriers_list_simple(main_couriers_list):
    # need if empty or None validation
    f = open("x_main_couriers_list.txt", "w")
    for line in main_couriers_list:
        f.write(line + "\n")
    f.close


def load_default_couriers_list_to_global():
    list_copier = []
    
    f = open("x_main_couriers_list.txt", "r")
    for lines in f:
        #print(lines)
        list_copier.append(lines.strip())
    f.close()

    main_couriers_list = list_copier

    fm.format_display()
    return(main_couriers_list)


    
def save_orders_list(main_orders_list):
    with open("x_main_orders_list.json", "w+") as f:
        if len(f.read()) == 0:
            f.write(json.dumps(main_orders_list, indent = 4))
        else:
            f.write(',\n' + json.dumps(main_orders_list, indent = 4))





def load_orders_list():
    pass





# DRIVER
load_all()