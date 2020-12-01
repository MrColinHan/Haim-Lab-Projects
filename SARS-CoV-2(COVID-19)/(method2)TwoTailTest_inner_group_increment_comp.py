"""
Created on Nov 5 2020

@author: Changze Han
"""

"""
    For Project COVID-19:
        Input: output from 'format_csvRow_to_list.py'
               then manually add '[]' to identify groups 

               e.g. input : each inner list is a group 
            [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 210.0, 0.0, 0.0], [140.0, 190.0, 1180.0, 1350.0, 140.0], [630.0, 270.0, 160.0, 840.0], [2220.0, 940.0, 295.0, 240.0], [1060.0, 380.0, 440.0, 1680.0], [720.0, 2000.0, 895.0, 2420.0], [1510.0, 990.0, 940.0, 600.0], [1140.0, 700.0, 1365.0, 2000.0], [1940.0, 910.0, 650.0, 1480.0], [980.0, 780.0, 1590.0, 1090.0], [640.0, 3010.0, 3045.0, 3700.0, 1800]]

        This program takes a list of groups(lists) to do a new way of comparision of t-test between groups. 

        e.g. 
            suppose we have 5 groups : 1 2 3 4 5   (1 is the least binding group, 4 is the most binding group)
            then perfrom t-test this way: 
                5+4+3+2  vs  5+4+3+2+1
                5+4+3  vs  5+4+3+2+1
                5+4  vs  5+4+3+2+1
                5  vs  5+4+3+2+1

            3 output value: t-test p value,  mean, standard error

"""

import csv
from scipy import stats
import itertools
import statistics
import scipy

# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/11.4.20_quartile_precision/11.16new data/"
input_list = [[0.0, 5.0, 0.0, 81.0], [129.0, 80.0, 160.0, 150.0], [320.0, 413.0, 200.0, 160.0], [285.0, 719.0, 35.0, 518.0], [640.0, 152.0, 224.0, 260.0], [320.0, 791.0, 1271.0, 1439.0]]

title = r"cbeli-bsl"
output_name = r"method2-precision_output.csv"

# cbEli(LUC): [[190.0, 210.0, 160.0, 140.0], [140.0, 2000.0, 1350.0, 240.0], [895.0, 1180.0, 720.0, 2220.0], [840.0, 440.0, 270.0, 295.0, 780.0], [1940.0, 990.0, 980.0, 1480.0, 940.0], [1140.0, 650.0, 2420.0, 3010.0, 1365.0], [910.0, 380.0, 640.0, 600.0], [940.0, 1590.0, 1060.0, 1680.0], [1510.0, 700.0, 2000.0, 630.0], [1090.0, 1800.0, 3045.0, 3700.0]]
# Euroi(LUC): [[140.0, 240.0, 190.0, 630.0], [940.0, 2220.0, 1350.0, 2420.0], [720.0, 895.0, 940.0, 1180.0], [1680.0, 840.0, 2000.0, 295.0], [160.0, 440.0, 270.0, 1060.0, 380.0], [600.0, 990.0, 1940.0, 910.0], [980.0, 1590.0, 650.0, 2000.0], [700.0, 1140.0, 1510.0, 3010.0], [1090.0, 1480.0, 780.0, 1800.0], [3700.0, 640.0, 3045.0, 1365.0]]
# Roche(LUC): [[2000.0, 650.0, 190.0, 140.0], [210.0, 140.0, 780.0, 940.0], [600.0, 1180.0, 1365.0, 2420.0], [240.0, 1680.0, 895.0, 1350.0, 720.0], [1090.0, 840.0, 1590.0, 1140.0, 295.0], [700.0, 1800.0, 380.0, 1940.0, 160.0], [3700.0, 3010.0, 3045.0, 270.0], [440.0, 990.0, 910.0, 940.0], [980.0, 1060.0, 1510.0, 630.0], [1480.0, 2220.0, 640.0, 2000.0]]
# Dia(LUC):  [[1180.0, 1350.0, 140.0, 630.0], [270.0, 160.0, 840.0, 2220.0], [940.0, 295.0, 240.0, 1060.0], [380.0, 440.0, 1680.0, 720.0], [2000.0, 895.0, 2420.0, 1510.0], [990.0, 940.0, 600.0, 1140.0], [700.0, 1365.0, 2000.0, 1940.0], [910.0, 650.0, 1480.0, 780.0], [980.0, 1590.0, 1090.0, 640.0], [3010.0, 3045.0, 3700.0, 1800.0]]


