from helper import get_MF_Struct

MF_Struct = get_MF_Struct('./input/input1.txt')
gv = "_".join([v.strip() for v in MF_Struct['groupingAttributes'].split(',')])
print(gv)