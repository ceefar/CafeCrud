from numpy import number
import format_random_v2_00 as fm

## END IMPORTS

# CLASSES ##################################################################################################################################################################
# COURIERS CLASS #################################


class Orders:
    """ Orders class stores each order object in a 'global' list, customer name, address, phone + courier id + product ids + order status and (new) tot price """
    orders_list = [] # list to store all instances of each courier
    orders_id_cache = [] # for ensuring the same orders id is NEVER used again, this is of critical importance imo

    # init constructor
    def __init__(self, customer_name:str, customer_address:str, customer_phone:str, order_status:int, order_price:float, courier_id:int = None, products_ids:list = []): 
        """ Load or create new courier with name, phone numb, & id numb """





# customer name, address, phone
# courier number (index or id idc)
# product - items (product ids)
# order - status, price



## MAIN PROGRAM ############################################################################################################################################################

def main():
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
            # QUICK MENU / CREATE AGAIN
            print("Quick Create Another Order?\n")
            if fm.get_user_yes_true_or_no_false():
                print_again = False
                user_menu_input = "1"
            else:
                print_again = True


if __name__ == "__main__":
    main()