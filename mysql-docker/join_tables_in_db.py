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

# o.person_id, o.order_price \
# RIGHT JOIN orders o
# ON p.person_id = o.person_id

sql = "SELECT \
  person.first_name AS name, \
  person.last_name AS last, \
  orders.person_id AS id, \
  orders.order_price AS price \
  FROM person \
  INNER JOIN orders ON person.person_id = orders.person_id \
  ORDER BY person.person_id "

cursor.execute(sql) 

myresult = cursor.fetchall()

for x in myresult:
    print(x)

#connection.commit()
#cursor.close()
#connection.close()