# This is a helper file which includes all helper functions for the project.
from collections import defaultdict

def readFile(path: str):
    # Read the file of path provided and return the contents
    with open(path, 'r') as f:
        return f.read()


def readFileByLines(path: str):
    # Read the file by lines of path provided and return the contents
    with open(path, 'r') as f:
        return f.readlines()

def writeFile(path: str, data):
    # Write contents to the file
    with open(path, 'w') as f:
        f.write(data)
    print(f'Data successfully written to {path}')

def groupingVariables(number):
    return ": " + ", ".join([chr(i + 64) for i in range(1, number + 1)])

def getMaxOf(data):
    # Data should be a list to iterate and perform math 'max' operation
    return max(data)

def getMinOf(data):
    # Data should be a list to iterate and perform math 'min' operation
    return min(data)

def getSumOf(data):
    # Data should be a list to iterate and perform math 'sum' operation
    return sum(data)

def getAvgOf(data):
    # Data should be a list to iterate and perform math 'avg' operation
    return getSumOf(data) / len(data)

def isString(string):
    # Validation function to check if the passed argument is a string
    return type(string) == str and len(string.strip()) > 0

def isStringArray(stringArray):
    # Validation function to check if the passed argument is a string array
    return type(stringArray) == list and len(stringArray) > 0

def isNumber(number):
    # Validation function to check if the passed argument is a number/integer
    return type(number) == int

def get_MF_Struct(file_path):
    MF_Struct = dict()
    
    # Read the file 
    with open(file_path, 'r') as f:
        contents = f.read().split('\n')

    #----Outline Algorithm for reading attributes
    for idx, line in enumerate(contents):
        if line == 'SELECT ATTRIBUTE(S):':
            MF_Struct['select'] = contents[idx+1]
        if line == 'NUMBER OF GROUPING VARIABLES(n):':
            MF_Struct['groupingVariables'] = int(contents[idx+1])
        if line == 'GROUPING ATTRIBUTES(V):':
            MF_Struct['groupingAttributes'] = contents[idx+1]
        if line == 'F-VECT([F]):':
            MF_Struct['listOfAggregateFuncs'] = [agg.strip() for agg in contents[idx+1].split(',')]
        if line == 'SELECT CONDITION-VECT([C]):':
            conditions = []
            idx_t = idx + 1
            while True:
                if (contents[idx_t] == 'HAVING CLAUSE (G):'):
                    break
                conditions.append(contents[idx_t])
                idx_t += 1
                
            MF_Struct['selectConditionVector'] = conditions
        if line == 'HAVING CLAUSE (G):':
            # print('in having caluse')
            MF_Struct['havingClause'] = contents[idx+1]
            having_idx = int(idx)
            # if MF_Struct['havingClause'] == '-':
            #     del MF_Struct['havingClause']
    return MF_Struct

def get_aggregate_for(data, gv, type):
    groupBy = {}
    for idx, (cust, prod, day, month, year, state, quantC, date) in enumerate(data, 1):
            if gv in groupBy:
                if type == 'sum':
                    groupBy[gv][type] += quantC
            else:
                groupBy[gv] = {type: 0}

def get_where_conditions(gv_str, no_gv, conditions, listOfAggFns):
    such_that_str = ""
    for i in range(no_gv):
        if i == 0:
            such_that_str += f"""if {conditions[i][2:]}:
    sales_gb_group[({gv_str})]['{listOfAggFns[i].split('_')[1].lower()}'] += quantC"""
        else:
            such_that_str += f"""\n\telif {conditions[i][2:]}:
    sales_gb_group[({gv_str})]['{listOfAggFns[i].split('_')[1].lower()}'] += quantC"""
    return such_that_str