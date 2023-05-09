input_path = './input/input1.txt'
    # Reading the input file
    with open(input_path, 'r') as f:
        contents = f.read().split('\n')

    MF_Struct = {}

    for idx, line in enumerate(contents):
        if line == 'SELECT ATTRIBUTE(S):':
            MF_Struct['select'] = contents[idx+1]
        if line == 'NUMBER OF GROUPING VARIABLES(n):':
            MF_Struct['groupingVariables'] = int(contents[idx+1])
        if line == 'GROUPING ATTRIBUTES(V):':
            MF_Struct['groupingAttributes'] = contents[idx+1]
        if line == 'F-VECT([F]):':
            MF_Struct['listOfAggregateFuncs'] = contents[idx+1]
        if line == 'SELECT CONDITION-VECT([C]):':
            conditions = []
            idx_t = idx + 1
            while True:
                if (contents[idx_t] == 'HAVING CLAUSE (G):'):
                    break
                conditions.append(contents[idx_t])
                idx_t += 1
            print(conditions)
                
            MF_Struct['selectConditionVector'] = conditions
        if line == 'HAVING CLAUSE (G):':
            # print('in having caluse')
            MF_Struct['havingClause'] = contents[idx+1]
            having_idx = int(idx)
            # if MF_Struct['havingClause'] == '-':
            #     del MF_Struct['havingClause']

    print(MF_Struct)
    print(groupingVariables(2))

    query = f"""
    SELECT {MF_Struct['select']}
    from sales
    """

    # This is for group by clause, checking whether we have any grouping variables present or no.
    if MF_Struct['groupingVariables'] > 0:
        query += f"""group by {MF_Struct['groupingAttributes']}{groupingVariables(MF_Struct['groupingVariables'])}\n"""
    else:
        query += f"""group by {MF_Struct['groupingAttributes']}\n"""

    # This is for having clause (G)
    if MF_Struct['havingClause'] != '-':
        query += f"    having {MF_Struct['havingClause']};\n"
    
    print(query)