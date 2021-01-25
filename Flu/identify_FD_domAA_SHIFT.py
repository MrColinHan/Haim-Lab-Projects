"""
Created on Fri Jan 22 2021

@author: Changze Han
"""

'''
    For Flu or HIV project:
    
    Input is the output from identify_FD_domAA.py. 
    
    This program go through all positions, and display columns that have AA shift. 
'''

import csv
# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/1.12.21_flu_tree/fd&std_output/each_group_FD&stdev(afterFuse)/"
input_filename = r"rearanged_dominant_AA.csv"
output_filename = r"AA_shifts.csv"

position_range = (1, 550)
# ==========================================================================================
input_file = working_dir + input_filename
output_file = working_dir + output_filename

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
    global input_list, output_list

    read_csv(input_file, input_list)

    output_col_index_list = list()

    header_row = input_list[0]
    data_rows = input_list[1:]
    for pos in range(position_range[0], position_range[1]+1):
        pos_index = header_row.index(str(pos))
        current_pos_AA_list = list()
        for group_row in data_rows:
            if len(current_pos_AA_list) == 0:
                current_pos_AA_list.append(group_row[pos_index][0])  # add the first group's AA
            else:
                if group_row[pos_index][0] not in current_pos_AA_list:
                    print(pos)
                    output_col_index_list.append(pos_index)
                    break
                else:
                    current_pos_AA_list.append(group_row[pos_index][0])

    # formating output
    for row in input_list:
        current_output_row = list()
        current_output_row.append(row[0])
        current_output_row.append(row[1])
        for p in output_col_index_list:
            current_output_row.append(row[p])
        output_list.append(current_output_row)



    write_csv(output_list, output_file)





main()


