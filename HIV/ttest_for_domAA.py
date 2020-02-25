"""
Created on Feb 24 2020

@author: Han
"""

'''
    For HIV Project: 
    Use this program to analyze the output of "analyze_domAA-output.py"
    
    Perform two tailed test on each position's top two AA. (two AAs which have the most and second most count)
    stats.ttest_ind gives a tuple output with two values inside: 
                    statistic : The calculated t-statistic
                    pvalue : The two-tailed p-value
    Modify line ??? to change the output value (statistic is [0], pvalue is [1])
    
    Input: 
        1. format has to be : 
                        |    1	  |   M-1  |  M-0  |
                        | 1 count |	  204  |   1   | 
                        |    2	  |   ...  |  ...  |
                        | 2 count |	  ...  |  ...  | 
                        ......
'''

import csv
from scipy import stats
import itertools

# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/2.21.20_b_single_dominantAA/B_ALL/"
input_name = "domAA_analysis_result.csv"
output_name = "ttest_results.csv"

# ==========================================================================================
input_file = working_dir + input_name
output_file = working_dir + output_name
input_file_list = []
output_file_list = []


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


# n is number, t is repeat times. e.g. (1,5) is [1,1,1,1,1]     (0,3) is [0,0,0]
def make_repeat_list(n, t):
    return list(itertools.repeat(n, t))


def twotail_test(l1, l2):  # l1 and l2 are two lists
    return stats.ttest_ind(l1, l2)


def main():
    global input_file_list
    global output_file_list

    read_csv(input_file, input_file_list)

    for row_i in range(len(input_file_list)):  # go through each row index
        if row_i % 2 == 0:  # index 0,2,4,6... are the position rows, 1,3,5,7... are the count rows

            top_aa_dict = {}  # record the index of top and second most counted aa and their index
            second_aa_dict = {}  # dict format: {'R': [3,6]} means 'R' appears in index 3 and 6
                                 # {'R': [3]} means only 'R' only appear once in index 3

            list_top = []  # save output of 'make_repeat_list(n,t)' for t test
            list_second = []

            for aa in input_file_list[row_i][1:]:  # go through this position row's aa, exclude first index
                if len(top_aa_dict) == 0:  # haven't found the top aa yet
                    if (aa != 'None') and (aa != ''):  # skip 'None' and empty cells
                        # aa format is 'R-1', so aa[0] is the aa letter
                        # 'input_file_list[row_i].index(aa)' is the index of aa
                        top_aa_dict[aa[0]] = [input_file_list[row_i].index(aa)]
                else:  # already found at least one half of top aa, now need to look for the other half of top aa or second aa
                       # 'R-0' is the other half of 'R-1'
                    if (aa != 'None') and (aa != ''):
                        if aa[0] in top_aa_dict:  # if this is the other half of top aa
                            top_aa_dict[aa[0]].append(input_file_list[row_i].index(aa))  # add new index
                        else:  # if not, then check if second dict is empty
                            if len(second_aa_dict) == 0:
                                second_aa_dict[aa[0]] = [input_file_list[row_i].index(aa)]
                            else:  # already found at least one half of second aa
                                if aa[0] in second_aa_dict:
                                    second_aa_dict[aa[0]].append(input_file_list[row_i].index(aa))
                                # there's no other situation after here
            # now construct the two lists for t test using two dicts
            print(input_file_list[row_i][0])
            print(top_aa_dict)
            print(second_aa_dict)
            if (len(top_aa_dict) == 0) or (len(second_aa_dict) == 0):  # if no top or second aa found, then no need for t test
                output_file_list.append([input_file_list[row_i][0]] + ["insufficient data"])
                output_file_list.append([f"{input_file_list[row_i][0]} P_Value"] + ["insufficient data"])
            else:
                for top_k in top_aa_dict:  # actually no need to use 'for' because only one key in dict
                    for top_v in top_aa_dict[top_k]:  # go through value list
                    # 'input_file_list[row_i][top_v][2]' is the '1' in 'R-1'
                    # 'input_file_list[row_i + 1][top_v]' is the corresponding count of 'R-1'
                        list_top = list_top + make_repeat_list(int(input_file_list[row_i][top_v][2])
                                                               , int(input_file_list[row_i + 1][top_v]))
                        print(f"{int(input_file_list[row_i][top_v][2])} : {int(input_file_list[row_i + 1][top_v])}")

                for sec_k in second_aa_dict:
                    for sec_v in second_aa_dict[sec_k]:
                        list_second = list_second + make_repeat_list(int(input_file_list[row_i][sec_v][2])
                                                                     , int(input_file_list[row_i + 1][sec_v]))
                        print(f"{int(input_file_list[row_i][sec_v][2])} : {int(input_file_list[row_i + 1][sec_v])}")
                # format output for this position
                output_file_list.append([input_file_list[row_i][0]] + [f"{list(top_aa_dict.keys())[0]} vs {list(second_aa_dict.keys())[0]}"])
                output_file_list.append([f"{input_file_list[row_i][0]} P_Value"] + [twotail_test(list_top, list_second)[1]])






    print(f"{int(len(input_file_list)/2)} positions total")
    write_csv(output_file_list, output_file)


main()




