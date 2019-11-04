#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 02:27:35 2019

@author: Changze Han
"""

'''
    For Flu Project:
    Input: 
           1. a text file contains all grouped accession numbers
           2. a csv file contains PNGS converted AA sequences
    Expected output: 
        Give the program a group name, then it will extract all the corresponding 
        AA sequences from the csv AA file and generated a new csv file as output. 
        (in another work, the output is part of the original AA csv file)
    
'''

import csv 

# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/9.20.19_h1n1/10-15_season(cleaned_51_non-human)/divide_group0_based_on_162pos/";
AA_csv_filename = "G.10-15_season_H1N1_USA_AA_PNGS_csv.csv"
grouped_txt_filename = "I.groups_0.009.txt"
output_name = "Group0_AA.csv"

target_group_name = 'Group-0-615'
# ========================================================================================================
target_group_name = target_group_name + ':\n'
csv_input_file = working_dir + AA_csv_filename
txt_input_file = working_dir + grouped_txt_filename
output_file = working_dir + output_name

csv_input_list = []
txt_input_list = []
group_dict = {}  # {group_name:(group_name_index, group_length)}
target_group_acc_list = []  # store the target group's access numbers
target_group_AA_seq = []

def read_csv(filedir,listname):
    file = open(filedir)
    reader = csv.reader(file)
    for row in reader:
        listname.append(row) 
        
        
def read_txt(x,y): # read a text file x and store into a list y
    file = open(x,"r")
    for line in file:
        y.append(line)
        
def write_csv(x,y):  # write list x into file y
    with open(y,'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()
        

def construct_dict():
    i = 0  # index for the list
    list_len = len(txt_input_list)
    while i<list_len:
        if 'Group' in txt_input_list[i]:  # find the string contains group name
            # now find the group length for each group
            find_dash = 0  # keep track of the dash, int after the 2nd dash is group_length
            j = 0  # index for the group name string
            while j < len(txt_input_list[i]):
                if txt_input_list[i][j] == '-':
                    find_dash += 1
                    if find_dash == 2:
                        group_dict[txt_input_list[i]] = (i,int(txt_input_list[i][j+1:-2]))  # [:-2] remove the ending ':\n'         
                j += 1
        i += 1

def extract_tar_acc_nums():  # return the target group's all acc nums
    acc_start_at = group_dict[target_group_name][0] + 1
    acc_end_at = group_dict[target_group_name][0] + group_dict[target_group_name][1] + 1
    return(txt_input_list[acc_start_at:acc_end_at])


def rm_end_char(x):  # remove \n at the end of each accession number
    i = 0
    while i < len(x):
        x[i] = x[i][:-1]
        i += 1
    

def match_csv(x):  # match accession number list x with AA csv file
    target_group_AA_seq.append(csv_input_list[0]) # add the header row
    for i in csv_input_list:
        if i[0] in x:
            target_group_AA_seq.append(i)




read_csv(csv_input_file, csv_input_list)  # read csv to a list
read_txt(txt_input_file, txt_input_list)  # read txt to a list
construct_dict()  # construct dict
target_group_acc_list  = extract_tar_acc_nums()  # get all acc nums of this group
rm_end_char(target_group_acc_list)  #  remove \n at the end of each accession number
match_csv(target_group_acc_list)  # match accession list with AA sequence
write_csv(target_group_AA_seq,output_file)  # write output
print(f"Check accession numbers in group {target_group_name[:-1]}")
print(f"First accession number in this group is {target_group_acc_list[0]}")
print(f"Last accession number in this group is {target_group_acc_list[-1]}")
print(f"\nDouble check output sequence count: {len(target_group_AA_seq)-1}")
        
















        
        
        
        
        
        
        
        
        
        
        
        
        
        