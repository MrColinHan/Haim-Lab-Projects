#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 16:32:57 2019

@author: Changze Han
"""

'''
    For FLU project: 
    This script equally distribute x groups into 2 parts in order to run the fisher 
    test fairly. 
    How it works: 
        Input: first part of flu_stdev.py's output. 
        procedure: 
            sort by each group's amount of samples(accession numbers)
            even index's row goes into one part (0,2,4,6,8...)
            odd index's row goes into another part (1,3,5,7,9...)
        Output: two csv files 
'''

import operator
import csv
# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/9.13.19_h1n1_usa/"
csv_name = "0.009_divide_input.csv"
# ========================================================================================================

input_file = working_dir + csv_name
out_1st = working_dir + "1st_half.csv"
out_2nd = working_dir + "2nd_half.csv"

input_list = []  #save input data to a list
acc_amt_dict = {}  # count each row's amount of samples into a dict: {index_0:count_of_samples, index_1:count_of_samples, ...}
half_1st = [] 
half_2nd = []


def readCSV(filedir,listname):
    file = open(filedir)
    reader = csv.reader(file)
    for row in reader:
        listname.append(row) 


def write_csv(x,y):  # write list x into file y
    with open(y,'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()


def count_acc():  #count the number of samples
    index = 1  # iterate each row, start from the second row(index 1)
    while index < len(input_list):
        count = 1
        for i in input_list[index][0]:
            if i == '+':
                count += 1
        acc_amt_dict[index] = count
        index += 1


def distribute(x):  # equally distribute list x into two lists
    index = 0  # iterate sorted dict_list
    length = len(x)
    if length%2 ==0:  # if even length
        while index < length-1:
            half_1st.append(input_list[x[index][0]])
            half_2nd.append(input_list[x[index+1][0]])
            index = index + 2
    else:  # if odd length 
        half_1st.append(input_list[x[-1][0]])  # add the last one to 1st half, then treat the rest as even
        while index < length-2:  # -2 because need to -1 more to be even
            half_1st.append(input_list[x[index][0]])
            half_2nd.append(input_list[x[index+1][0]])
            index = index + 2
    
    
readCSV(input_file,input_list)  # save input data to list

count_acc()  # form a dict

# sort the dic, output a list of tuples [(index_0,count_of_samples), (index_1,count_of_samples), ...]
sorted_dic = sorted(acc_amt_dict.items(), key=operator.itemgetter(1)) 

half_1st.append(input_list[0])  # add position number row as first row
half_2nd.append(input_list[0])
distribute(sorted_dic)

write_csv(half_1st,out_1st)
write_csv(half_2nd,out_2nd)

print(f"Before sort, dict(index:count),len: {len(acc_amt_dict)} : \n {acc_amt_dict} \n")
print(f"After sort, [(index:count)], len: {len(sorted_dic)} : \n {sorted_dic} \n")
print("...Equally distribute...")
print(f"First half len: {len(half_1st)-1}")
print(f"Second half len: {len(half_2nd)-1} \n")

print("Running tests: ")
if len(sorted_dic)%2 ==0:
    print("  check 1st half: ")
    if (input_list[sorted_dic[0][0]][0]) == (half_1st[1][0]):
        if (input_list[sorted_dic[2][0]][0]) == (half_1st[2][0]):
            print("     Correct")
        else:
            print("     !!!WRONG!!!")
    else:
        print("     !!!WRONG!!!")
    
    print("\n  check 2nd half: ")
    if (input_list[sorted_dic[1][0]][0]) == (half_2nd[1][0]):
        if (input_list[sorted_dic[3][0]][0]) == (half_2nd[2][0]):
            print("     Correct")
        else:
            print("     !!!WRONG!!!")
    else:
        print("     !!!WRONG!!!")

else:
    print("  check 1st half: ")
    if (input_list[sorted_dic[-1][0]][0]) == (half_1st[1][0]):
        if (input_list[sorted_dic[0][0]][0]) == (half_1st[2][0]):
            print("     Correct")
        else:
            print("     !!!WRONG!!!")
    else:
        print("     !!!WRONG!!!")
    
    print("\n  check 2nd half: ")
    if (input_list[sorted_dic[1][0]][0]) == (half_2nd[1][0]):
        if (input_list[sorted_dic[3][0]][0]) == (half_2nd[2][0]):
            print("     Correct")
        else:
            print("     !!!WRONG!!!")
    else:
        print("     !!!WRONG!!!")



# equally distribute, sorted_dic's even index row & sorted_dic's odd index row

