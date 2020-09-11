"""
Created on Sep 11 2020

@author: Changze Han
"""

"""
    For Project COVID-19:
        Same input format as precision calculating program. 
    
        This program Performs permutation t-test to provide statistic for the Precision results. 
        
        step: 
            1. Data cleaning and arranging process same as precision script. 
                Predictor row and actual row are sorted based on predictor. 
            2. If predictor value < its neg cutoff, then put in one group. Then replace those value with 
                corresponding value in actual row. 
            3. for the rest of the actual row, go from back to front in the list, every 4 value put in one group. 
            4. Now we have all groups. Do permutation two-tailed t test on them and produce a matrix output. 
"""


import csv
from scipy import stats
import itertools

# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/9.6.20_covid_dyna_confusionMatrix/dyna_up_to_90%/twoTail_T_test/"
input_name = "ttest_input.csv"
output_name = r"ttest_cbEli(<100000)--BSL(groupsize4).csv"
missing_value = "Null"

each_group_size = 4  # for general groups, put 4 value in each group.
pred_negative_cutoff = 100000  # < than cutoff will be put in one group based on predictor value

label_row_index = 0  # usually it is always the first row
pred_value_row_index = 4  # row number in csv file that contains true value (index start from 0)
true_value_row_index = 7

# ==========================================================================================

input_file = working_dir + input_name  # full directory for input file
output_file = working_dir + output_name

input_file_list = []  # store the input csv file
output_list = []  # store value for csv output

# variables for step 1 =====================
pred_values = []
true_values = []  # empty list to store true values read from input file
label_values = []  # this is usually the first row

pred_name = None  # save the name of this predictor (usually first cell of its row)
true_name = None

# variables for step 2 =====================
label_pred_true_dict = {}  # {label_1:(pred_1, true_1), label_2:(pred_2, true_2), ...... }

# variables for step 4 =====================
sorted_p_t_l_list = []  # sort the dict then save in list [(pred, true, label), ...]

# variables for step 5 =====================
all_groups = []  # save all group. each group will be a sub list in this list


def read_csv(filedir, listname):  # output [len(true_list), pvalue, FPR, FNR, TPR, TNR]
    file = open(filedir)
    reader = csv.reader(file)
    for row in reader:
        listname.append(row)


