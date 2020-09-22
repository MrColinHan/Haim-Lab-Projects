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

# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/9.6.20_covid_dyna_confusionMatrix/(NEW)dyna_up_to_90%/"
input_list = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [190.0, 210.0, 160.0, 140.0, 140.0], [1350.0, 240.0, 1180.0, 720.0], [2220.0, 840.0, 440.0, 270.0], [295.0, 1940.0, 990.0, 1480.0], [940.0, 1140.0, 650.0, 2420.0], [3010.0, 910.0, 380.0, 640.0], [940.0, 1060.0, 1680.0, 1510.0], [700.0, 2000.0, 630.0, 1800.0, 3700]]

#Euroi: [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 210.0], [0.0, 140.0, 140.0, 240.0, 190.0], [630.0, 940.0, 2220.0, 1350.0], [2420.0, 720.0, 895.0, 940.0], [1180.0, 1680.0, 840.0, 2000.0], [295.0, 160.0, 440.0, 270.0], [1060.0, 380.0, 600.0, 990.0], [1940.0, 910.0, 980.0, 1590.0], [650.0, 2000.0, 700.0, 1140.0], [1510.0, 3010.0, 1090.0, 1480.0], [780.0, 1800.0, 3700.0, 640.0, 3045.0, 1365]]

#Roche: [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [2000.0, 650.0, 190.0, 140.0, 210.0], [140.0, 780.0, 940.0, 600.0], [1180.0, 1365.0, 2420.0, 240.0], [1680.0, 895.0, 1350.0, 720.0], [1090.0, 840.0, 1590.0, 1140.0], [295.0, 700.0, 1800.0, 380.0], [1940.0, 160.0, 3700.0, 3010.0], [3045.0, 270.0, 440.0, 990.0], [910.0, 940.0, 980.0, 1060.0], [1510.0, 630.0, 1480.0, 2220.0, 640.0, 2000]]

#Dia: [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 210.0, 0.0, 0.0], [140.0, 190.0, 1180.0, 1350.0, 140.0], [630.0, 270.0, 160.0, 840.0], [2220.0, 940.0, 295.0, 240.0], [1060.0, 380.0, 440.0, 1680.0], [720.0, 2000.0, 895.0, 2420.0], [1510.0, 990.0, 940.0, 600.0], [1140.0, 700.0, 1365.0, 2000.0], [1940.0, 910.0, 650.0, 1480.0], [980.0, 780.0, 1590.0, 1090.0], [640.0, 3010.0, 3045.0, 3700.0, 1800]]

title = r"cbEli"
output_name = r"output.csv"
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
    count = 1  # for first row's label purpose only
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

    write_csv(output_list, output_file)


main()


