#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 11:28:10 2019

@author: Changze Han
"""



'''
    For Flu project: 
    
    Input group name format must be 'Group_groupNumber_sampleNumber:' e.g.: 'Group_3_12:'
    
    Output group format: 
            'Group_3_12_14-15_0.009' 
            Meaning Group 3 contains 12 samples and its season is 14-15 with 0.009 grouping_threshold
'''           
                  
import csv 
from re import compile

# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/10.25.19_H3N2/human/15-19_season_USA/17-19/"
seq_filename = r"human_17-19_PNGS&Attributes.csv"
group_filename = r"groups_0.009.txt" 
output_filename = r"human_17-19_PNGS&Attributes&groups.csv"
threshold = 0.009  # for naming the group
season = '17-19'  # for naming the group  e.g.: '14-15'

accession_attribute_name = 'Sequence Accession'  # this is the name of accession attribute appears in the sequence file
# ==========================================================================================


seq_file = working_dir + seq_filename
group_file = working_dir + group_filename
out_file = working_dir + output_filename
ACCESSION_MATCHER = compile(r'[A-Za-z]{2}\d{6}|[A-Za-z]{1}\d{5}|[A-Za-z]{3}\d{5}')
group_name_ext = '_' + season + '_' + str(threshold)  # e.g.:  _14-15_0.009
acc_col_index = None  # index of accession_attribute_name in the sequence file

seq_list = []  # list store seq file
group_list = []  # list store group file
group_dic = {}  # {groupName:[accessionNumbers]}
r_group_dic = {}  # reverse group_dic  {accessionNum:groupName}
out_list = []  # store output lists

def read_csv(filedir,listname):
    file = open(filedir)
    reader = csv.reader(file)
    for row in reader:
        listname.append(row) 


def read_txt(x,y): # read a txt file x and store into a list y
    file = open(x,"r")
    for line in file:
        y.append(line)
        
        
def write_csv(x,y):  # write list x into file y
    with open(y,'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()
    
    
def getAccessNum(string):
    #extract accession from the given string, returns the first match if there are multiple matches
    return ACCESSION_MATCHER.findall(string)[0]


def find_acc_index():  
    global acc_col_index
    acc_col_index = seq_list[0].index(accession_attribute_name)
    

def const_group_dict():  # {groupName:[accessionNumbers]}
    global group_dic
    find_group_name = None
    for i in group_list:
        if 'Group' in i:
            find_group_name = i.rstrip()  # remove newline in the end of group name
            group_dic[find_group_name] = []
        else:
            try:
                group_dic[find_group_name].append(getAccessNum(i))
            except: 
                continue


def reverse_dict():  # reverse group_dic to {accessionNum:groupName}
    global r_group_dic
    for i in group_dic:
        for j in group_dic[i]:
            r_group_dic[j] = i[:-1]+group_name_ext
            

def match():  # match each sequence with a group name
    global out_list
    out_list.append(['Group']+seq_list[0])  # add header row
    for i in seq_list[1:]:  # exclude header row
        temp_list = i
        temp_list.insert(0,r_group_dic[i[acc_col_index]])  # add the group name to the start of the sequence attributes
        out_list.append(temp_list)



read_csv(seq_file, seq_list)  # load the sequence file
read_txt(group_file, group_list)  # load the all_attributes file
find_acc_index()  
const_group_dict() # construct the group name dict  key:value
reverse_dict()  # reverse the dict  value:key
match()  # match the group name with seq
write_csv(out_list, out_file)  # write output
# check group_dict length
print("Check group_dict: ")
total_samples = 0
for i in group_dic:
    total_samples = total_samples + len(group_dic[i])
    print(f"     {i}     {len(group_dic[i])}")
print(f"  total sample number = {total_samples} \n")

# check reverse_group_dict length
print("Check reverse_group_dict: ")
if len(r_group_dic) != total_samples:
    print("  !!!SAMPLE NUMBER DOESN'T MATCH!!! SOMETHING WRONG!!! ")
    print(f"  total sample number = {len(r_group_dic)} \n")
else:
    print(f"  total sample number = {len(r_group_dic)}  CORRECT! \n")

# check output list
print("Check output lists: ")
if (len(out_list) - 1) != total_samples:
    print("  !!!OUTPUT SAMPLE NUMBER DOESN'T MATCH!!! SOMETHING WRONG!!! ")
    print(f"  Output file contains {len(out_list) - 1} samples")
else:
    print(f"  Output file contains {len(out_list) - 1} samples  CORRECT! ")
    
    
    
    
    
    
    
    
    
    
    
    
    