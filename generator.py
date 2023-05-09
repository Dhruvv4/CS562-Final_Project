import subprocess
from helper import readFileByLines, groupingVariables

def main():
    """
    This is the generator code. It should take in the MF structure and generate the code
    needed to run the query. That generated code should be saved to a 
    file (e.g. _generated.py) and then run.
    """
    input_path = './input/input1.txt'
    # Reading the input file
    with open(input_path, 'r') as f:
        contents = f.read().split('\n')

    db_queries = {}

    for idx, line in enumerate(contents):
        if line == 'SELECT ATTRIBUTE(S):':
            db_queries['select'] = contents[idx+1]
        if line == 'NUMBER OF GROUPING VARIABLES(n):':
            db_queries['groupingVariables'] = int(contents[idx+1])
        if line == 'GROUPING ATTRIBUTES(V):':
            db_queries['groupingAttributes'] = contents[idx+1]
        if line == 'F-VECT([F]):':
            db_queries['listOfAggregateFuncs'] = contents[idx+1]
        if line == 'SELECT CONDITION-VECT([C]):':
            conditions = []
            idx_t = idx + 1
            while True:
                if (contents[idx_t] == 'HAVING CLAUSE (G):'):
                    break
                conditions.append(contents[idx_t])
                idx_t += 1
            print(conditions)
                
            db_queries['selectConditionVector'] = conditions
        if line == 'HAVING CLAUSE (G):':
            # print('in having caluse')
            db_queries['havingClause'] = contents[idx+1]
            having_idx = int(idx)
            # if db_queries['havingClause'] == '-':
            #     del db_queries['havingClause']

    print(db_queries)
    print(groupingVariables(2))

    query = f"""
    SELECT {db_queries['select']}
    from sales
    """

    # This is for group by clause, checking whether we have any grouping variables present or no.
    if db_queries['groupingVariables'] > 0:
        query += f"""group by {db_queries['groupingAttributes']}{groupingVariables(db_queries['groupingVariables'])}\n"""
    else:
        query += f"""group by {db_queries['groupingAttributes']}\n"""

    # This is for having clause (G)
    if db_queries['havingClause'] != '-':
        query += f"    having {db_queries['havingClause']};\n"
    
    print(query)

    body = """

    #---Variable declaration
    sales_gb_group = defaultdict()
    db_queries = {}
    #---end variable Declaration


    def get_all_records(cur):
        get_all_records_query = '''SELECT * from sales;'''
        # Execute a command: this creates a new table
        cur.execute(get_all_records_query)
        all_sales = cur.fetchall()
        return all_sales

    # Fetching all records from sales table
    all_records = get_all_records(cur)

    #----Reading Input File
    input_path = './input/input1.txt'
    # Reading the input file
    with open(input_path, 'r') as f:
        contents = f.read().split('\\n')

    #----Outline Algorithm for reading attributes
    for idx, line in enumerate(contents):
        if line == 'SELECT ATTRIBUTE(S):':
            db_queries['select'] = contents[idx+1]
        if line == 'NUMBER OF GROUPING VARIABLES(n):':
            db_queries['groupingVariables'] = int(contents[idx+1])
        if line == 'GROUPING ATTRIBUTES(V):':
            db_queries['groupingAttributes'] = contents[idx+1]
        if line == 'F-VECT([F]):':
            db_queries['listOfAggregateFuncs'] = contents[idx+1]
        if line == 'SELECT CONDITION-VECT([C]):':
            conditions = []
            idx_t = idx + 1
            while True:
                if (contents[idx_t] == 'HAVING CLAUSE (G):'):
                    break
                conditions.append(contents[idx_t])
                idx_t += 1
            print(conditions)
                
            db_queries['selectConditionVector'] = conditions
        if line == 'HAVING CLAUSE (G):':
            # print('in having caluse')
            db_queries['havingClause'] = contents[idx+1]
            having_idx = int(idx)
            # if db_queries['havingClause'] == '-':
            #     del db_queries['havingClause']

    print(db_queries)

    groupList = [col.strip() for col in db_queries['groupingAttributes'].split(",")]
    groupTuple = tuple(groupList)


    for idx, (cust, prod, day, month, year, state, quantC, date) in enumerate(all_records, 1):
        if  (cust, prod) not in sales_gb_group:
            sales_gb_group[(cust, prod)] = { 'sumq': 0}
        else:
            sales_gb_group[(cust, prod)]['sumq'] += quantC
    print(sales_gb_group)
    
    for raw in sales_gb_group.items():
        _global.append( for col in raw])
    """

    # Note: The f allows formatting with variables.
    #       Also, note the indentation is preserved.
    tmp = f"""
import os
from psycopg2 import Error, connect
import psycopg2.extras
import tabulate
from dotenv import load_dotenv
#from queryDatabase import get_all_records
load_dotenv()
from collections import defaultdict

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
    
    _global = []
    {body}
    return tabulate.tabulate(_global,
                        headers="keys", tablefmt="psql")

def main():
    print(query())
    
if "__main__" == __name__:
    main()
    """

    # Write the generated code to a file
    open("_generated.py", "w").write(tmp)
    # Execute the generated code
    subprocess.run(["python", "_generated.py"])


if "__main__" == __name__:
    main()
