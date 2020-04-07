"""
Created on Jan 03 2020

@author: Changze Han
"""

import itertools
import csv
import math
'''
    For HIV project - trimer distance step2: 
    
    Calculate the shortest euclidean distance between all positions on a given Trimer structure. 
    Input: a csv file contains all coordinates. 
    Output: a customized table. 
    
    Note: Currently there are 6 chains(A,B,C,D,E,F). 
          If more chains are required, then need to add more dictionaries and modify function separate_dict(d)
'''
# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/3.11.20_trimer_distance/"
in_csv_name = "6mzj_all_coords(atom&hetam).csv"
out_csv_name = "(chain matrix)6mzj_all_coords(atom&hetam).csv"

# Current output table/matrix: (to customize the table, modify the main function)
# cols: ['A', 'B', 'C', 'D', 'E', 'F']
# rows : ['A', 'B', 'C', 'D', 'E', 'F']
# ========================================================================================================
in_csv_file = working_dir + in_csv_name
out_csv_file = working_dir + out_csv_name
in_csv_list = []  # store input csv file
out_csv_list = []  # store output csv file
pos_coord_dict = {}   # {position1:[[coord1],[coord2],[coord3],[coord4]]}
# separate pos_coord_dict in to separated dicts
A_dict = {}  # separate dict for chain A only
B_dict = {}
C_dict = {}
D_dict = {}
E_dict = {}
F_dict = {}
# ---------------------------add more dicts here: ---------------------------


def read_csv(filedir, listname):
    file = open(filedir)
    reader = csv.reader(file)
    for row in reader:
        listname.append(row)


def write_csv(x, y):  # write list x into file y
    with open(y, 'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()


# go through the csv file and put coordinates that from same position into the same key in a dict
def build_pos_coord_dict(x):   # x is the input csv list
    global pos_coord_dict
    for row in x:
        if row[0] not in pos_coord_dict:
            pos_coord_dict[row[0]] = [row[1:]]
        else:
            pos_coord_dict[row[0]].append(row[1:])


def separate_dict(d):  # separate dict d into separate chains
    global A_dict
    global B_dict
    global C_dict
    global D_dict
    global E_dict
    global F_dict

    for key in d:
        if key[0] == 'A':
            A_dict[key] = d[key]
    for key in d:
        if key[0] == 'B':
            B_dict[key] = d[key]
    for key in d:
        if key[0] == 'C':
            C_dict[key] = d[key]
    for key in d:
        if key[0] == 'D':
            D_dict[key] = d[key]
    for key in d:
        if key[0] == 'E':
            E_dict[key] = d[key]
    for key in d:
        if key[0] == 'F':
            F_dict[key] = d[key]
    # ---------------------------add more if statements here: ---------------------------


# calculate euclidean distance between two N-dimensional coordinates
def euclidean(coord1, coord2):
    square_sum = 0
    for i in range(len(coord1)):
        square_sum = square_sum + ((float(coord2[i]) - float(coord1[i])) ** 2)
    return math.sqrt(square_sum)


# calculate the shortest euclidean distance between two positions
# each position contains multiple coordinates. So need to try all combinations.
# pos1 and pos2: list of lists
def shortest_eucli(pos1, pos2):
    all_distance = []  # while trying all combinations, record each distance
    for cd1 in pos1:  # go through each coord in pos1
        for cd2 in pos2:  # go through each coord in pos2
            all_distance.append(euclidean(cd1, cd2))
    return min(all_distance)


def main():
    read_csv(in_csv_file, in_csv_list)  # store input csv file to a list

    build_pos_coord_dict(in_csv_list)  # convert input csv list to a dict
    separate_dict(pos_coord_dict)  # separate dict into multiple chain dict

    # merge dicts for cols and rows
    col_dict = {**A_dict, **B_dict, **C_dict, **D_dict, **E_dict, **F_dict}  # col_dict = {**A_dict, **B_dict}
    row_dict = {**A_dict, **B_dict, **C_dict, **D_dict, **E_dict, **F_dict}

    # construct first row of output file
    out_csv_list.append(list(col_dict.keys()))
    out_csv_list[0].insert(0, '')  # insert one space at the beginning for the first column

    # construct all rows' header which is also the first column
    for key in row_dict:
        out_csv_list.append([key])

    # cal shortest dis bet positions and add them to output file
    # ---------------------------Customize the output table/matrix here:---------------------------
    '''
    # entire matrix: for matrix output n x n (n rows by n cols):
    for row in out_csv_list[1:]:  # ignore header row
        for col in out_csv_list[0][1:]:  # ignore first index because it's empty
            print(f"{row[0]} VS {col}")
            row.append(shortest_eucli(pos_coord_dict[row[0]], pos_coord_dict[col]))
    '''
    # half matrix: for table output n x m (n rows by m cols, m < n, only top part is a small matrix)
    empty_need = 1
    for row in out_csv_list[1:]:  # ignore header row
        row.extend('' for i in range(empty_need))  # add enough space in advance because only need to cal half matrix
        for col in out_csv_list[0][empty_need+1:]:  # 'empty_need+1' start calculation after the empty space
            print(f"{row[0]} VS {col}")
            row.append(shortest_eucli(pos_coord_dict[row[0]], pos_coord_dict[col]))
        empty_need += 1  # move to next row, so need one extra empty space before the actual value
    # ----------------------------------------------------------------------------------------------

    '''
    print(list(A_dict.keys()))
    print(list(B_dict.keys()))
    print(list(C_dict.keys()))
    print(list(D_dict.keys()))
    print(list(E_dict.keys()))
    print(list(F_dict.keys()))
    '''

    print(f"\nChecking: ")
    print(f"{len(in_csv_list)} rows in Input csv file")
    check_dict_count = 0  # count the total number in dict
    for i in pos_coord_dict:
        check_dict_count += len(pos_coord_dict[i])
    print(f"{check_dict_count} values and {len(pos_coord_dict.keys())} keys in pos-coord dictionary.  ")

    check_chain_dict_value_count = 0
    check_chain_dict_key_count = len(A_dict.keys()) + len(B_dict.keys()) + len(C_dict.keys()) + \
                                 len(D_dict.keys()) + len(E_dict.keys()) + len(F_dict.keys())
    for i in A_dict:
        check_chain_dict_value_count += len(A_dict[i])
    for i in B_dict:
        check_chain_dict_value_count += len(B_dict[i])
    for i in C_dict:
        check_chain_dict_value_count += len(C_dict[i])
    for i in D_dict:
        check_chain_dict_value_count += len(D_dict[i])
    for i in E_dict:
        check_chain_dict_value_count += len(E_dict[i])
    for i in F_dict:
        check_chain_dict_value_count += len(F_dict[i])
    print(f"{check_chain_dict_value_count} values and {check_chain_dict_key_count} keys in separated chain dictionaries.")

    write_csv(out_csv_list, out_csv_file)  # write the output cs file


main()



