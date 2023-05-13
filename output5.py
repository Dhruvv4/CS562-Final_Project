
import os
from psycopg2 import connect
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

    input_path = f'./input/input5.txt'
    MF_Struct = get_MF_Struct(input_path)

    cols_name = [x.strip().lower() for x in MF_Struct['select'].split(',')]
    output = PrettyTable(cols_name)
    
    sales_gb_group = defaultdict()

    # Fetching all records from sales table
    all_records = get_all_records(cur)

    groupTuple = "_".join([v.strip() for v in MF_Struct['groupingAttributes'].split(',')])

    for idx, (cust, prod, day, month, year, state, quantC, date) in enumerate(all_records, 1):
        for i in range(MF_Struct['groupingVariables']):
    
            if i == 0:
                if (prod, month) in sales_gb_group and state == "NJ":
                    sales_gb_group[(prod, month)]['1_sum'] += quantC
                else:
                    sales_gb_group[(prod, month)] = {}
                    sales_gb_group[(prod, month)]['1_sum'] = quantC
            if i == 1:
                if (prod) in sales_gb_group and state == "NJ":
                    sales_gb_group[(prod)]['2_sum'] += quantC
                else:
                    sales_gb_group[(prod)] = {}
                    sales_gb_group[(prod)]['2_sum'] = quantC
    
    for key, values in sales_gb_group.items():
        if len(key) == 2:
            if sales_gb_group[(key[0],key[1])]['1_sum'] < sales_gb_group[(key[0])]['2_sum']:
        
                output.add_row([*key] + [sales_gb_group[(key[0],key[1])]['1_sum'],sales_gb_group[(key[0])]['2_sum'],])
        
    print(output)
    

    
    return output


def main():
    query()
    
if "__main__" == __name__:
    main()
    