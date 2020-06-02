"""
Created on Feb 18 2020

@author: Changze Han
"""

'''
    After extract_position_pairs.py

    This script takes three or more col csv data as input 
    The first two cols are position pairs (pos1, pos2, p_value)
    Given a list of target positions, output all rows that both positions are in the given list.  
    Note: input needs a header row

'''

import csv

# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/2.18.20_domains-antibody&ppt/"
csv_name = "B_all_pairs.csv"
out_name = "2.27.20_target_pairs.csv"
target_positions = [97, 276, 278, 279, 280, 281, 282, 283, 365, 366, 367,
                    368, 371, 427, 428, 429, 430, 455, 456, 457, 458, 459,
                    460, 461, 462, 463, 464, 465, 469, 472, 473, 474, 476, 1276]
# ========================================================================================================

input_file = working_dir + csv_name
output_file = working_dir + out_name
input_list = []  # save input data to a list
output_list = []


def read_csv(filedir, listname):
    file = open(filedir)
    reader = csv.reader(file)
    for row in reader:
        listname.append(row)


def write_txt(x, y):  # write the list x into y txt file
    output = open(y, "w+")
    for i in x:
        output.write(str(i) + "\n")
    output.close


def write_csv(x, y):  # write list x into file y
    with open(y, 'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()


def main():
    global input_list
    global output_list

    read_csv(input_file, input_list)
    output_list.append(input_list[0])  # add the header row to the output list
    found_pair_count = 0  # keep track of count of found pairs
    for p in input_list[1:]:  # exclude header row, iterate all the pairs
        if (int(p[0]) in target_positions) and (int(p[1]) in target_positions):  # check first col and second col
            output_list.append(p)
            found_pair_count += 1

    print(f"{len(input_list)-1} pairs in the input file.\n")
    print(f"{found_pair_count} pairs are found containing target positions\n")
    print(f"check counts: should be {len(target_positions)}*{len(target_positions)-1}/2 = "
          f"{(len(target_positions)*(len(target_positions)-1))/2} ")
    print("(if not same, might because of some "
          f"target positions are not in the input file (e.g. glycan), then manually check)")
    write_csv(output_list, output_file)


main()
