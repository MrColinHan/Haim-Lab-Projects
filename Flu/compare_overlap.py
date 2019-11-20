#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 15:23:04 2019

@author: Changze Han
"""

import csv
# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/10.25.19_H3N2/human/15-19_season_USA/10-19(rm_dup)/stdev/";
group1_name = "1st_pos_pairs_all.csv";
group2_name = "2nd_pos_pairs_all.csv"
out_name = "compare_2_groups_all.csv"
# ========================================================================================================
group1_file = working_dir + group1_name
group2_file = working_dir + group2_name
out_file = working_dir + out_name
group1_list = []
group2_list = []


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
    

read_csv(group1_file, group1_list)
read_csv(group2_file, group2_list)


overlap_list = []  # store overlap pos pairs (pos1, pos2, p_value)
rest_group1_list = []  # store remaining group1 pos pairs
rest_group2_list = []  # store remaining group2 pos pairs


def find_overlap():  # find overlap pairs
    for i in group1_list:  
        for j in group2_list:
            if (i[0],i[1]) == (j[0],j[1]):
                #print(str((i[0],i[1])) + " vs " + str((j[0],j[1])))
                overlap_list.append(i+[j[2]])
       

# check the remaining pos pairs in two groups
overlap_pos_pairs = []  # store [pos1,pos2] of each overlaping pairs (pos1, pos2, p_value)

def get_pos_pair():
    for i in overlap_list: 
        overlap_pos_pairs.append([i[0],i[1]])


# the rest group1 pairs
def find_rest_group1():
    for i in group1_list:
        if [i[0],i[1]] not in overlap_pos_pairs:
            rest_group1_list.append(i)


# the rest group2 pairs
def find_rest_group2():       
    for i in group2_list:
        if [i[0],i[1]] not in overlap_pos_pairs:
            rest_group2_list.append(i)



find_overlap()  # overlap [(pos1, pos2, p_value)]
get_pos_pair()  # [[pos1,pos2]]
find_rest_group1()  # remaining group1 [(pos1, pos2, p_value)]
find_rest_group2()  # remaining group2 [(pos1, pos2, p_value)]

overall_list = []  # combine 3 lists together in order to write in an overall csv file
print(f"overlap pairs: {len(overlap_list)}")
print(f"rest pairs in group1: {len(rest_group1_list)}")
print(f"rest pairs in group2: {len(rest_group2_list)} \n")
print(f"original pairs group1: {len(group1_list)}")
print(f"original pairs group2: {len(group2_list)}")
overall_list = [["overlap position pairs:"],["pos1","pos2","1st half p","2nd half p"]] + overlap_list + [[]] + [["Remaining 1st half:"],["pos1","pos2","1st half p"]] + rest_group1_list + [[]] + [["Remaining 2nd half:"],["pos1","pos2","2nd half p"]] + rest_group2_list
write_csv(overall_list,out_file )

            
            