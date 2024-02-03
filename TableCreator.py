import mysql.connector
from data_generator import *
from SQL_Commands import *
from entry_info import *
import pandas as pd
import pyarrow
import pymysql
from sqlalchemy import create_engine

mydb = mysql.connector.connect(
    host=host,
    user= user,
    password= password,
    port=port,
    database=database
)

####################### CODE
mycurser = mydb.cursor()
# CREATE AND FILL EMPLOYEE TABLE
mycurser.execute(create_employees_table)
mydb.commit()
mycurser.executemany(act_insert_workers, create_employees(500))
mydb.commit()
# CREATE AND FILL BRANCH TABLE
mycurser.execute(create_branches_table)
mydb.commit()
mycurser.executemany(act_insert_branches, branch_info)
mydb.commit()
print("Done creating tables")
# data = mycurser.fetchall()
# df = pd.read_sql_query(sql, mydb)
# df1 = pd.DataFrame(df)
# print(df)

mydb.close()

####################### FUNCS
def generate_data():
    mycurser.executemany(act_insert_workers, create_employees(1))

