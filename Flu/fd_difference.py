#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 14:41:24 2019

@author: Han
"""

'''
    For Flu Project: 
        Compare FD between two seasons and calculate the difference
        (sum of absolute value of each AA's pct's difference)
'''
import csv 


# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/9.25.19_new_accession(H1N1_USA)/compare_fd/"
fd1_filename = r"17-18_FD.csv"
fd2_filename = r"18-19_FD.csv"
output_filename = r"17-18_vs_18-19.csv"
pct_threshold = 50  # if pct difference is larger than this number, then put in output
# ==========================================================================================

fd1_file = working_dir + fd1_filename
fd2_file = working_dir + fd2_filename
out_file = working_dir + output_filename

fd1_list = []
fd2_list = []
zip_fd1_list = []
zip_fd2_list = []

diff_val_list = []  # a list to store each position's difference value 
cutoff_pos_list = []  # store part of diff_val_list based on pct_threshold, position row
cutoff_val_list = []  # store part of diff_val_list based on pct_threshold, value row
out_list = []


def read_csv(filedir,listname):
    file = open(filedir)
    reader = csv.reader(file)
    for row in reader:
        listname.append(row) 
        
        
def write_csv(x,y):  # write list x into file y
    with open(y,'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()


def zip_rows_get_cols(x,y):  # zip list x then store in new list y
    zip_out_tuple = list(zip(*x))
    for i in zip_out_tuple:
        y.append(list(i))


def cal_diff(zip_one,zip_two):  # calculate difference between season one and season two (use zipped lis tfile)
    global out_list
    global diff_val_list
    header_row = fd1_list[0]
    header_row[0] = 'Position'
    out_list.append(header_row)  # add the position header row in the output
    diff_val_list.append('pct_Difference')  # add a title to the second row of the output
    
    cutoff_pos_list.append('Position')
    cutoff_val_list.append(f'diff >= {pct_threshold}')
    
    position = 1  # position, start at index 1, index 0 is the 'Position,Z,N,T,S....'title row
    while position<len(zip_one):
        diff_sum = 0
        aa = 0  # amino acid index 0-20 
        while aa < len(zip_one[position][1:-1]):  # [1:-1] remove position number and sample number
            diff_sum = diff_sum + abs(float(zip_one[position][1:-1][aa]) - float(zip_two[position][1:-1][aa]))
            aa += 1
        diff_val_list.append(diff_sum)
        if diff_sum >= pct_threshold:
            cutoff_pos_list.append(position)
            cutoff_val_list.append(diff_sum)
        
        position += 1
    out_list.append(diff_val_list)
    if pct_threshold != 0:
        out_list.append([])
        out_list.append(cutoff_pos_list)
        out_list.append(cutoff_val_list)


read_csv(fd1_file, fd1_list)
read_csv(fd2_file, fd2_list)

zip_rows_get_cols(fd1_list,zip_fd1_list)
zip_rows_get_cols(fd2_list,zip_fd2_list)

cal_diff(zip_fd1_list,zip_fd2_list)

write_csv(out_list, out_file)


    








