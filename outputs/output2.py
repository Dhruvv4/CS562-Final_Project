
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

    input_path = f'./input/input2.txt'
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
                if (cust) in sales_gb_group and state == 'NY':
                    sales_gb_group[(cust)]['1_avg'] += quantC
                else:
                    sales_gb_group[(cust)] = {}
                    sales_gb_group[(cust)]['1_avg'] = quantC
            if i == 1:
                if (cust) in sales_gb_group and state == 'NJ':
                    sales_gb_group[(cust)]['2_avg'] += quantC
                else:
                    sales_gb_group[(cust)] = {}
                    sales_gb_group[(cust)]['2_avg'] = quantC
            if i == 2:
                if (cust) in sales_gb_group and state == 'CT':
                    sales_gb_group[(cust)]['3_avg'] += quantC
                else:
                    sales_gb_group[(cust)] = {}
                    sales_gb_group[(cust)]['3_avg'] = quantC
    
    for key, values in sales_gb_group.items():
        if len(key) == 3:
            if sales_gb_group[(key[0])]['1_avg'] > sales_gb_group[(key[0])]['2_avg']:
        
                output.add_row([*key] + [sales_gb_group[(key[0])]['1_avg'],sales_gb_group[(key[0])]['2_avg'],sales_gb_group[(key[0])]['3_avg'],])
        
    print(output)
    

    
    return output



def main():
    query()
    
if "__main__" == __name__:
    main()
    