#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 03:08:21 2019

@author: Changze Han
"""

'''
    For FLU project: 
    
    This script takes co-volatility matrix as input file and extract 
    a list of position pairs based on the given p_value range. 
     
'''

import csv
# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/12.5.19_hiv_single/volatility/"
csv_name = "(bin)2nd_fisher_p.csv"
out_name = "(bin)2nd_fisher_p_pairs"   # no need to put a suffix
p_range = (0, 10000)  # cutoff for p value: (0,0.05) means  0 < p < 0.05
# ========================================================================================================

input_file = working_dir + csv_name
input_list = []  #save input data to a list
out_file_txt = working_dir + out_name + ".txt"
out_file_csv = working_dir + out_name + ".csv"


def read_csv(filedir,listname):
    file = open(filedir)
    reader = csv.reader(file)
    for row in reader:
        listname.append(row) 
        
def write_txt(x,y): # write the list x into y txt file
    output= open(y,"w+") 
    for i in x:
        output.write(str(i)+"\n")
    output.close


def write_csv(x,y):  # write list x into file y
    with open(y,'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()


# take a range (0,0.5) as input and loop for position pairs, and then return a list of pos pairs. 
# if x == y then look for p_value = x, else look for x<p_value<y 
def look_up(x,y):
    row = 1  # index to iterate rows, skip header row index = 0, start from 1
    out_list = []  # use to save output list
    while row < len(input_list):
        column = row+1  # set column = row + 1, because only want to look at right top half of the matrix
        while column < len(input_list[row]):
            if (float(input_list[row][column]) > x) and (float(input_list[row][column]) < y) :
                out_list.append([input_list[0][column],input_list[row][0],input_list[row][column]])
                #print(input_list[row][column])
            column += 1
        row += 1     
    return out_list



read_csv(input_file, input_list)  # load input to a list
output = look_up(*p_range)  # search & extract position pairs
#print(output)

#write_txt(output,out_file_txt)
write_csv(output,out_file_csv)

print(f"Between range {p_range[0]} < p_value < {p_range[1]} found : {len(output)} position pairs")



