"""
Created on Feb 10 2020

@author: Changze Han
"""
import csv
import numpy as np
import random
'''
    For HIV Volatility project: 
    Analysis different kinds of significance(P value)
    Current analysis functions : 
                1. Variance 
    algorithms: 
        1. (optional) convert input data to binary ( 0 --> 0, non-0 --> 1)
        2. calculate an original average variance for each position: 
            2.a. calculate variance for each patient in each position
            2.b. 
'''
# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/2.8.10_variance_volatility/"
in_csv_name = "b_part_test.csv"
out_csv_name = "test_out.csv"

target_pos_tuple = (126, 126)  # (126, 130) means 126,127,...,130
shuffle_t = 1  # shuffle times
patient_col = 3  # patient identifiers is at this col (starts at index 0)
aa_at = 5  # Amino Acids start at this col (starts at index 0)
# ========================================================================================================
input_file = working_dir + in_csv_name
output_file = working_dir + out_csv_name

input_file_list = []  # store input file to list
total_sample_rows = 0  # will be auto-generated in main(), number of rows in input file, exclude header row
short_input_file_list = []  # store shorted input list, only include target positions
target_pos_list = []  # convert the tuple to a list

pat_aa_dict = {}  # dict for patients and their aa lists.
                  # Key is patient name
                  # Value is a list of lists(incase one patient name has multiple days, e.g. longitudinal, one sample is one inner list)
                  # e.g. {pat1:[[day1],[day5],[day8]], pat2:[...]...}
pat_name_list = []  # will be auto-generated from the dict in main()

pat_var_dict = {}  # dict for patients and their target positions' calculated variance
                   # Key is patient name
                   # Value is a list of lists(one shuffle time is one inner list)
                   # e.g. {pat1:[[shuffle1],[shuffle2],[shuffle3]...], pat2:[[shuffle1],...], ...}
original_pat_var_dict = {}  # store the original variances before shuffle

output_file_list = []  # store output data to list


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


def narrow_down_input(l):  # narrow down the aa part of the input list by only taking the target positions
    global target_pos_tuple
    global target_pos_list  # convert the pos tuple to a list along the way

    temp_result_list = []
    start_index = input_file_list[0].index((str(target_pos_tuple[0])))
    end_index = input_file_list[0].index(str(target_pos_tuple[1]))

    for row in l:  # format new shorted input list
        temp_result_list.append(row[:aa_at] + row[start_index:end_index+1])  # all properties + selected positions

    # build the target_pos_list
    for pos in temp_result_list[0][aa_at:]:
        target_pos_list.append(int(pos))
    if len(target_pos_list) == 0:  # check the output list, make sure it's nto empty
        raise ValueError("Error in convert_pos_tuple(): target position list is empty.")
    return temp_result_list


def build_pat_aa_dict(l):  # l is input list
    global pat_aa_dict
    global total_sample_rows
    for row in l[1:]:  # check pat name in the dict, exclude first header row
        if row[patient_col] not in pat_aa_dict:  # not found
            pat_aa_dict[row[patient_col]] = []  # add this pat, assign empty list as value
            pat_aa_dict[row[patient_col]].append(row[aa_at:])  # add this row's AA list, starts from col aa_at
        else:  # found
            pat_aa_dict[row[patient_col]].append(row[aa_at:])  # add aa list
    local_count = 0
    for pat in pat_aa_dict:  # count each patient's sample number
        local_count += len(pat_aa_dict[pat])
    if local_count != total_sample_rows:  # compare with input file's sample number
        raise ValueError("ERROR in build_pat_aa_dict(): total value count != total sample rows")


def cal_variance(p_list):  # p_list is a position list, e.g. target_pos_list
    global pat_aa_dict  # use this dict to calculate variance
    global pat_var_dict  # store the results in this dict



def main():
    global pat_aa_dict
    global pat_name_list
    global total_sample_rows
    global short_input_file_list

    read_csv(input_file, input_file_list)  # read input file
    total_sample_rows = len(input_file_list)-1  # input file's sample number, exclude header row

    short_input_file_list = narrow_down_input(input_file_list)  # narrow down the input list by only taking thar target positions
    if len(short_input_file_list)-1 != total_sample_rows:  # check new list's total sample number
        raise ValueError("Error in Shorted input list: total sample number doesn't match with the original.")
    write_csv(short_input_file_list, working_dir+"target_pos_input.csv")  # for debugging

    build_pat_aa_dict(short_input_file_list)  # first time construct the dict
    pat_name_list = list(pat_aa_dict.keys())  # put keys in the patients' name list

    # use random.sample(l, len(l)) to shuffle


    cal_variance(target_pos_list)

    # print all related info:
    print(f"input file :{total_sample_rows} rows data, {len(pat_name_list)} patients")
    print(f"target position list : {target_pos_list}")


main()



