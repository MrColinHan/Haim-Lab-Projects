#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 11:14:25 2019

@author: Han
"""


'''
    For FLU project: (NEW Program, used on new stdev cal's output)
    This script equally distribute x groups into 2 parts in order to run the fisher 
    test fairly. 
    How it works: 
        Input: stdev output of flu_fd_stdev_cal.py, 
               Before put the input in this program: 
                      1. sort the file by sample number in Excel from largest to smallest
                      2. delete samples less than a certain cutoff number (e.g: 10)
        
        Output: two csv files
        
        program procedure: 
            even index's row goes into one part (0,2,4,6,8...)    (doesn't count header row)
            odd index's row goes into another part (1,3,5,7,9...) (doesn't count header row)     
'''

import csv
# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/12.5.19_hiv_single/volatility/"
csv_name = "B_volatility_need_separate.csv"
# ========================================================================================================

input_file = working_dir + csv_name
out_1st = working_dir + "1st_half.csv"
out_2nd = working_dir + "2nd_half.csv"

input_list = []  # save input data to a list
half_1st = []  # for output
half_2nd = []  # for output


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


def main():
    global input_list
    global half_1st
    global half_2nd
    
    readCSV(input_file, input_list)  # read input file
    
    input_list_no_header = input_list[1:]  # remove header and then save to a list
    
    total_count = 0 
    for i in input_list_no_header:  # record the total count of input file
        total_count += int(i[0])
    print(f"\nInput file contains {len(input_list)-1} groups. Total sample number: {total_count}\n")
    
    half_1st.append(input_list[0])  # add header row
    half_2nd.append(input_list[0])
    
    for row_i in range(len(input_list_no_header)):
        if row_i % 2 == 0: 
            half_1st.append(input_list_no_header[row_i])
        else:
            half_2nd.append(input_list_no_header[row_i])
    
    half_1st_count = 0
    half_2nd_count = 0
    for j in half_1st[1:]:
        half_1st_count += int(j[0])
    for k in half_2nd[1:]:
        half_2nd_count += int(k[0])
    
    print(f"1st part output contains {len(half_1st)-1} groups. Total sample number: {half_1st_count}")
    print(f"2nd part output contains {len(half_2nd)-1} groups. Total sample number: {half_2nd_count}")
    
    print("\n   Checking......   ")
    print(f"        {len(half_1st)-1} + {len(half_2nd)-1} = {len(half_1st)-1 + len(half_2nd)-1} ----vs---- {len(input_list)-1}")
    print(f"        {half_1st_count} + {half_2nd_count} = {half_1st_count + half_2nd_count} ----vs---- {total_count}")
    
    write_csv(half_1st, out_1st)  # write first output
    write_csv(half_2nd, out_2nd)  # write second output
    
    
main()
    
















