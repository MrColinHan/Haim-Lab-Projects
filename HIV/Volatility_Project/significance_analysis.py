"""
Created on Feb 10 2020

@author: Changze Han
"""
import csv
import numpy as np
import random
import copy
'''
    For HIV Volatility project: 
    Analysis different kinds of significance(P value)
    Current analysis functions : 
                1. Variance 
    algorithms: 
        1. (optional, do this step in Excel) convert input data to binary ( 0 --> 0, non-0 --> 1)
        2. calculate an original average variance for each position: 
            2.a. calculate variance for each patient in each position
            2.b. calculate all patients' average variance for each position 
        3. shuffle the patient name list 10,000 times:
            3.a. calculate the same average variance for each shuffle
        4. Compare the 10,000 avg variance with the original variance: 
            4.a. calculate how many times are smaller than the original avg var? 
'''
# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/2.8.10_variance_volatility/"
in_csv_name = "(bin)All_Bs_long_Volatility.csv"
# Final P value will be printed out in the console

target_pos_tuple = (281, 281)  # (126, 130) means 126,127,...,130, (126, 126) means one position 126
shuffle_t = 10000  # shuffle times
patient_col = 3  # patient identifiers is at this col (starts at index 0)
pos_start = 5  # position starts at this col (starts at index 0)
# ========================================================================================================
input_file = working_dir + in_csv_name

input_file_list = []  # store input file to list
total_sample_rows = 0  # will be auto-generated in main(), number of rows in input file, exclude header row
short_input_file_list = []  # store shorted input list, only include target positions and patient name property
# separate short_input_file_list into two parts:
pat_name_col = []  # only name col, generated from short_input_file_list
aa_cols = []  # only aa/volatility cols, generated from short_input_file_list


target_pos_list = []  # convert the tuple to a list

pat_aa_dict = {}  # dict for patients and their aa lists(volatility lists).
                  # Key is patient name
                  # Value is a list of lists(incase one patient name has multiple days, e.g. longitudinal, one sample is one inner list)
                  # e.g. {pat1:[[day1],[day5],[day8]], pat2:[...]...}
pat_name_list = []  # unique name list, will be auto-generated from the dict in main()

avg_var_lists = []  # list for all calculated avg variance lists
                    # each inner list is one shuffle, order of inner list numbers are target pos order
                    # e.g. [ [shuffle1 avg var list], [shuffle2 avg var list],...... ]
original_pat_var_list = []  # store the original variances before shuffle process, use this dict for final p value cal

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
    start_index = l[0].index((str(target_pos_tuple[0])))  # index of first pos in tuple
    end_index = l[0].index(str(target_pos_tuple[1]))  # index of second pos in tuple

    if end_index == (len(l[0])-1):  # check if the second position is the end of this row
        for row in l:  # in this case, use 'row[start_index:]'
            temp_result_list.append([row[patient_col]] + list(map(float, row[start_index:])))  # patient_name + selected positions
    else:  # second pos is not the end
        for row in l:  # in this case, use 'row[start_index:end_index + 1]'
            temp_result_list.append([row[patient_col]] + list(map(float, row[start_index:end_index + 1])))  # patient_name + selected positions

    # build the target_pos_list
    for pos in temp_result_list[0][1:]:  # [0]first header row, [0][1:] all target positions, iterate through them
        target_pos_list.append(int(pos))
    if len(target_pos_list) == 0:  # check the output list, make sure it's not empty
        raise ValueError("Error in narrow_down_input(): target position list is empty.")

    return temp_result_list


def build_pat_aa_dict(l):  # l is shorted input list
    global pat_aa_dict
    global total_sample_rows
    pat_aa_dict = {}  # empty the dict
    for row in l[1:]:  # check pat name in the dict, exclude first header row
        if row[0] not in pat_aa_dict:  # not found, index 0 is the patient name
            pat_aa_dict[row[0]] = []  # add this pat, assign empty list as value
            pat_aa_dict[row[0]].append(row[1:])  # add this row's AA list, starts from index 1
        else:  # found
            pat_aa_dict[row[0]].append(row[1:])  # add aa list
    # checking part:
    local_pat_count = 0
    for pat in pat_aa_dict:  # count each patient's sample number
        local_pat_count += len(pat_aa_dict[pat])
    if local_pat_count != total_sample_rows:  # compare with input file's sample number
        raise ValueError("ERROR in build_pat_aa_dict(): total value count != total sample rows")


