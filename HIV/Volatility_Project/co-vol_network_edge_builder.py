"""
Created on Tue Jun 2 2020

@author: Changze Han
"""

import csv
import math

'''
    For HIV co-vol: 
    Prepare input for this program: convert the co-vol matrix into position pairs "Pos1 | Pos2 | co-vol"
                                    co-vol value need to be '-log(x)+1'
    
    This program filter out necessary position pairs which will be used as edges in network visualization.
    args: 
        1. center_position: is the main position that will be in the center of the network
        2. first_level_threshold: is the co-vol value cutoff, any position that has a co-vol with center_position
                                  >= than the cutoff will be written into output
        3. second_level_threshold: for each position we got after the first threshold, apply the 2nd threshold on
                                   these positions(meaning they become the new center_position) to find more edges
'''

# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/3.13.20_co-vol_network/"
input_filename = r"(log)B_single_nonBin_co-vol(180patients).csv"
output_filename = r"332_OUTPUT_two_level_thresh.csv"

input_has_header = True
center_position = 332
first_level_threshold = 3.3  # -log(0.05)+1
second_level_threshold = 5.3  # -log(0.00005)+1
# ==========================================================================================

input_file = working_dir + input_filename
output_file = working_dir + output_filename

input_list = []
output_list = []
node_list = []  # store unique positions for network nodes


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


# input_l is the input list, c_p is the center position, thre is the co-vol threshold
def apply_covol_thresh(input_l, c_p, thre):
    result_list = []
    for row in input_l:
        if int(row[0]) == c_p:
            if float(row[2]) >= thre:  # apply the threshold
                result_list.append(row)
        if int(row[1]) == c_p:
            if float(row[2]) >= thre:  # apply the threshold
                result_list.append([row[1], row[0], row[2]])  # reorder, put the c_p at the front
    return result_list


def main():
    global input_list
    global output_list
    global node_list

    read_csv(input_file, input_list)

    # clean the input:
    clean_input_list = []
    if input_has_header:  # check if the input file has a header row
        clean_input_list = input_list[1:].copy()  # remove the header row
    else:
        clean_input_list = input_list.copy()

    # now apply the first level thrshold for the center position
    first_level_out = apply_covol_thresh(clean_input_list, center_position, first_level_threshold)
    output_list += first_level_out

    print(f"input has {len(input_list)} rows, meaning {(1+math.sqrt(1+8*(len(input_list)-1)))/2} positions")

    print(f"first level output has {len(first_level_out)} edges")

    # now apply the second level threshold for each positions in the first_level_out:

    # build node list along the way
    node_list.append([str(center_position)])
    for row in first_level_out:
        if [row[1]] not in node_list:
            node_list.append([row[1]])
    for row in first_level_out:  # row[1] will be new center positions
        second_level_out = apply_covol_thresh(clean_input_list, int(row[1]), second_level_threshold)
        # now remove possible duplicates in the second_level_out before append to the final output
        for new_row in second_level_out:
            if [new_row[1]] not in node_list:
                node_list.append([new_row[1]])
            if [new_row[1], new_row[0], new_row[2]] not in output_list:
                output_list.append(new_row)
        print(f"after {row[1]}, final out length : {len(output_list)}")

    print(f"output has {len(output_list)} rows : {output_list[:2]} ... {output_list[-2:]}")
    write_csv(output_list, output_file)

    write_csv(node_list, f"{working_dir}node_list.csv")
    print(f"node list: {len(node_list)} nodes")


main()