# cbEli(BSL):  [[0.0, 5.0, 0.0, 81.0], [129.0, 80.0, 160.0, 150.0], [320.0, 413.0, 200.0, 160.0], [285.0, 719.0, 35.0, 518.0], [640.0, 152.0, 224.0, 260.0], [320.0, 791.0, 1271.0, 1439.0]]
# Eurio(BSL): [[81.0, 0.0, 320.0, 160.0], [285.0, 80.0, 129.0, 152.0], [0.0, 150.0, 640.0], [35.0, 413.0, 320.0, 260.0], [160.0, 224.0, 719.0, 200.0], [791.0, 1439.0, 518.0, 1271.0]]
# Roche(BSL): [[0.0, 5.0, 129.0, 285.0], [81.0, 152.0, 80.0, 160.0], [791.0, 35.0, 320.0, 0.0], [1439.0, 719.0, 1271.0, 150.0], [413.0, 640.0, 224.0, 320.0], [200.0, 160.0, 518.0, 260.0]]
# Dia(BSL):  [[129.0, 320.0, 150.0, 0.0], [160.0, 81.0, 640.0, 35.0], [152.0, 80.0, 285.0], [224.0, 413.0, 160.0], [260.0, 320.0, 200.0, 518.0], [719.0, 1271.0, 1439.0, 791.0]]


# ==========================================================================================
output_file = working_dir + output_name

group_num_list_dict = {}  # {#0:[], #1:[], #2:[]}

output_list = []  # store value for csv output


def write_csv(x, y):  # write list x into file y
    with open(y, 'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()


def twotail_t_test(l1, l2):  # l1 and l2 are two lists
    return stats.ttest_ind(l1, l2)


def main():
    global input_list, output_list, title, group_num_list_dict

    # format output info, print out the groups first
    group_num = 1  # keep track of the group label. start from 1
    output_list.append([title])
    for g in input_list:  # for each group
        output_list.append([f"#{group_num}", g])
        group_num_list_dict[group_num] = g
        group_num += 1

    for i in group_num_list_dict:
        print(f"{i}: {group_num_list_dict[i]}")

    output_list.append([])
    output_list.append(["Two Tail T-test: "])

    current_group_num = list(group_num_list_dict.keys())[-1]
    first_group_num = list(group_num_list_dict.keys())[0]

    compare_group_set_1_dict = dict()
    while current_group_num > first_group_num:
        current_output_row = list()

        print(f"\ncurrent group num: {current_group_num}: ")

        # add current group to the compare group set
        compare_group_set_1_dict[current_group_num] = group_num_list_dict[current_group_num]

        # remove current group from the original dict
        #del group_num_list_dict[current_group_num]

        set_1_list = list(compare_group_set_1_dict.values())
        set_1_list = [ele for inner in set_1_list for ele in inner]

        set_2_list = list(group_num_list_dict.values())
        set_2_list = [ele for inner in set_2_list for ele in inner]

        print(f"set 1: {list(compare_group_set_1_dict.keys())}: {set_1_list}")
        print(f"set 2: {list(group_num_list_dict.keys())}: {set_2_list}")
        p_value = twotail_t_test(set_1_list, set_2_list)[1]
        print(f"two tail t test p value: {p_value}")

        current_output_row.append(list(compare_group_set_1_dict.keys()))
        current_output_row.append("VS")
        current_output_row.append(list(group_num_list_dict.keys()))
        current_output_row.append(p_value)

        output_list.append(current_output_row)
        current_group_num -= 1

    write_csv(output_list, output_file)


main()


