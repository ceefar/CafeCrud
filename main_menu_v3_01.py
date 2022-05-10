from numpy import disp
import products_v1_02 as prdct
import couriers_v3_01 as cour
import format_random_v2_00 as fm # for formatting display, getting random things


def main_menu():
    disp_size = 20
    rows = 3
    user_menu_input = 1
    while user_menu_input != "0":
        # PRINT THE MENU & GET THE USERS INPUT
        print_main_menu() 
        user_menu_input = input("Enter Menu Selection : ")
        # GO TO COURIERS
        if user_menu_input == "1":
            cour.main()
        # GO TO ORDERS
        elif user_menu_input == "2":
            rows, disp_size = prdct.main_menu(rows, disp_size)
        elif user_menu_input == "3":
            for x, _ in enumerate(cour.Couriers.couriers_list):
                print(cour.Couriers.couriers_list[x].name)
        elif user_menu_input == "4":
            cour.update_courier(disp_size)
        elif user_menu_input == "5":
            print(f"Rows : {rows}, Display Size : {disp_size}")
        elif user_menu_input == "6":
            #prdct.Product.print_via_class_method()
            prdct.Product.update_name(prdct.Product,15)
        #
        # IMPORTANT - THIS IS WHAT IM TRYING TO WRAP MY HEAD AROUND
        # by using class method you dont need to initialise an instance of product to be able to access the methods within the class, 
        # you have just made your own new method that can be directly accessed by the class (which is stored in the module) and therefore everything within it,
        # if the method in question did not require self as a parameter then it could still be accessed without an instance,
        # hence why load works, it creates instances and creating instances doesn't *require* an instance to exist
        # NAH NOT EVEN 
        # very confusing everytime i think ive wrapped my head around it...
        #
        elif user_menu_input == "0":
            break
        else:
            print("Some Wrong Input Error Message")
    # END WHILE
    print("SAVING...")
    prdct.Product.save_all_products_as_csv(prdct.Product) # DO NOT HAVE MULTIPLE AT END SAVES (im sure cant hurt but still is unnecessary)
    cour.Couriers.save_all_products_as_csv(cour.Couriers)
    # BADLY NEED TRY EXCEPT SO CATCHES ERRORS AND SAVES BEFORE QUITTING A FATAL EXCEPTION!


def print_main_menu():
    fm.print_app_name("MAIN")
    #menu_string = ["[ 1 ] for Couriers", "[ 2 ] for Orders", "[ 3 ] to Print Couriers", "[ 4 ] to Print Orders", "[ 0 ] to Quit","- - - - - - - - - - -"]
    menu_string = ["[ 1 ] for Couriers", "[ 2 ] for Products", "[ 0 ] to Quit","- - - - - - - - - - -"]
    print(*menu_string, sep="\n")


def driver(): #loads files, initialises app (should do save here when bounce now ig!)
    prdct.Product.load_products_via_csv()
    #prdct.Product.load_list_from_file(True)
    #cour.Couriers.load_via_pickle() # both are class methods and therefore i think means would be properly encapuslated (if made private) which is awesome but sure im likely missing something (is a way to fake it in python using underscore notation right?)
    cour.Couriers.load_couriers_via_csv() # yh legit is actually private but just can access because python not c++ ok kl np
    main_menu()
    

driver()