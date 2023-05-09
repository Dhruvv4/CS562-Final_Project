# Basic imports
from psycopg2 import Error, connect
import os
from dotenv import load_dotenv
from queryDatabase import get_all_records
load_dotenv()
from collections import defaultdict
from prettytable import PrettyTable


class DatabaseConfig:
    database = os.getenv('DB_DATABASE')
    host = os.getenv('DB_HOST')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    input_path = os.getenv('DB_INPUT_PATH')

db_cfg = DatabaseConfig()

#---Variable declaration
sales_gb_group = defaultdict()
MF_Struct = {}
#---end variable Declaration


# Connection instance


# try:

connection = connect(host=db_cfg.host, 
                            database=db_cfg.database,
                            user=db_cfg.user,
                            password=db_cfg.password)

# Create a cursor to perform database operations
cursor = connection.cursor()
# Print PostgreSQL details
# print("PostgreSQL server information")
# print(connection.get_dsn_parameters(), "\n")

# Fetching all records from sales table
all_records = get_all_records(cursor)
# cust, prod, day, month, year, state, quantC, date = all_records[0]
# print(cust, prod, day, month, year, state, quantC, date) 

# Reading the input file
with open('./input/input1.txt', 'r') as f:
    contents = f.read().split('\n')

db_queries = {}

for idx, line in enumerate(contents):
    if line == 'SELECT ATTRIBUTE(S):':
        db_queries['select'] = contents[idx+1]
    if line == 'NUMBER OF GROUPING VARIABLES(n):':
        db_queries['groupingVariables'] = contents[idx+1]
    if line == 'GROUPING ATTRIBUTES(V):':
        db_queries['groupingAttributes'] = contents[idx+1]
    if line == 'F-VECT([F]):':
        db_queries['listOfAggregateFuncs'] = contents[idx+1]

# print(db_queries)

# Get all sales tables count and average
sales_gb_cust = defaultdict()

for idx, (cust, prod, day, month, year, state, quantC, date) in enumerate(all_records, 1):
    if cust not in sales_gb_cust:
        sales_gb_cust[cust] = {'maxq': 0, 'minq': 999999, 'sumq': 0, 'countq': 1}
    else:
        if quantC >= sales_gb_cust[cust]['maxq']:
            sales_gb_cust[cust]['maxq'] = quantC
        if quantC <= sales_gb_cust[cust]['minq']:
            sales_gb_cust[cust]['minq'] = quantC
        sales_gb_cust[cust]['sumq'] += quantC
        sales_gb_cust[cust]['countq'] += 1
        sales_gb_cust[cust]['avgq'] = sales_gb_cust[cust]['sumq'] / sales_gb_cust[cust]['countq']

output = PrettyTable()
print(db_queries['select'].split(','))
output.field_names = db_queries['select'].split(',')

for customer, data in sales_gb_cust.items():
    row = [customer, data['avgq'], data['maxq']]
    output.add_row(row)

# print(output)

    # Only select those columns which are in the select attributes of the MF Structure
for idx, (cust, prod, day, month, year, state, quantC, date) in enumerate(all_records, 1):

    if (cust, prod) not in sales_gb_group:
        sales_gb_group[(cust, prod)] = { 'sumq': 0}
    else:
        sales_gb_group[(cust, prod)]['sumq'] += quantC
print(sales_gb_group)
    
# except (Exception, Error) as error:
#     print(error)
#     print("Error while connecting to PostgreSQL", error)
# finally:
#     if (connection):
#         cursor.close()
#         connection.close()
#         print("PostgreSQL connection is closed")