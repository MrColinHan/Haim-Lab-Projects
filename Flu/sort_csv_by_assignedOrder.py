"""
Created on Wed Jan 13 2021

@author: Changze Han
"""

'''
    For Flu Project: 

        Sort the data by a assigned order for a certain attribute column. 
        
        example:  Sample# | Group # | 135 | 158 | 225 | ...
                    ...
                    ...
        The data has its own way of sorted group #, but we want to re-arrange it according to our order of group #
        So give it a list of our group # order  [4,6,1,3,2]
        
        The program writes a new CSV file
'''

import csv

# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/1.12.21_flu_tree/fd&std_output/rearrange_group_number/"
input_file_name = r"(afterFuse)segment_3.csv"
output_file_name = r"rearanged_output.csv"

attribute_column = "Group_num"
new_order = [33, 15, 59, 9, 13, 50, 27, 17, 14, 11967, 11068, 30, 23, 5, 25, 0, 29, 8, 43, 42, 28, 51, 36, 12, 11, 4, 48, 26, 58, 44,
             2, 45, 57, 22, 38, 55, 19, 24, 20, 47, 3, 54, 1, 46, 32, 49, 53, 16, 40, 18, 7, 31, 34, 6, 52, 35, 10]

# H3N2 Tree_0.009 Segment 1 = [106, 33, 65, 15, 94, 96, 59, 60, 9, 13, 50, 67, 27, 63, 17, 14, 110, 68, 93, 80, 30, 23, 73, 62, 109, 69, 5, 108, 25, 0]
# H3N2 Tree_0.009 Segment 2 = [84, 29, 72, 8, 105, 101, 83, 92, 43, 42, 28, 61, 79, 51, 36, 12, 11, 4, 88, 48, 71, 26, 82, 58, 44, 2, 45, 57, 66, 22, 38, 81, 78, 55, 100, 91, 19, 24, 20, 87, 47, 104, 3, 103, 54, 99, 1]
# H3N2 Tree_0.009 Segment 3 = [46, 32, 49, 53, 77, 102, 98, 89, 16, 76, 40, 18, 7, 31, 34, 97, 6, 52, 86, 35, 107, 75, 10]

# after fusing groups
# [33, 15, 59, 9, 13, 50, 27, 17, 14, 11967, 11068, 30, 23, 5, 25, 0, 29, 8, 43, 42, 28, 51, 36, 12, 11, 4, 48, 26, 58, 44,
#             2, 45, 57, 22, 38, 55, 19, 24, 20, 47, 3, 54, 1, 46, 32, 49, 53, 16, 40, 18, 7, 31, 34, 6, 52, 35, 10]
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
    global attribute_column, new_order, input_file, output_file, input_list, output_list

    # first step, check if there are dup typo in the selected value list
    selected_values_set = set(new_order)
    if len(selected_values_set) != len(new_order):
        raise Exception("ERROR: There are duplicate values in the selected_value list !!!")

    read_csv(input_file, input_list)

    header_row = input_list[0]
    attribute_column_index = header_row.index(attribute_column)
    output_list.append(header_row)

    for v in new_order:
        for row in input_list[1:]:
            if int(row[attribute_column_index]) == v:
                output_list.append(row)

    write_csv(output_list, output_file)


main()

