"""
Created on Jan 27 2021

@author: Changze Han
"""

'''
    For HIV Volatility project: 
    
        Input data: 
            CSV file
            AARegionCounts (loop length)
        
        process: 
            in the input data, each patient usually have multiple rows data. 
            this program calculate the average value at each position column for each patient
        
        output: 
            CSV file
'''

import csv
import numpy as np

# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/1.26.21_HIV_Volatility_single/"
input_name = r"single_c_average_input.csv"
output_name = r"single_C_average_looplength.csv"

patient_name_col = 2  # column index of patient name, index starts at 0 (NOT 1)
data_start_col = 3
# ==========================================================================================
input_file = working_dir + input_name
output_file = working_dir + output_name
input_list = list()
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
    global input_list, output_list, patient_name_col, data_start_col

    read_csv(input_file, input_list)

    header_row = input_list[0]
    output_list.append(header_row)
    data_rows = input_list[1:]
    for row in data_rows:
        if row[patient_name_col] not in patient_seq_dict:
            patient_seq_dict[row[patient_name_col]] = [row]
        else:
            patient_seq_dict[row[patient_name_col]].append(row)

    print(f"number of patients: {len(patient_seq_dict)}\n")

    for pat in patient_seq_dict:
        print(pat)
        current_pat_features = patient_seq_dict[pat][0][:data_start_col]
        current_pat_data_only_matrix = list()
        for row in patient_seq_dict[pat]:
            current_pat_data_only_matrix.append([int(i) for i in row[data_start_col:]])
        current_pat_output_row = current_pat_features + list(np.mean(current_pat_data_only_matrix, axis=0))
        print(f"{pat} --- average: {current_pat_output_row}")
        output_list.append(current_pat_output_row)

    write_csv(output_list, output_file)

main()