def cal_avg_variance():  # variance calculation based on 'pat_aa_dict', avg var results will be added to 'avg_var_lists'
    global pat_aa_dict
    global avg_var_lists  # store the results in this dict
    global pat_name_list  # not sure if this is useful in this function so far
    global target_pos_list  # for print use, debug

    current_shuffle_avg_var_lists = []  # local variable
    for pat in pat_aa_dict:  # go through each patient key
        current_pat_samples_zip = list(zip(*pat_aa_dict[pat]))  # local variable
        # print(f"{pat} === {current_pat_samples_zip}")
        for pos in range(len(current_pat_samples_zip)):  # go through each position's list
            # print(f"{target_pos_list[pos]}: {current_pat_samples_zip[pos]}")
            current_pat_samples_zip[pos] = np.var(current_pat_samples_zip[pos])  # replace this list with its variance
            # print(f"{target_pos_list[pos]}:{current_pat_samples_zip[pos]}")
        # print(f"{pat} === {current_pat_samples_zip}")
        # print("=========================================")
        current_shuffle_avg_var_lists.append(current_pat_samples_zip)
    # print(f"current shuffle avg var: {current_shuffle_avg_var_lists}")
    current_shuffle_avg_var_lists = list(zip(*current_shuffle_avg_var_lists))  # zip in order to calculate vertical average
    # print(f"current shuffle avg var(zip): {current_shuffle_avg_var_lists}")
    for col in range(len(current_shuffle_avg_var_lists)):  # go through each column tuple
        # replace this col list with its average
        current_shuffle_avg_var_lists[col] = (sum(current_shuffle_avg_var_lists[col])/len(current_shuffle_avg_var_lists[col]))
    print(f"current shuffle average variance: {current_shuffle_avg_var_lists}")

    avg_var_lists.append(current_shuffle_avg_var_lists)  # add current shuffle's avg var to all shuffle lists




def main():
    global input_file_list
    global pat_aa_dict
    global avg_var_lists
    global pat_name_list
    global total_sample_rows
    global short_input_file_list
    global target_pos_list
    global original_pat_var_list
    global shuffle_t
    global pat_name_col
    global aa_cols

    read_csv(input_file, input_file_list)  # read input file
    total_sample_rows = len(input_file_list)-1  # input file's sample number, exclude header row

    short_input_file_list = narrow_down_input(input_file_list)  # narrow down the input list by only taking thar target positions
    if len(short_input_file_list)-1 != total_sample_rows:  # check new list's total sample number
        raise ValueError("Error in Shorted input list: total sample number doesn't match with the original.")
    # separate short_input_file_list into two parts:
    pat_name_col = [[item[0]] for item in short_input_file_list[1:]]  # generate entire pat name list, for shuffling purpose
    aa_cols = [item[1:] for item in short_input_file_list[1:]]
    write_csv(short_input_file_list, working_dir+"original_shorted_input.csv")  # write a temp file for debugging
    write_csv(pat_name_col+aa_cols, working_dir+"original_shorted_input_two_parts.csv")

    build_pat_aa_dict(short_input_file_list)  # first time construct the dict, use shorted input
    pat_name_list = list(pat_aa_dict.keys())  # record the original order of the patient list

    # first time calculating the variance which is the original data's variance:
    cal_avg_variance()  # avg variance calculation based on pat_aa_dict
    original_pat_var_list = copy.deepcopy(avg_var_lists[0])  # deepcopy the original avg variance data for p value cal
    write_csv([original_pat_var_list], working_dir+"original_avg_var.csv")

    avg_var_lists = []  # empty avg var lists before shuffling process
    # start shuffling process: shuffle the short_input_file_list
    while shuffle_t != 0:
        print("=========================================")
        print(f"shuffle count down --- {shuffle_t}: ")
        new_pat_name_col = random.sample(pat_name_col, len(pat_name_col))
        new_aa_cols = copy.deepcopy(aa_cols)  # deepcopy original aa_cols in order to keep aa_cols never change
        for row in range(len(new_aa_cols)):  # re-combine shuffled name list and aa_cols
            new_aa_cols[row] = new_pat_name_col[row] + new_aa_cols[row]
        new_aa_cols.insert(0, [])  # insert a fake empty header row
        # now 'new_aa_cols' is the new 'short_input_file_list'

        # uncomment this line if want to see each shuffle's input
        # write_csv(new_aa_cols, working_dir + f"shuffle{shuffle_t}_input.csv")

        build_pat_aa_dict(new_aa_cols)
        cal_avg_variance()

        shuffle_t -= 1
    write_csv(avg_var_lists, working_dir + "shuffled_avg_var_lists.csv")

    # now compare 'original_pat_var_list' with 'avg_var_lists'
    final_p_value_list = []
    for p in range(len(original_pat_var_list)):
        current_p_count = 0  # count how many avg var is less than original avg var
        for shuffle in avg_var_lists:
            if shuffle[p] < original_pat_var_list[p]:
                current_p_count += 1
        final_p_value_list.append(current_p_count/len(avg_var_lists))  # counts divided by shuffle times

    # print all related info:
    print("=========================================")
    print(f"input file :{total_sample_rows} rows data")
    print(f"{len(pat_name_list)} patients : {pat_name_list}")
    print(f"target position list : {target_pos_list}")
    print(f"Original avg var: {original_pat_var_list}")
    print(f"Shuffle times: {len(avg_var_lists)}")
    print(f"P value(counts/{len(avg_var_lists)}): {final_p_value_list}")


main()



