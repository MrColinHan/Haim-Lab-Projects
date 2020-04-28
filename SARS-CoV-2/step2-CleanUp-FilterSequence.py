"""
@author: Changze Han
"""


from re import compile
import csv

"""
    This program clean up the extracted SARS-Cov-2 nucleotide sequences after step1. 
    
    Standard sequence(numbering): MN908947, length 21291
    
    Remove : sequences that are too short (< 20000)
             sequences contain too many non-ACTG
    
    Input: fasta
    Output: fasta

"""

# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/4.26.20_sars_cov-2/"
in_fas_name = "complete_record(extracted_1524).fasta"
out_name = "complete_record(extracted_filtered_).fasta"

length_cutoff = 20000  # if the sequence length < 20000, then remove
non_ACTG_cutoff = 1  # if the sequence contain >1 non-ACTG, then remove
# ==========================================================================================
input_file = working_dir + in_fas_name
input_list = []  # save input sequences
output_file = working_dir + out_name
output_list = []  # save output sequences

nucleotide_seq = ('A', 'C', 'T', 'G', '-', ' ', '\n')


def readFasta(x, y):  # read a fasta file x and store into a list y
    file = open(x, "r")
    for line in file:
        y.append(line)


def write(x, y):  # write the list x into y file
    output = open(y, "w+")
    for i in x:
        output.write(i)
    output.close


def write_csv(x, y):  # write list x into file y
    with open(y, 'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()


# l is the input list or the remaining of input list. This program extract the first set of sequence.
def find_next_sequence_set(l):
    result = []
    for row_i in range(len()):
        if

    return result

def main():
    readFasta(input_file, input_list)

    current_index = 0  # index of current row
    current_sequence = []
    while current_index < len()
    for row in input_list:
        if row[0] == '>':
            return
        else:


    write(output_list, output_file)


main()




