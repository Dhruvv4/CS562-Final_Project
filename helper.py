# This is a helper file which includes all helper functions for the project.
from collections import defaultdict
from math import inf
import re

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
    
    with open(file_path, 'r') as f:
        contents = f.read().split('\n')

    for idx, line in enumerate(contents):
        if line == 'SELECT ATTRIBUTE(S):':
            MF_Struct['select'] = contents[idx+1]
        if line == 'NUMBER OF GROUPING VARIABLES(n):':
            MF_Struct['groupingVariables'] = int(contents[idx+1])
        if line == 'GROUPING ATTRIBUTES(V):':
            MF_Struct['groupingAttributes'] = contents[idx+1]
        if line == 'F-VECT([F]):':
            MF_Struct['listOfAggregateFuncs'] = [agg.strip().lower() for agg in contents[idx+1].split(',')]
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
            MF_Struct['havingClause'] = contents[idx+1]
            having_idx = int(idx)
            # if MF_Struct['havingClause'] == '-':
            #     del MF_Struct['havingClause']
    return MF_Struct

def print_MFStruct(MF_struct):
    for key, value in MF_struct.items():
        print(key)
        print(value, end='\n')
    print()

def get_aggregate_for(data, gv, type):
    groupBy = {}
    for idx, (cust, prod, day, month, year, state, quantC, date) in enumerate(data, 1):
            if gv in groupBy:
                if type == 'sum':
                    groupBy[gv][type] += quantC
            else:
                groupBy[gv] = {type: 0}

def get_agg_funcs(agg_funcs: list[str]):
    gv = {}
    for func in agg_funcs:
        if func[0] in gv:
            idx, agg, col = func.split('_')
            gv[func[0]].append((agg, col))
        else:
            idx, agg, col = func.split('_')
            gv[func[0]] = [(agg, col)]
    return gv

def get_group_from_such_that(such_that: str):
    groups, where = [], []
    if 'and' in such_that:
        result = such_that.split(' and ')
        print(result)
        for group in result:
            if '=' in group:
                res = group.split(' = ')
                if len(res) == 2 and res[0][2:] == res[1]:
                    groups.append(res[1])
                else:
                    where.append(group[2:].replace('=', '=='))
    else:
        if '=' in such_that:
            res = such_that.split(' = ')
            if len(res) == 2 and res[0][2:] == res[1]:
                groups.append(res[1])
            else:
                print(group)
                where.append(group[2:].replace('=', '=='))
    where = [w.replace('quant', 'quantC') if 'quant' in w else w for w in where]
    return ", ".join(groups), " and ".join(where)

