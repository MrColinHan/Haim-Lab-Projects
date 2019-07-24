#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 13:44:03 2019

@author: Han
"""
import csv 
'''
    This script takes a gp120 csv file as input and remove a given list of samples from it
    output: 1. remaining AA after the removing
            2. removed sequences
'''
AAFile = r"/Users/Han/Documents/Haim_Lab(2018_summer)/7.23.19_fig4_centroids/clean_sequence/regional/A1_OTH_remaining2.csv"
need_to_rm_file = r"/Users/Han/Documents/Haim_Lab(2018_summer)/7.23.19_fig4_centroids/clean_sequence/A1_remove_list.csv"

OutputDir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/7.23.19_fig4_centroids/clean_sequence/regional/"
remaining_output = "A1_OTH_remaining3.csv"
removed_output = "A1_OTH_non_functional3.csv"


AAList = [] # store the AAFlie
remove_access = [] # store the need_to_rm_access File
rm_access_str_list = [] # store the remove_access into a list of strings


def readCSV(filedir,listname):
    file = open(filedir)
    reader = csv.reader(file)
    for row in reader:
        listname.append(row) 
        
readCSV(AAFile,AAList)
readCSV(need_to_rm_file,remove_access)
#=================output lists====================
remaining_output_list = AAList.copy() # copy AAList and keep poping rm samples from here, 
                                      # so original AAList will never be changed
#print(remaining_output_list)
removed_output_list = []
#=================================================
#print(remove_access)

for i in remove_access: # store the rm list into a list of strings
    rm_access_str_list.append(i[0])
#print(rm_access_str_list)

#check each sample's accession number to see if it appears in the rm_access_str_list
i = 0
while i < len(remaining_output_list):
    if remaining_output_list[i][3] in rm_access_str_list:
        removed_output_list.append(remaining_output_list.pop(i))
    else:
        i += 1
#print(removed_output_list[0][:4])
#print(len(remaining_output_list))

print("\n"+"Original AA sequence had " + str(len(AAList)-1) + " samples" + "\n")

print(str(len(rm_access_str_list))+" samples are supposed to be removed: " 
      + "\n" + str(rm_access_str_list) + "\n")

print(str(len(removed_output_list)) + "/" + str(len(rm_access_str_list)) + " samples are found" + "\n")

print("removing..." + "\n")

print("Now, remaining AA sequence has "+ str(len(remaining_output_list)-1) 
      + " samples, "+ str(len(removed_output_list)) + " samples are removed. " + "\n")

if ((len(remaining_output_list) + (len(removed_output_list))) != len(AAList)): 
    print("Total number doesn't add up, DOUBLE CHECK !!! ")

print("Removed samples: ")
print_rm = []
for i in removed_output_list:
    print_rm.append(i[3])
print(print_rm)

def writeCsv(x,y,z): # x is input list, y is OutputDir, z is OutputName
    with open(y+z,'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()
            
writeCsv(remaining_output_list,OutputDir,remaining_output)
removed_output_list.insert(0,AAList[0])
writeCsv(removed_output_list,OutputDir,removed_output)


        
        
        

        
    
