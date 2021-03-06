import products_v1_02 as prdct
import couriers_v3_01 as cour
import format_random_v2_00 as fm # for formatting display, getting random things
import orders_v3_01 as ordrs


import pymysql
import os
from dotenv import load_dotenv

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


def write_to_db():
    # A cursor is an object that represents a DB cursor,
    # which is used to manage the context of a fetch operation.
    cursor = connection.cursor()

    for index, _ in enumerate(cour.Couriers.couriers_list):
        print(index)
        name_1 = (cour.Couriers.couriers_list[index].name)
        num_1 = (cour.Couriers.couriers_list[index].phone_number)
        loc_1 = (cour.Couriers.couriers_list[index].location)
        uuid_1 = (cour.Couriers.couriers_list[index].courier_id)

        # Execute SQL query
        sql = "INSERT INTO couriers (name, phone_number, location, courier_uuid) VALUES (%s, %s, %s, %s)"
        val = (name_1, num_1, loc_1, uuid_1)

        cursor.execute(sql, val)
        connection.commit()

    # Closes the cursor so will be unusable from this point 
    cursor.close()

    # Closes the connection to the DB, make sure you ALWAYS do this
    connection.close()


def read_from_db():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM couriers") 
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)
    
    # NEED THIS HERE?
    # Closes the connection to the DB, make sure you ALWAYS do this
    #cursor.close()
    connection.close()



##########################################################################

def main_menu(disp_size = 22, rows = 3):
    user_menu_input = 1
    while user_menu_input != "0":
        # PRINT THE MENU & GET THE USERS INPUT
        print_main_menu() 
        user_menu_input = input("Enter Menu Selection : ")
        # GO TO COURIERS
        if user_menu_input == "1":
            rows, disp_size = cour.main(rows, disp_size)
        # GO TO PRODCTS
        elif user_menu_input == "2":
            rows, disp_size = prdct.main_menu(rows, disp_size)
        # GO TO ORDERS
        elif user_menu_input == "3":
            rows, disp_size = ordrs.main_orders(rows, disp_size) 
        # HIDDEN (print display info)
        elif user_menu_input == "5":
            print(f"Rows : {rows}, Display Size : {disp_size}")
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
    menu_string = ["[ 1 ] for Couriers", "[ 2 ] for Products", "[ 3 ] for Orders", "[ 0 ] to Quit","- - - - - - - - - - -"]
    print(*menu_string, sep="\n")


def driver(): #loads files, initialises app (should do save here when bounce now ig!)
    prdct.Product.load_products_via_csv()
    #prdct.Product.load_list_from_file(True)
    #cour.Couriers.load_via_pickle() # both are class methods and therefore i think means would be properly encapuslated (if made private) which is awesome but sure im likely missing something (is a way to fake it in python using underscore notation right?)
    cour.Couriers.load_couriers_via_csv() # yh legit is actually private but just can access because python not c++ ok kl np

    #write_to_db() # would be something like read if you cant read (theres no data) then write it from backup csv idk
    #read_from_db()
    main_menu()
    
    
driver()