"""
Created on Wed Jan 13 2021

@author: Changze Han
"""

'''
    For Flu Project: 
        
        Extract rows from a csv file based on a list of selected value for a certain attribute column. 
        Designed for program "flu_fd_stdev_cal.py" input. 
        
        example: 
        
                Group_0.009  |  Season  |  Country  |  Accession  | 1 | 2 | 3 | 4 | 5 | ...
                    1           ...
                    1           ...
                    1           ...
                    2           ...
                    2           ...
                    3           ...
                    4           ...
                    4           ...
                    5           ...
                    
                Then I can choose "Group_0.009" attribute and give it a selected values [2,3], 
                and the result would be rows that have [2,3] as their "Group_0.009" values.
                
        Input: CSV file 
        Output: CSV file 

'''

import csv

# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/1.12.21_flu_tree/fd&std_output/"
input_file_name = r"human_10-19_season_H3N2_USA_AA_PNGS_7750(&attributes&groups).csv"
output_file_name = r"segment_1.csv"

attribute_column = "Group_num"
selected_values = [106, 33, 65, 15, 94, 96, 59, 60, 9, 13, 50, 67, 27, 63, 17, 14, 110, 68, 93, 80, 30, 23, 73, 62, 109, 69, 5, 108, 25, 0]
# H3N2 Tree_0.009 Segment 1 = [106, 33, 65, 15, 94, 96, 59, 60, 9, 13, 50, 67, 27, 63, 17, 14, 110, 68, 93, 80, 30, 23, 73, 62, 109, 69, 5, 108, 25, 0]
# H3N2 Tree_0.009 Segment 2 = [84, 29, 72, 8, 105, 101, 83, 92, 43, 42, 28, 61, 79, 51, 36, 12, 11, 4, 88, 48, 71, 26, 82, 58, 44, 2, 45, 57, 66, 22, 38, 81, 78, 55, 100, 91, 19, 24, 20, 87, 47, 104, 3, 103, 54, 99, 1]
# H3N2 Tree_0.009 Segment 3 = [46, 32, 49, 53, 77, 102, 98, 89, 16, 76, 40, 18, 7, 31, 34, 97, 6, 52, 86, 35, 107, 75, 10]

# =========================================================================================
input_file = working_dir + input_file_name
output_file = working_dir + output_file_name

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


def main():
    global attribute_column, selected_values, input_file, output_file, input_list, output_list

    # first step, check if there are dup typo in the selected value list
    selected_values_set = set(selected_values)
    if len(selected_values_set) != len(selected_values):
        raise Exception("ERROR: There are duplicate values in the selected_value list !!!")

    read_csv(input_file, input_list)

    header_row = input_list[0]
    attribute_column_index = header_row.index(attribute_column)
    output_list.append(header_row)

    for r in input_list[1:]:
        if int(r[attribute_column_index]) in selected_values:
            output_list.append(r)

    write_csv(output_list, output_file)


main()

