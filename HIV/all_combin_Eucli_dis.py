"""
Created on Mar 6 2020

@author: Changze Han
"""
import csv
import numpy as np
import random
import copy
import math

'''
    For HIV project: (maybe other projects)
    
    Calculate euclidean distance for all combination. 
    
    Algorithm: 
        1. Categorize data based on fixed column
        2. Find all combinations based on varied column
        3. calculate multi-vector euclidean distance for each combination 
        
    Example: 
    Take two Longitudinal patients data : 
        | Patient | Days | 137 | 289 | 295 | 
        |   aaa   |   0  |  1  |  0  |  1  | 
        |   aaa   |  10  |  1  |  0  |  1  | 
        |   aaa   |  160 |  1  |  0  |  1  | 
        |   bbb   |   0  |  1  |  0  |  1  | 
        |   bbb   |  50  |  1  |  0  |  1  | 
        ......
        Then this program will calculate euclidean distance for : 
            aaa(0) vs aaa(10)
            aaa(0) vs aaa(160)
            aaa(10) vs aaa(160)
            bbb(0) vs bbb(50) 
            
    Input file: 
        1. should have a header row
        2. should do a two level sort on the input file: sort fixed col then varied col 
        
'''

# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/3.6.20_eucli_dis/"
in_csv_name = "(bin)C_10pos_3patients.csv"
out_csv_name = "eucli_dis_C_3patients.csv"

fixed_col = 3  # col that will be used to categorize data e.g. 'Patients'
var_col = 4  # col that will be used to form combinations e.g. 'Days'
vector_start_col = 5  # vectors start from this column
# ========================================================================================================
input_file = working_dir + in_csv_name
out_file = working_dir + out_csv_name
input_file_list = []  # store input file to list
output_file_list = []

each_fix_start_end_dict = {}
# e.g. {'a':[1,5], 'b':[5,9]} means: two fixed category 'a' & 'b', 'a' starts from index 1 row to 5. 'b' from 5 to 9


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


def comp_euclidean(list1, list2):  # compute euclidean distance between two multi-vector lists
    square_sum = 0
    for i in range(len(list1)):
        square_sum = square_sum + ((float(list2[i]) - float(list1[i]))**2)
    return math.sqrt(square_sum)


# categorize based on fixed column
# build a dict"each_fix_start_end_dict" that has patient name as key, and a list of 2 index as index
# value list: e.g.(1,7) means this patient starts from row index 1 to row index 7
def categorize(l):  # l is input list without header row
    global fixed_col
    global each_fix_start_end_dict
    for row_i in range(len(l)):  # go through each row's index
        if l[row_i][fixed_col] not in each_fix_start_end_dict:  # l[row_i][fixed_col] is this row's fixed category
            each_fix_start_end_dict[l[row_i][fixed_col]] = [row_i+1]  # add the start row index
            # row_i+1 because header was removed, so need to add one index back
        else:  # this category already in the dict
            if len(each_fix_start_end_dict[l[row_i][fixed_col]]) == 2:  # there's already a ending index
                each_fix_start_end_dict[l[row_i][fixed_col]][1] = row_i+1  # update the ending index
            else:  # if there's only start index in the value list
                each_fix_start_end_dict[l[row_i][fixed_col]].append(row_i+1)  # add an ending index


# find all combinations based on varied col then calculate euclidean distance
# d is the completed dictionary by categorize(l) function; l is input list with header;
def all_comb_eucli_dis(d, l):
    global output_file_list
    global var_col
    global vector_start_col
    vec_len = len(l[0][vector_start_col:])  # keep a record of how many vector should be in each row. for debugging
    waste_key_count = 0  # count how many key only has starting index in the value list. unable to cal eucli dis
    waste_key_list = []
    for key in d:
        print(f"{key}: ")
        if len(d[key]) == 1:
            waste_key_count += 1
            waste_key_list.append(key)
            print("Unable to calculate distance.")
        else:
            start = d[key][0]  # start index
            end = d[key][1]  # end index
            how_many_var = end + 1 - start
            how_many_comb_sofar = 0  # count how many combinations have calculated
            while start < end:
                list_one = [int(i) for i in l[start][vector_start_col:]]
                if len(list_one) != vec_len:  # double check
                    raise ValueError(f"Vector Amount Wrong: row{start} has {len(list_one)} vectors.")
                for next in list(range(start+1, end+1)):
                    how_many_comb_sofar += 1
                    list_two = [int(j) for j in l[next][vector_start_col:]]
                    if len(list_two) != vec_len:  # double check
                        raise ValueError(f"Vector Amount Wrong: row{next} has {len(list_two)} vectors.")
                    #  construct output file
                    output_file_list.append([key] +   # fixed name
                                            [l[start][var_col]] +  # varied name 1
                                            [l[next][var_col]] +  # varied name 2
                                            [comp_euclidean(list_one, list_two)])  # eucl dist of varied name 1 VS 2
                start += 1
            print(f"how many varied value : {how_many_var}")
            if how_many_comb_sofar != (how_many_var*(how_many_var-1)/2):
                raise ValueError(f"Error in Combination number : {how_many_comb_sofar}")
            else:
                print(f"how many combinations calculated: {how_many_comb_sofar}")

    if waste_key_count != 0:
        print(f"{waste_key_count} categories are unable to calculate euclidean distance since there's only one sample: "
              f"\n {waste_key_list}")


def main():
    global input_file_list
    global output_file_list
    global vector_start_col
    global each_fix_start_end_dict
    read_csv(input_file, input_file_list)  # read input file

    categorize(input_file_list[1:])  # categorize the data. remove header row.

    all_comb_eucli_dis(each_fix_start_end_dict, input_file_list)

    write_csv(output_file_list, out_file)
    print(f"\n{len(input_file_list)-1} rows data from input(exclude header)")
    print(f"{len(input_file_list[0][vector_start_col:])} vectors each row : {input_file_list[0][vector_start_col:]}")
    print(f"each category's start and end index: \n{each_fix_start_end_dict}")  # print to check the dict


main()



