"""
Created on Aug 27 2021

@author: Changze Han
"""
import csv
import numpy as np
import random
import copy
import math
import itertools

# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/8.27.21_AA_grouping/"
sequence_name = r"test_input.csv"
reference_name = r"Reference_Numbering.csv"
output_folder = working_dir + r"outputs/"  # this is the folder within the working_dir, all txt outputs will be saved here

remove_dom_AA = True  # remove dominant amino acid for each position

accession_col_index = 1
pos_start_col_index = 10 # positions start at this col
# ========================================================================================================
sequence_file = working_dir + sequence_name
reference_file = working_dir + reference_name

sequence_list = list()
reference_list = list()

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


def write_txt(x,y): # write the list x into y file
    output= open(y,"w+")
    for i in x:
        output.write(i)
    output.close


reference_dict = dict()  # {pos: AA, ...}
def main():
    global sequence_list, reference_list, reference_dict

    read_csv(sequence_file, sequence_list)
    read_csv(reference_file, reference_list)

    print(f"sequence file len: {len(sequence_list)}")
    print(f"reference file len: {len(reference_list)}")

    # build a dict for reference data
    for i in reference_list[1:]:  # remove first row
        if i[0] not in reference_dict:
            reference_dict[i[0]] = i[1]

    print(f"how many pos in reference: {len(reference_dict)}")

    current_pos_dic = dict()  # {AA: [accession list], AA: [accession list], ....}
    current_pos_index = copy.deepcopy(pos_start_col_index)

    while current_pos_index < len(sequence_list[0]):  # go through each position, build dict
        current_pos = sequence_list[0][current_pos_index]  # position name
        for row in sequence_list[1:]:  # exclude header row, go through each accession row
            if row[current_pos_index] not in current_pos_dic:  # if this AA is not in dict
                current_pos_dic[row[current_pos_index]] = [row[accession_col_index]]  # add this AA and also add corresponding accession number
            else:
                current_pos_dic[row[current_pos_index]].append(row[accession_col_index])  # append another accession

        if remove_dom_AA == True:  # remove dominant AA key and its values
            dom_AA = reference_dict[current_pos]
            del current_pos_dic[dom_AA]  # remove this AA

        # write output file
        #print(f"====={current_pos}")
        #print(current_pos_dic)
        output_list = list()
        for aa_k in current_pos_dic:
            output_list.append(f"{current_pos}_{aa_k}:\n")  # add AA
            for v in current_pos_dic[aa_k]:
                output_list.append(f"{v}\n")  # add accession number
            output_list.append("\n")  # add extra empty line
        write_txt(output_list, f"{output_folder}output_{current_pos}.txt")


        current_pos_index += 1  # go to next position
        current_pos_dic = dict()  # reset the dict for next pos



main()