def get_algorithm(file_path):
    MF_Struct = get_MF_Struct(file_path)
    n = MF_Struct['groupingVariables']
    agg_funcs = get_agg_funcs(MF_Struct['listOfAggregateFuncs'])
    setup_gv = """for i in range(MF_Struct['groupingVariables']):
    """
    for i in range(len(MF_Struct['selectConditionVector'])):
        such_that = MF_Struct['selectConditionVector'][i]
        if i == 0:
            groups, where = get_group_from_such_that(such_that)
            agg_func = agg_funcs[f"{i + 1}"]
            setup_gv += f"""
            if i == 0:
                if ({groups}) in sales_gb_group"""
            setup_gv += f" and {where}:" if len(where) > 0 else ":"
                
            for (agg, col) in agg_func:
                if agg in ['avg', 'sum']:
                    setup_gv += f"""
                    sales_gb_group[({groups})]['{i+1}_{agg}'] += quantC"""
                elif (agg == 'max'):
                    setup_gv += f"""
                    sales_gb_group[({groups})]['{i+1}_{agg}'] = max(sales_gb_group[({groups})]['{i+1}_{agg}'], quantC)"""
                elif (agg == 'min'):
                    setup_gv += f"""
                    sales_gb_group[({groups})]['{i+1}_{agg}'] = min(sales_gb_group[({groups})]['{i+1}_{agg}'], quantC)"""
                elif (agg == 'count'):
                    setup_gv += f"""
                        sales_gb_group[({groups})]['{i+1}_{agg}'] += 1"""
                    
            setup_gv += f"""
                else:
                    sales_gb_group[({groups})] = {{}}"""
            for agg, col in agg_func:
                # agg = listOfAggFns[i].split('_')[1].lower()
                if agg in ['avg', 'sum']:
                    setup_gv += f"""
                    sales_gb_group[({groups})]['{i+1}_{agg}'] = quantC"""
                elif (agg == 'max'):
                    setup_gv += f"""
                    sales_gb_group[({groups})]['{i+1}_{agg}'] = quantC"""
                elif (agg == 'min'):
                    setup_gv += f"""
                    sales_gb_group[({groups})]['{i+1}_{agg}'] = quantC"""
                elif (agg == 'count'):
                    setup_gv += f"""
                sales_gb_group[({groups})]['{i+1}_{agg}'] += 1
                """
        elif i != 0:
            groups, where = get_group_from_such_that(such_that)
            agg_func = agg_funcs[f"{i + 1}"]
            setup_gv += f"""
            if i == {i}:
                if ({groups}) in sales_gb_group"""
            setup_gv += f" and {where}:" if len(where) > 0 else ":"
            for (agg, col) in agg_func:
                if agg in ['avg', 'sum']:
                    setup_gv += f"""
                    sales_gb_group[({groups})]['{i+1}_{agg}'] += quantC"""
                elif (agg == 'max'):
                    setup_gv += f"""
                    sales_gb_group[({groups})]['{i+1}_{agg}'] = max(sales_gb_group[({groups})]['{i+1}_{agg}'], quantC)"""
                elif (agg == 'min'):
                    setup_gv += f"""
                    sales_gb_group[({groups})]['{i+1}_{agg}'] = min(sales_gb_group[({groups})]['{i+1}_{agg}'], quantC)"""
                elif (agg == 'count'):
                    setup_gv += f"""
                        sales_gb_group[({groups})]['{i+1}_{agg}'] += 1"""
                    
            setup_gv += f"""
                else:
                    sales_gb_group[({groups})] = {{}}"""
            for agg, col in agg_func:
                if agg in ['avg', 'sum']:
                    setup_gv += f"""
                    sales_gb_group[({groups})]['{i+1}_{agg}'] = quantC"""
                elif (agg == 'max'):
                    setup_gv += f"""
                    sales_gb_group[({groups})]['{i+1}_{agg}'] = quantC"""
                elif (agg == 'min'):
                    setup_gv += f"""
                    sales_gb_group[({groups})]['{i+1}_{agg}'] = quantC"""
                elif (agg == 'count'):
                    setup_gv += f"""
                    sales_gb_group[({groups})]['{i+1}_{agg}'] += 1
                    """
    
    agg = MF_Struct['listOfAggregateFuncs']
    such_that = MF_Struct['selectConditionVector']
    mapper = {}
    agg_row = ""
    for idx, a in enumerate(agg):
        group, _ = get_group_from_such_that(such_that[int(a[0]) - 1])
        mapper[a] =  group
        g = len(group.split(','))
        mapper[a] = ",".join([f'key[{i}]' for i in range(g)])        

    for idx, a in enumerate(agg):
        agg_func = "_".join(a.split('_')[:-1])
        agg_row += f"sales_gb_group[({mapper[a]})]['{agg_func}'],"

    having_str = ""
    if MF_Struct['havingClause'] != '-':
        having_str += "if "
        having_str += f"""{fetch_having(MF_Struct['havingClause'], mapper)}:
        """
    
    setup_gv += f"""
    
    for key, values in sales_gb_group.items():
        if len(key) == {n}:
            {having_str if len(having_str) > 0 else ""}
                output.add_row([*key] + [{agg_row}])
        
    print(output)
    """
    return setup_gv
    

def fetch_having(having_str, mapper):
    having_str = having_str.lower()
    condition = None
    result = ""
    if '=' in having_str:
        condition = having_str.split(' = ')
        left = "_".join(condition[0].split('_')[:-1])
        right = "_".join(condition[1].split('_')[:-1])
        result = f"sales_gb_group[({mapper[condition[0]]})]['{left}'] = sales_gb_group[({mapper[condition[1]]})]['{right}']"
    elif '<' in having_str:
        condition = having_str.split(' < ')
        left = "_".join(condition[0].split('_')[:-1])
        right = "_".join(condition[1].split('_')[:-1])
        result = f"sales_gb_group[({mapper[condition[0]]})]['{left}'] < sales_gb_group[({mapper[condition[1]]})]['{right}']"
    elif '>' in having_str:
        condition = having_str.split(' > ')
        left = "_".join(condition[0].split('_')[:-1])
        right = "_".join(condition[1].split('_')[:-1])
        result = f"sales_gb_group[({mapper[condition[0]]})]['{left}'] > sales_gb_group[({mapper[condition[1]]})]['{right}']"
    elif '!=' in having_str:
        condition = having_str.split(' != ')
        left = "_".join(condition[0].split('_')[:-1])
        right = "_".join(condition[1].split('_')[:-1])
        result = f"sales_gb_group[9{mapper[condition[0]]})]['{left}'] != sales_gb_group[({mapper[condition[1]]})]['{right}']"
    elif '<>' in having_str:
        condition = having_str.split(' <> ')
        left = "_".join(condition[0].split('_')[:-1])
        right = "_".join(condition[1].split('_')[:-1])
        result = f"sales_gb_group[({mapper[condition[0]]})]['{left}'] != sales_gb_group[{mapper[condition[1]]}]['{right}']"
    
    return result