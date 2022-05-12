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
    host,
    user,
    password,
    database
)

# A cursor is an object that represents a DB cursor, which is used to manage the context of a fetch operation.
cursor = connection.cursor()

sql = "INSERT INTO person (first_name, last_name, height) VALUES (%s, %s, %s)"
val = ("Cave","Johnson", 1.95)
cursor.execute(sql, val)

connection.commit()
cursor.close()
connection.close()