"""
Created on Sep 22 2020

@author: Changze Han
"""

"""
    For Project COVID-19:
        Input: output from 'format_csvRow_to_list.py'
               then manually add '[]' to identify groups 
               
               e.g. input : each inner list is a group 
            [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 210.0, 0.0, 0.0], [140.0, 190.0, 1180.0, 1350.0, 140.0], [630.0, 270.0, 160.0, 840.0], [2220.0, 940.0, 295.0, 240.0], [1060.0, 380.0, 440.0, 1680.0], [720.0, 2000.0, 895.0, 2420.0], [1510.0, 990.0, 940.0, 600.0], [1140.0, 700.0, 1365.0, 2000.0], [1940.0, 910.0, 650.0, 1480.0], [980.0, 780.0, 1590.0, 1090.0], [640.0, 3010.0, 3045.0, 3700.0, 1800]]
        
        This program takes a list of groups(lists) to perform permutation t-test to provide statistic for the Precision results.
        
"""

import csv
from scipy import stats
import itertools
from statistics import mean
from scipy.stats import sem

# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/11.4.20_quartile_precision/11.16new data/"
input_list = [[0.0, 0.0, 0.0], [0.0, 5.0, 129.0, 285.0], [81.0, 152.0, 80.0, 160.0], [791.0, 35.0, 320.0, 0.0], [1439.0, 719.0, 1271.0, 150.0], [413.0, 640.0, 224.0, 320.0], [200.0, 160.0, 518.0, 260.0]]


title = r"roche-bsl3"
output_name = r"t test output.csv"


# cbEli(LUC): [[0.0, 0.0, 0.0], [190.0, 210.0, 160.0, 140.0], [140.0, 2000.0, 1350.0, 240.0], [895.0, 1180.0, 720.0, 2220.0], [840.0, 440.0, 270.0, 295.0, 780.0], [1940.0, 990.0, 980.0, 1480.0, 940.0], [1140.0, 650.0, 2420.0, 3010.0, 1365.0], [910.0, 380.0, 640.0, 600.0], [940.0, 1590.0, 1060.0, 1680.0], [1510.0, 700.0, 2000.0, 630.0], [1090.0, 1800.0, 3045.0, 3700.0]]
# Euroi(LUC): [[0.0, 0.0, 0.0, 210.0, 140.0], [140.0, 240.0, 190.0, 630.0], [940.0, 2220.0, 1350.0, 2420.0], [720.0, 895.0, 940.0, 1180.0], [1680.0, 840.0, 2000.0, 295.0], [160.0, 440.0, 270.0, 1060.0, 380.0], [600.0, 990.0, 1940.0, 910.0], [980.0, 1590.0, 650.0, 2000.0], [700.0, 1140.0, 1510.0, 3010.0], [1090.0, 1480.0, 780.0, 1800.0], [3700.0, 640.0, 3045.0, 1365.0]]
# Roche(LUC):  [[0.0, 0.0, 0.0], [2000.0, 650.0, 190.0, 140.0], [210.0, 140.0, 780.0, 940.0], [600.0, 1180.0, 1365.0, 2420.0], [240.0, 1680.0, 895.0, 1350.0, 720.0], [1090.0, 840.0, 1590.0, 1140.0, 295.0], [700.0, 1800.0, 380.0, 1940.0, 160.0], [3700.0, 3010.0, 3045.0, 270.0], [440.0, 990.0, 910.0, 940.0], [980.0, 1060.0, 1510.0, 630.0], [1480.0, 2220.0, 640.0, 2000.0]]
# Dia(LUC):  [[0.0, 0.0, 210.0, 0.0, 140.0, 190.0], [1180.0, 1350.0, 140.0, 630.0], [270.0, 160.0, 840.0, 2220.0], [940.0, 295.0, 240.0, 1060.0], [380.0, 440.0, 1680.0, 720.0], [2000.0, 895.0, 2420.0, 1510.0], [990.0, 940.0, 600.0, 1140.0], [700.0, 1365.0, 2000.0, 1940.0], [910.0, 650.0, 1480.0, 780.0], [980.0, 1590.0, 1090.0, 640.0], [3010.0, 3045.0, 3700.0, 1800.0]]


# cbEli(BSL): [[0.0, 0.0, 0.0], [0.0, 5.0, 0.0, 81.0], [129.0, 80.0, 160.0, 150.0], [320.0, 413.0, 200.0, 160.0], [285.0, 719.0, 35.0, 518.0], [640.0, 152.0, 224.0, 260.0], [320.0, 791.0, 1271.0, 1439.0]]
# Eurio(BSL): [[0.0, 0.0, 0.0, 5.0], [81.0, 0.0, 320.0, 160.0], [285.0, 80.0, 129.0, 152.0], [0.0, 150.0, 640.0], [35.0, 413.0, 320.0, 260.0], [160.0, 224.0, 719.0, 200.0], [791.0, 1439.0, 518.0, 1271.0]]
# Roche(BSL): [[0.0, 0.0, 0.0], [0.0, 5.0, 129.0, 285.0], [81.0, 152.0, 80.0, 160.0], [791.0, 35.0, 320.0, 0.0], [1439.0, 719.0, 1271.0, 150.0], [413.0, 640.0, 224.0, 320.0], [200.0, 160.0, 518.0, 260.0]]
# Dia(BSL):  [[0.0, 0.0, 5.0, 0.0, 0.0], [129.0, 320.0, 150.0, 0.0], [160.0, 81.0, 640.0, 35.0], [152.0, 80.0, 285.0], [224.0, 413.0, 160.0], [260.0, 320.0, 200.0, 518.0], [719.0, 1271.0, 1439.0, 791.0]]


# ==========================================================================================
output_file = working_dir + output_name

output_list = []  # store value for csv output


def write_csv(x, y):  # write list x into file y
    with open(y, 'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()


def twotail_t_test(l1, l2):  # l1 and l2 are two lists
    return stats.ttest_ind(l1, l2)


def main():
    global input_list, output_list, title

    # format first label row for output
    first_row = [f'Two-Tailed T test P value({title})']  # first cell will be empty or title because it is a matrix
    count = 0  # for first row's label purpose only
    for group in input_list:
        first_row.append(f"#{count}:{group}")
        count += 1
    output_list.append(first_row)  # add to output list

    matrix_row_i = 0  # keep track row index

    # now build up each row in the matrix
    while matrix_row_i < len(input_list):
        temp_new_row = [first_row[matrix_row_i + 1]]  # for each row, add label first (+1 because need to skip the first cell)

        # give enough empty space for each row because we only need half of the matrix to save computation time
        temp_new_row += [''] * (matrix_row_i + 1)
        if (matrix_row_i + 1) < len(input_list):  # corner test for the last row
            temp_compare_col_i = matrix_row_i + 1
            while temp_compare_col_i < len(input_list):
                list_one = input_list[matrix_row_i]
                list_two = input_list[temp_compare_col_i]
                temp_new_row.append(twotail_t_test(list_one, list_two)[1])
                temp_compare_col_i += 1

        output_list.append(temp_new_row)
        temp_new_row = []  # reset
        matrix_row_i += 1

    output_list.append([])
    output_list.append(["group", "mean", "std err"])
    g_count = 0
    for g in input_list:
        output_list.append([f"#{g_count}", mean(g), sem(g)])
        g_count += 1


    write_csv(output_list, output_file)


main()


