"""
Created on Jan 27 2021

@author: Changze Han
"""

'''
    For HIV Volatility project: 

        Input data: 
            two CSV file2
            1. average loop length for each patient (output from 'average_each_patient_data.py')
            2. volatility data

        process: 
            add the loop length as extra attributes for each corresponding patient in the volatility data

        output: 
            CSV file
'''

import csv
import numpy as np

# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/1.26.21_HIV_Volatility_single/"
volatility_input_name = r"single_B_VolatilityData.csv"
looplength_input_name = r"single_B_average_looplength.csv"

output_name = r"single_B_volatility_w_looplength.csv"

vol_patient_name_col = 3  # column index of patient name, index starts at 0 (NOT 1)
looplen_patient_name_col = 2

# ==========================================================================================
vol_input_file = working_dir + volatility_input_name
looplen_input_file = working_dir + looplength_input_name
output_file = working_dir +output_name

vol_input_list = list()
looplen_input_list = list()
output_list = list()


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


patient_seq_dict = dict()  # {pat1: [row1, row2, ...]}


def main():
    global vol_input_list, looplen_input_list

    read_csv(vol_input_file, vol_input_list)
    read_csv(looplen_input_file, looplen_input_list)

    output_list.append(looplen_input_list[0] + vol_input_list[0])

    for vol_row in vol_input_list[1:]:
        current_vol_pat = vol_row[vol_patient_name_col]
        for lop_row in looplen_input_list[1:]:
            if current_vol_pat == lop_row[looplen_patient_name_col]:
                output_list.append(lop_row + vol_row)

    write_csv(output_list, output_file)


main()


