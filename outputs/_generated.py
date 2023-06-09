
import os
from psycopg2 import Error, connect
import psycopg2.extras
import tabulate
from dotenv import load_dotenv
from database.queryDatabase import get_all_records
load_dotenv()
from collections import defaultdict
from prettytable import PrettyTable
from helper import get_MF_Struct
from math import inf

# DO NOT EDIT THIS FILE, IT IS GENERATED BY generator.py

def query():
    load_dotenv()

    database = os.getenv('DB_DATABASE')
    host = os.getenv('DB_HOST')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    input_path = os.getenv('DB_INPUT_PATH')

    conn = connect(host=host,database=database,user=user,password=password)
    cur = conn.cursor()
    cur.execute("SELECT * FROM sales")

    input_path = './input/input2a.txt'
    MF_Struct = get_MF_Struct(input_path)

    cols_name = [x.strip().lower() for x in MF_Struct['select'].split(',')]
    output = PrettyTable(cols_name)
    #---Variable declaration
    sales_gb_group = defaultdict()
    #---end variable Declaration

    # Fetching all records from sales table
    all_records = get_all_records(cur)
    
    # output.field_names = all_records.split(',')

    groupTuple = "_".join([v.strip() for v in MF_Struct['groupingAttributes'].split(',')])

    # Only select those columns which are in the select attributes of the MF Structure
    for idx, (cust, prod, day, month, year, state, quantC, date) in enumerate(all_records, 1):

        # Aggregation block
        # Here we have to take into account for the aggregate variables and it's corresponding
        # column.

        for i in range(MF_Struct['groupingVariables']):
            if i == 0:
                # Iterate over a list of gv by index and check for gv in sales_gb
                # get a proper gv along with it's agg func
                if (prod, month) in sales_gb_group:
                    # Here check for any different condition
                    # Such as non gv parameter, eg comparison with state = 'NY'
                    sales_gb_group[(prod, month)]['1_sum'] += quantC
                else:
                    sales_gb_group[(prod, month)] = {}
                    sales_gb_group[(prod, month)]['1_sum'] = quantC
            elif i == 1:
                if (prod) in sales_gb_group:
                    sales_gb_group[(prod)]['2_sum'] += quantC
                else:
                    sales_gb_group[(prod)] = {}
                    sales_gb_group[(prod)]['2_sum'] = quantC
    
    # Here check for the select state and prepare row to append
    for key, value in sales_gb_group.items():
        # This is our having clause as well as custom select variables
        if (len(key) == MF_Struct['groupingVariables']):
            output.add_row([key[0], key[1], (value['1_sum'] / sales_gb_group[key[0]]['2_sum']) * 100])
        # output.add_row([col for col in row])

    print(output)
    return output

def main():
    query()
    
if "__main__" == __name__:
    main()
    