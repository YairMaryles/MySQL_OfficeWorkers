from sqlalchemy import create_engine
import pandas as pd
import openpyxl
from SQL_Commands import *
from entry_info import *


# CONNECTS TO LOCAL DATABASE
def connect():
    entry_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    cnx = create_engine(entry_string)
    mc = cnx.connect()
    return mc


# DISCONNECTS FROM LOCAL DATABASE
def disconnect(mc):
    mc.close()


# OUTPUTS A GIVEN TABLE
def create_full_table(name, mc):
    df1 = pd.read_sql_query(f"SELECT * FROM {name}", mc)
    df = pd.DataFrame(df1)
    df.to_excel(f"{name}_full.xlsx", index=False)


# RUNS A SPECIFIC STATEMENT GIVEN AND RETURNS A DATABASE
def run_statement(mc, statement: str) -> pd.DataFrame:
    df = pd.read_sql_query(statement, mc)
    return pd.DataFrame(df)


# RUNS AND SAVES STATEMENTS GIVEN INTO A GIVEN FILE
def output_statements(mc, output_file_name: str, statements: []):
    DFS = [run_statement(mc=mc, statement=st)  for st in statements]

    with pd.ExcelWriter(output_file_name, engine='openpyxl') as writer:
        for i, df in enumerate(DFS):
            df.to_excel(writer, sheet_name=f'Sheet{i}', index=False)

    print(f"Statements outputted to file: {output_file_name}")


if __name__ == '__main__':
    mc = connect()
    output_statements(mc=mc, output_file_name='output_file.xlsx', statements=select_commands)
    disconnect(mc)

