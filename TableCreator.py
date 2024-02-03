import mysql.connector
from data_generator import *
from SQL_Commands import *
from entry_info import *
import pandas as pd
import pyarrow
import pymysql
from sqlalchemy import create_engine


# CONNECTS TO LOCAL DATABASE
def connect():
    mydb = mysql.connector.connect( host=host,
                                    user=user,
                                    password=password,
                                    port=port,
                                    database=database)
    return mydb.cursor(), mydb


# DISCONNECTS FROM LOCAL DATABASE
def disconnect(mydb):
    mydb.close()


# CREATES AND FILLS TABLES
def create_tables(mycurser, mydb):

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



if __name__ == '__main__':
    mycurser, mydb = connect()
    create_tables(mycurser=mycurser, mydb=mydb)
    disconnect(mydb=mydb)
    print("Done creating tables")
