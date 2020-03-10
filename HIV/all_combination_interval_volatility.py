"""
Created on Mar 10 2020

@author: Changze Han
"""

import csv
import numpy as np
import random
import copy
import math

'''
    For HIV Volatility project: 

    Given a target position, prepare the data for further temporal persistence analysis by calculating the 
    all combinations's interval volatility. 

    Algorithm: 
        1. For each patient: 
                for each day, form all combinations with the days after it.
                And separate the combinations into 2 groups: "start as 0 volatility" --- first day is 0 volatility 
                                                             "start as 1 volatility" --- first day is 1 volatility
            e.g. 
                | patient |  aaa   aaa   aaa   aaa   aaa   aaa
                |   days  |   0    50    100   200   500   1000  
                |  pos295 |   0     0      1     1    0      1 
                Then : 
                    START as 0 group includes : 
                       | days pair | interval | volat1 |  volat2 |
                       |  0,50     |   50     |   0    |    0    | 
                       |  0,100    |   100    |   0    |    1    |
                       |  0,200    |   200    |   0    |    1    | 
                       |  0,500    |   500    |   0    |    0    |
                       |  0,1000   |   1000   |   0    |    1    |
                       --------------------------------------------
                       |  50,100   |    50    |   0    |    1    | 
                       |  50,200   |    150   |   0    |    1    | 
                       |  50,500   |    450   |   0    |    0    | 
                       |  50,1000  |   1000   |   0    |    1    | 
                       --------------------------------------------
                       |  500,1000 |   500    |   0    |    1    | 
                       
                    START as 1 group includes: 
                       | days pair | interval | volat1 |  volat2 |
                       |  100,200  |   100    |   1    |    1    | 
                       |  100,500  |   400    |   1    |    0    | 
                       |  100,1000 |   900    |   1    |    1    | 
                       --------------------------------------------
                       |  200,500  |   300    |   1    |    0    | 
                       |  200,1000 |   800    |   1    |    1    | 
                        
        2. output two files: 
            one for combinations 'start as 0 volatility'
            one for combinations 'start as 1 volatility'
                                

    Input file: 
        1. should have a header row
        2. should do a two level sort on the input file in Excel before run the program: sort patient then sort days
                e.g.    
                    | Patient | Days | 137 | 289 | 295 | 
                    |   aaa   |   0  |  1  |  0  |  1  | 
                    |   aaa   |  10  |  1  |  0  |  0  | 
                    |   aaa   |  160 |  1  |  0  |  1  | 
                    |   bbb   |   0  |  1  |  0  |  1  | 
                    |   bbb   |  50  |  1  |  0  |  0  | 
        3. then transpose paste
                e.g. 
                    | Patient | aaa | aaa | aaa | bbb | bbb |
                    |  Days   |  0  |  10 | 160 |  0  |  50 | 
                    |   137   |  1  |  1  |  1  |  1  |  1  | 
                    |   289   |  0  |  0  |  0  |  0  |  0  | 
                    |   285   |  1  |  0  |  1  |  1  |  0  |
'''

# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/3.10.20_interval_volatility/"
in_csv_name = "C_Long_binary_volat_10pos.csv"
out_csv_name = "(448)C_all_comb"  # no '.csv' at the end

patient_col = 3  # patient name col
days_col = 4  # days col
pos_col = 14  # target position col that contains volatility
# ========================================================================================================
input_file = working_dir + in_csv_name
output_file_start_as0 = working_dir + f"{out_csv_name}(start as 0).csv"
output_file_start_as1 = working_dir + f"{out_csv_name}(start as 1).csv"

input_file_list = []
output_file_start_as0_list = []
output_file_start_as1_list = []

# construct a dict for each patient: key is patient, value is [[days list], [volatility list]]
pat_vola_days_dict = {}


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


def main():
    global output_file_start_as0_list
    global output_file_start_as1_list
    global pat_vola_days_dict
    read_csv(input_file, input_file_list)  # read input file

    # construct a dict for each patient: key is patient, value is [[days list], [volatility list]]
    for row in input_file_list[1:]:
        current_name = row[patient_col]
        current_volatility = row[pos_col]
        current_day = row[days_col]
        if current_name not in pat_vola_days_dict:
            pat_vola_days_dict[current_name] = [[current_day], [current_volatility]]
        else:
            pat_vola_days_dict[current_name][0].append(current_day)
            pat_vola_days_dict[current_name][1].append(current_volatility)

    # construct combinations and format outputs
    output_file_start_as1_list.append(["patient", "days pair", "interval", "volatile state1", "volatile state2"])
    output_file_start_as0_list.append(["patient", "days pair", "interval", "volatile state1", "volatile state2"])
    for name in pat_vola_days_dict:
        cur_name_days = pat_vola_days_dict[name][0]
        cur_name_volat = pat_vola_days_dict[name][1]
        for vol_i in range(len(cur_name_volat)):
            if int(cur_name_volat[vol_i]) == 0:  # assign to 'start as 0 volatility' group
                next_vol_i = copy.deepcopy(vol_i)
                next_vol_i += 1
                while next_vol_i < len(cur_name_volat):
                    output_file_start_as0_list.append([f"{name}",
                                                       f"{cur_name_days[vol_i]}---{cur_name_days[next_vol_i]}",
                                                      abs(int(cur_name_days[next_vol_i])-int(cur_name_days[vol_i])),
                                                      cur_name_volat[vol_i],
                                                      cur_name_volat[next_vol_i]])
                    next_vol_i += 1

            if int(cur_name_volat[vol_i]) == 1:  # assign to 'start as 1 volatility' group
                next_vol_i = copy.deepcopy(vol_i)
                next_vol_i += 1
                while next_vol_i < len(cur_name_volat):
                    output_file_start_as1_list.append([f"{name}",
                                                       f"{cur_name_days[vol_i]}---{cur_name_days[next_vol_i]}",
                                                      abs(int(cur_name_days[next_vol_i])-int(cur_name_days[vol_i])),
                                                      cur_name_volat[vol_i],
                                                      cur_name_volat[next_vol_i]])
                    next_vol_i += 1



    # checking:
    check_total_sample_number = len(input_file_list)-1
    for key in pat_vola_days_dict:
        check_total_sample_number -= len(pat_vola_days_dict[key][0])
    if check_total_sample_number != 0:
        raise ValueError("Total sample number WRONG in the dict.")


    print(f"{len(input_file_list)-1} patient samples")
    print(f"target position: {input_file_list[0][pos_col]}")
    print(pat_vola_days_dict)

    write_csv(output_file_start_as1_list, output_file_start_as1)
    write_csv(output_file_start_as0_list, output_file_start_as0)



main()