def write_csv(x,y):  # write list x into file y
    with open(y,'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()


def divide_list_chunks(l, n):  # l is list, n is size of each chunk
    for i in range(0, len(l), n):
        yield l[i:i+n]


def twotail_t_test(l1, l2):  # l1 and l2 are two lists
    return stats.ttest_ind(l1, l2)


def main():
    global pred_values, true_values, input_file_list, label_values, pred_name, true_name, \
        label_pred_true_dict, output_list, sorted_p_t_l_list, all_groups

    read_csv(input_file, input_file_list)

    # step 1 ========================= import data
    pred_values = input_file_list[pred_value_row_index]  # save the target row for predictor value
    true_values = input_file_list[true_value_row_index]  # save the target row for true value
    label_values = input_file_list[label_row_index]  # save the sample name row for dict keys

    # separate out first cell which contains name of the predictor and true_value
    pred_name = pred_values[0]
    pred_values = pred_values[1:]  # remove first cell
    true_name = true_values[0]
    true_values = true_values[1:]
    label_values = label_values[1:]  # also remove first useless cell for label row
    print(f"step1 -- import data:\n  {pred_name} : {pred_values}\n  {true_name} : {true_values}")

    # step 2 ========================= construct dict
    # construct one dict {label_1:(pred_1, true_1), label_2:(pred_2, true_2), ...... }
    if len(label_values) == len(pred_values) == len(true_values):  # make sure 3 rows have same length
        label_pred_true_dict = dict(zip(label_values, zip(pred_values, true_values)))
    else:
        raise Exception("len(label) != len(predictor) != len(true_value)")
    print(f"\nstep 2  -- construct dict:\n  label-(pred,true)_dict: {label_pred_true_dict}")

    # step 3 ========================= clean dict
    # remove keys contain "Null"
    temp_keys_for_del = []  # temp list for keys will be deleted
    for key in label_pred_true_dict:
        if (label_pred_true_dict[key][0] == missing_value) or (label_pred_true_dict[key][1] == missing_value):
            temp_keys_for_del.append(key)
    for temp_key in temp_keys_for_del:  # now delete those keys
        del label_pred_true_dict[temp_key]
    print(f"\nstep 3 -- clean dict:\n  no-Null_dict:{label_pred_true_dict}")

    # convert "float" or "int" to float
    for key in label_pred_true_dict:
        label_pred_true_dict[key] = (float(label_pred_true_dict[key][0]), float(label_pred_true_dict[key][1]))
    print(f"  float_dict:{label_pred_true_dict}\n")

    # step 4 ========================= sort dict based on Predictor

    # sort the 'label_pred_true_dict' into list of tuples [(pred, true, label), ...]
    print("step 4 -- sort dict based on predictor:")
    sorted_p_t_l_list = sorted([(p, t, l) for (l, (p, t)) in label_pred_true_dict.items()])
    print(f"  sortted_p-t-l_list:{sorted_p_t_l_list}")
    #for i in sorted_p_t_l_list:
       # print(i)

    # step 5 ========================= Grouping
    print("\nstep 5 -- Grouping:")

    # First, reverse the list because we wanted to group from end to front
    sorted_p_t_l_list = sorted_p_t_l_list[::-1]
    check_len_sorted_p_t_l_list = len(sorted_p_t_l_list)  # keep a record for later check

    # Secondly, group the cutoff_group
    temp_Neg_group = []  # temporarily save sub group
    for i in sorted_p_t_l_list:
        if i[0] < pred_negative_cutoff:
            temp_Neg_group.append(i)
    for rm in temp_Neg_group:  # remove temp group from original group
        sorted_p_t_l_list.remove(rm)
    print("  Predictor Neg cutoff group:")
    print(temp_Neg_group)

    # Thirdly, group the rest by each_group_size
    print("\n  rest groups: ")
    temp_rest_groups = list(divide_list_chunks(sorted_p_t_l_list, each_group_size))
    for i in temp_rest_groups:
        print(i)

    # finish group, put everything together
    all_groups = temp_rest_groups + [temp_Neg_group]
    print(f"\n  {len(all_groups)} groups total:")
    for subgroup in all_groups:
        print(subgroup)

    if len([val for sublist in all_groups for val in sublist]) != check_len_sorted_p_t_l_list:
        raise Exception("ERROR: after grouping, len != to original len")

    # now check whether the last group in the temp_rest_groups is only length 1, if yes then remove
    if len(temp_rest_groups[-1]) == 1:
        print(f"\n  last second group is removed because it is length 1: {temp_rest_groups[-1]}")
        all_groups.remove(temp_rest_groups[-1])
        print(f"\n  NOW, All groups: ")
        for subgroup in all_groups:
            print(subgroup)

    # step 6 ========================= Compute matrix for two tailed t test
    # for each tuple, use the middle value which is the actual value, dont use the predictor [(pred, true, label), ...]

    # Reverse all groups again, because we changed mind on how to struct matrix
    all_groups = all_groups[::-1]

    # build up first label row for output
    temp_first_row = [f'Two-Tailed T test P value({pred_name})']  # first cell will be empty or title because it is a matrix
    temp_count = 1  # for first row's label purpose only
    for each in all_groups:
        temp_first_row.append(f"{temp_count}:{[middle for (left, middle, right) in each]}")
        temp_count += 1
    output_list.append(temp_first_row)

    matrix_row_i = 0  # keep track row index

    # now build up each row in the matrix

    while matrix_row_i < len(all_groups):
        temp_new_row = [temp_first_row[matrix_row_i+1]]  # for each row, add label first

        # give enough empty space for each row because we only need half of the matrix to save computation time
        temp_new_row += ['']*(matrix_row_i+1)
        if (matrix_row_i + 1) < len(all_groups):  # corner test for the last row
            temp_compare_col_i = matrix_row_i + 1
            while temp_compare_col_i < len(all_groups):
                list_one = [act for (p, act, lab) in all_groups[matrix_row_i]]
                list_two = [act for (p, act, lab) in all_groups[temp_compare_col_i]]
                temp_new_row.append(twotail_t_test(list_one, list_two)[1])
                temp_compare_col_i += 1

        output_list.append(temp_new_row)
        temp_new_row = []  # reset
        matrix_row_i += 1



    write_csv(output_list, output_file)

main()