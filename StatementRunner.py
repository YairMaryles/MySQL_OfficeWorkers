from sqlalchemy import create_engine
import pandas as pd
import openpyxl
from SQL_Commands import *
from entry_info import *


def run_sql():
    entry_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    cnx = create_engine(entry_string)
    mc = cnx.connect()
    return mc

def close_sql(mc):
    mc.close()

def create_full_table(name, mc):
    df1 = pd.read_sql_query(f"SELECT * FROM {name}", mc)
    df = pd.DataFrame(df1)
    df.to_excel(f"{name}_full.xlsx", index=False)


def run_statement(mc, statement: str) -> pd.DataFrame:
    df = pd.read_sql_query(statement, mc)
    return pd.DataFrame(df)


def output_statements(mc, output_file_name: str, statements: []):
    DFS = [run_statement(mc=mc, statement=st)  for st in statements]

    with pd.ExcelWriter(output_file_name, engine='openpyxl') as writer:
        for i, df in enumerate(DFS):
            df.to_excel(writer, sheet_name=f'Sheet{i}', index=False)

    print(f"Statements outputted to file: {output_file_name}")


if __name__ == '__main__':
    mc = run_sql()

    output_statements(mc=mc, output_file_name='output_file.xlsx', statements=select_commands)

    close_sql(mc)

