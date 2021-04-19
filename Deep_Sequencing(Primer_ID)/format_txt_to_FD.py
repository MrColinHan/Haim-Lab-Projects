"""
Feb 26, 2021

@author: Changze Han
"""

'''
    For deep sequencing data: 
        read a txt file downloaded from xxxx website. format it into regular FD format
        
        start reading from line "Aminoacid Frequence input sample.txt"
        every '|' indicates one new position
        every ';' indicates one new AA


'''

import csv
import math

# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/4.16.21 grant FD & deep seq/deep_seq_fd/"
input_filename = r"3.29.21 SRR5105421 1HD1 D0 Fw.txt"
output_filename = "3.29.21 SRR5105421 1HD1 D0 Fw.csv"

read_line_number = 5  # start counting from 0
data_start_index = 24  # after getting the line number, narrow down to the starting index
                       # (because there are useless info before actual data e.g. "BAR_GRAPH	Consensus	PID")
# ========================================================================================================
input_file = working_dir + input_filename
output_file = working_dir + output_filename

input_list = list()
output_list = list()

aa_fd_dict = {
            'A': 0,
            'C': 0,
            'D': 0,
            'E': 0,
            'F': 0,
            'G': 0,
            'H': 0,
            'I': 0,
            'K': 0,
            'L': 0,
            'M': 0,
            'N': 0,
            'P': 0,
            'Q': 0,
            'R': 0,
            'S': 0,
            'T': 0,
            'V': 0,
            'W': 0,
            'Y': 0,
            'X': 0,
            '*': 0}

def read_txt(x, y):  # read a fastq file x and store into a list y
    file = open(x,"r")
    for line in file:
        y.append(line)



def write_csv(x, y):  # write list x into file y
    with open(y, 'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()


def main():
    global input_list, output_list

    read_txt(input_file, input_list)

    data_line = input_list[read_line_number]
    print(f"Reading this line into FD: \n{data_line}\n")

    data_line = data_line[24:]
    print(f"remove useless info: \n{data_line}\n")

    pos_line_dict = dict()  # split the data line based on position indicator '|' and save each pos to dict

    data_line_split = data_line.split('|')
    pos_count = 1  # initialize pos from 1
    for line in data_line_split:
        if (line != '') and (line != '\n'):
            split_line_by_AA = line.split(';')  # split by ';' in order to isolate each AA
            # the first position format is unique e.g.'8.631102,T,T 8.6311%', need special process:
            split_line_by_AA[0] = split_line_by_AA[0].split(',')[2]
            pos_line_dict[pos_count] = split_line_by_AA
            print(f"pos {pos_count}: \n     {split_line_by_AA}")
            print(len(split_line_by_AA))
            pos_count += 1  # go to next pos

    # for each position, construct its own AA-FD dict
    output_list.append(['Positions'] + list(aa_fd_dict.keys()))  # add header row
    for pos in pos_line_dict:
        new_aa_fd_dict = aa_fd_dict.fromkeys(aa_fd_dict, 0)  # reset dict
        for aa_fd in pos_line_dict[pos]:
            aa = aa_fd.split()[0]
            fd = aa_fd.split()[1].strip('%')
            if aa not in new_aa_fd_dict:  # report if there's a new AA
                raise Exception (f"UNKNOWN AA: {aa}")
            if (aa in new_aa_fd_dict) and (new_aa_fd_dict[aa] != 0):  # report if there's duplicate
                raise Exception(f"Duplicate FD for AA: {aa}")
            else:
                new_aa_fd_dict[aa] = fd  # assign fd to this aa
        #output_list.append([pos] + list(new_aa_fd_dict.keys()))  # use this line to check whether positions were shifted
        output_list.append([pos] + list(new_aa_fd_dict.values()))
    # at the end, flip the output format
    output_list = zip(*output_list)

    write_csv(output_list, output_file)









main()


