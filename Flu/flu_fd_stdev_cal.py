#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 11:29:05 2019

@author: Changze Han
"""


'''
    For Flu Project:
    Select a specific group of samples(based on different identifier) and then calculate FD & Stdev: 
    
    Allow user to select from: position range
                               Flu Season: single season(13-14) or multiple season (13-16)
                               Group : calculate FD for each group
                               State/Province
                               Country
                               a list of accession numbers


    Ignore '?' '-' during the FD calculation: 
        e.g:  a position column has 10 AA, one of them is ?, then the total count of AA of this 
              position column is 9. When calculating the frequency distribution, divide by 9. 
    
    For HIV Project: (this program can also perform some fd calculations in HIV)
        1. single sample: change the group_attribute_name to 'Patient'
'''

import pandas as pd
import csv
import numpy as np
#import statistics 
#from constants import HYDROPATHY_SCORE_TABLE

# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/5.10.21 B gp120 gp160dynaFD/6.7.21/new c FD/"
#r"/Users/Han/Documents/Haim_Lab(2018_summer)/9.25.19_new_accession(H1N1_USA)/06-19_season/season_FDs/"
seq_filename = r"long C png seq(new patients).csv"
fd_output_filename = r"Clade B gp160 Dyna-FD.csv"
# if selection_name is group, then 1. this fd output file name doesn't matter 
#                                  2. make sure to make a new folder to perfrom FD for group selection(due to large amount of outputs)
stdev_output_filename = r"test_stdev.csv"  
# if need_stdev is False, then stdev output file name doesn't matter


#option 1:
season_attribute_name = 'Flu Season'  # this is the name of season attribute appears in the sequence file
#option 2:
group_attribute_name = 'Patient-Days' #'Patient-Days'#'Group'  # this is the name of group attribute appears in the sequence file
#option 3:
state_attribute_name = 'State/Province'  # this is the name of state attribute appears in the sequence file
#option 4:
country_attribute_name = 'Country'  # this is the name of country attribute appears in the sequence file
#option 5:
accession_attribute_name = 'Sequence Accession'  # value e.g.: ['KU591055', 'KU591039', 'KU590350']

# select identifier : 
selection_name = group_attribute_name  # choose from 5 options above
# select cutoff/value/... : 
selection_value = 0 #'15-16'
# 1. if 'Flu Season' is selected, you can also do multiple 
#    years : type '13-16' and it will combine 13-14,14-15,15-16
# 2. if 'Group' is selected, then selection_value is the group size cutoff value,
#    cutoff meaning: ignore groups that have sample numbers <= cutoff value
# 3. if 'Sequence Accession' is selected, then the selection_value is a list of accession numbers, 
#      e.g.: ['KU591055', 'KU591039', 'KU590350']

# remember to change the position range based on different flu type
# e.g: H1N1--(1,549)   H3N2--(1,550)
position_range = (1, 856)
 
need_stdev = False  # True : if want to calculate stdev  False: only calculate FD
zero_thresh = float('1e-5')  # stdev values < zero_thresh will be assigned zero
# ==========================================================================================


seq_file = working_dir + seq_filename
buffer_file = r"buffer.csv"  # store sequences after the selection, for debugging 
buffer_file = working_dir + buffer_file
fd_out_file = working_dir + fd_output_filename
stdev_out_file = working_dir + stdev_output_filename
AA=['Z','N','T','S','D','E','K','R','H','Y','Q','I','L','V','A','C','F','G','M','P','W']#,'B']


seq_list = []  # list store seq file
selection_list = []  # store lists after selection
df = None  # dataframe for selection_list in FD cal
df_sd = None # dataframe for selection_list in stdev cal
fd_out_list = []  # store FD output lists
stdev_out_list = []  # store stdev output lists
group_name_list = []  # store the distinct group names
fd_zip_output = []  # save ziped fd out list, will be wrote in output file
#stdev_zip_output = []  # save ziped stdev out list, will be wrote in output file


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


def generate_season_range(x):  # x = '13-16', output = ['13-14','14-15','15-16']
    output = []
    dash_index = x.index('-')
    start_year = int(x[:dash_index])
    end_year = int(x[dash_index+1:])
    if ((end_year) - (start_year)) >1:
        while ((start_year+1)<= end_year): 
            fix_1st_year = start_year
            fix_2nd_year = start_year+1
            if fix_1st_year < 10:
                fix_1st_year = f'0{fix_1st_year}'
            if fix_2nd_year < 10:
                fix_2nd_year = f'0{fix_2nd_year}'
            output.append(f"{fix_1st_year}-{fix_2nd_year}")
            start_year += 1
        return output
    else:
        output.append(x)
        return output


def generate_group_name_list():
    global group_name_list
    group_att_index = seq_list[0].index(group_attribute_name)
    for i in seq_list[1:]:
        if i[group_att_index] not in group_name_list:
            group_name_list.append(i[group_att_index])



def select_rows(name,value):  #select rows based on target attribute 'name' and target value 'value'
    global selection_list
    selection_list = []  # reset list
    selection_list.append(seq_list[0])  # add header row 
    target_name_index = seq_list[0].index(name)  # find the index of target_attribute in header row
    if name != group_attribute_name:
        print(f"{name} index: {target_name_index}")
    # if want to select seasons: 
    if name == season_attribute_name:  
        print(f"Season selected: \n  {generate_season_range(value)}")
        season_range = generate_season_range(value)
        for i in seq_list[1:]:  # exclude header row
            if i[target_name_index] in season_range:  # check season
                selection_list.append(i)
    
    #if want to select states or country: 
    if (name == state_attribute_name) or (name == country_attribute_name):
        for i in seq_list[1:]:
            if i[target_name_index] == value:
                selection_list.append(i)
    
    # if want to select groups: 
    if name == group_attribute_name:
        for i in seq_list[1:]:
            if i[target_name_index] == value:
                selection_list.append(i)
    
    # if want to select a list of accession numbers
    if name == accession_attribute_name: 
        for i in seq_list[1:]:
            if i[target_name_index] in value:
                selection_list.append(i)

def calculate_fd_stdev(x,y):  # x = position_range   e.g. (1,549); y is the title added to right corner of output
    global fd_out_list
    fd_out_list = []  # reset
    global stdev_out_list
    stdev_out_list = []  # reset 
    header_row = seq_list[0]
    #construct a dataframe for the selected lists
    global df
    df = pd.DataFrame(selection_list[1:], columns = header_row)
    
    HYDROPATHY_SCORE_TABLE = {
            'A': 0.68,
            'C': 0.733,
            'D': 0.19,
            'E': 0.203,
            'F': 1,
            'G': 0.584,
            'H': 0.304,
            'I': 0.958,
            'K': 0.403,
            'L': 0.953,
            'M': 0.782,
            'N': 0.363,
            'P': 0.759,
            'Q': 0.376,
            'R': 0.167,
            'S': 0.466,
            'T': 0.542,
            'V': 0.854,
            'W': 0.898,
            'Y': 0.900,
            'Z': 0,
            '-': 1.5}
            #,'B': 1.5}
    
    fd_out_list.append([f'{y}'] + AA + ['Sample#'])  # add header col for the fd output
    stdev_out_list.append(['Sample#'] + ['Group'] + list(range(position_range[0],position_range[1]+1)))  # add header col for stdev output
    stdev_out_list.append([len(selection_list)-1] + [f'{y}'])  # add sample number & group identifier to stdev output
                           
    i = x[0]   # start from the first position in the position range
    while ((i >= x[0]) and (i <= x[1])):
        total_count = 0  # count the total sample number of this position
        aa_count_dic = {'Z':0
                        ,'N':0
                        ,'T':0
                        ,'S':0
                        ,'D':0
                        ,'E':0
                        ,'K':0
                        ,'R':0
                        ,'H':0
                        ,'Y':0
                        ,'Q':0
                        ,'I':0
                        ,'L':0
                        ,'V':0
                        ,'A':0
                        ,'C':0
                        ,'F':0
                        ,'G':0
                        ,'M':0
                        ,'P':0
                        ,'W':0}  # store the count of each AA, reset for each position
                        #,'B':0}
        aa_count_list = []  # store aa count(values of dict) to a list, first element is the position
        aa_pct_list = []  # store the percentages of aa to a list
        hyd_stdev_list = []  # store the hydropathy value list of this position
        
        aa_list = df[str(i)].tolist()  # use dataframe to extract the column of this position
        
        #print(aa_list)
        for j in aa_list:
            if j in list(aa_count_dic.keys()):   # only count AA, ignore '?' '-'
                aa_count_dic[j] = aa_count_dic[j] + 1  # count the AA and add number in dict
            if j in list(HYDROPATHY_SCORE_TABLE.keys()):  # hydropathy value doesn't have '?' '-' 
                hyd_stdev_list.append(HYDROPATHY_SCORE_TABLE[j])  # assign a hydro value to this AA and add add the value to list
        

        
        pure_aa_list = list(aa_count_dic.values())  # transfer the value of dict to a list
        total_count = sum(list(aa_count_dic.values()))  # total sample count of this position
        
        aa_count_list = pure_aa_list[:]
        aa_count_list.insert(0,i)  # add position to the front of the list
        aa_count_list.append(total_count)  # add the total sample number of this position to the end
        # calculate percentage
        for k in pure_aa_list:
            if total_count != 0:
                aa_pct_list.append(k/total_count*100)  # calculate %
            else:
                aa_pct_list.append(0)
        aa_pct_list.insert(0,i)
        aa_pct_list.append(total_count)
        
        fd_out_list.append(aa_pct_list)  # add to the output list
        #print(hyd_stdev_list)
        
        temp_std = np.std(hyd_stdev_list)  # temporary place for stdev value
        if temp_std > zero_thresh:  # check the zero_thresh
            stdev_out_list[1].append(temp_std) # add this pos's stdev to the 2nd row of the output which is the stdev value row
        else:
            stdev_out_list[1].append(0)

        '''
            For Debug purpose: replace the above line with this line (see the count of aa instead of pct)
        fd_out_list.append(aa_count_list)  
        '''
        i += 1
    del df  # clean the dataframe memory


def zip_list(x,y):  # zip x then save to y
    zip_output_tuple = list(zip(*x))
    for i in zip_output_tuple:
        y.append(list(i))


def main():
    global fd_zip_output
    #global stdev_zip_output
    if selection_name == group_attribute_name:  # calculate data based on group
        read_csv(seq_file, seq_list)
        generate_group_name_list()
        print(f"Original sequence file contains {len(seq_list)-1} samples")
        print(f"{len(group_name_list)} groups total\n")
        all_group_stdev_output = []  # combine all group's stdev together into one file
        check_count = 0
        for i in group_name_list:
            select_rows(selection_name,i)
            if (len(selection_list)-1) <= (selection_value):  # cutoff, ignore low sample number groups
                continue
            print(f"{i}: {len(selection_list)-1} samples are selected to calculate FD")
            calculate_fd_stdev(position_range, i)
            fd_zip_output = []  # reset for each group's output
            zip_list(fd_out_list, fd_zip_output)   # zip the fd output
            write_csv(selection_list, f"{working_dir}Buffer({i}).csv")  # write the selection list file
            write_csv(fd_zip_output, f"{working_dir}FD({i}).csv")  # write fd output file
            
            all_group_stdev_output.append(stdev_out_list[1])  # only add the stdev value row (index 0 is attributes row)
            
            check_count += 1
        print(f"\nChecking ...... {check_count} groups are calculated. ")
        all_group_stdev_output.insert(0,stdev_out_list[0])  # add the header row
        if need_stdev == True:
            write_csv(all_group_stdev_output, stdev_out_file)  # write stdev output file
            print("\n* StDev is also calculated in the same selected samples.   ")       
    else:  # calculate data based on different attributes
        read_csv(seq_file, seq_list)
        select_rows(selection_name,selection_value)
        print(f"\nOriginal sequence file contains {len(seq_list)-1} samples")
        print(f"After the selection, {len(selection_list)-1} samples are selected to calculate FD")
        calculate_fd_stdev(position_range, selection_value)
        zip_list(fd_out_list, fd_zip_output)  # zip the fd output
        write_csv(selection_list, buffer_file)  # write the selection list file
        write_csv(fd_zip_output, fd_out_file)  # write fd output file
        if need_stdev == True:  # calculate stdev
            write_csv(stdev_out_list, stdev_out_file)  # write stdev output file
            print("\n* StDev is also calculated in the same selected samples.   ")            


main()



