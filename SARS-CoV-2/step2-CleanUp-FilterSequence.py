"""
@author: Changze Han
"""


from re import compile
import csv

"""
    This program filter the extracted SARS-Cov-2 nucleotide sequences after step1. 
    
    Output the sequences with nucleotide segment "GAATGACAAAA"
    
    Input: fasta
    Output: fasta

"""

# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/4.26.20_sars_cov-2/complete_record/"
in_fas_name = "complete_record(extracted_1524).fasta"
out_name = "complete_record(extracted_filtered_).fasta"

nucleo_segment = "GAATGACAAAA"
# ==========================================================================================
input_file = working_dir + in_fas_name
input_list = []  # save input sequences
output_file = working_dir + out_name
output_list = []  # save output sequences


def readFasta(x, y):  # read a fasta file x and store into a list y
    file = open(x, "r")
    for line in file:
        y.append(line)


def write(x, y):  # write the list x into y file
    output = open(y, "w+")
    for i in x:
        output.write(i)
    output.close


# l is the input list or the remaining of input list. This program extract the first set of sequence.
def find_next_sequence_set(l):
    result = []
    if l[0][0] == '>':
        result.append(l[0])
        for row in l[1:]:
            if row[0].isalpha() and row[0].isupper():
                result.append(row)
            else:  # row[0] is '>'
                break  # break before next set of sequence
    else:  # first row is not accession number
        raise Exception  # stop the program
    return result  # return the sequence block

def main():
    global input_list
    global output_list

    readFasta(input_file, input_list)

    test_list = []  # check whether test_list == input_list
    test_count = 0
    count_after_filter = 0  # keep track of how many are selected after filter

    current_index = 0  # index of current row
    current_sequence = []
    while current_index < len(input_list):
        print(current_index)
        current_sequence = find_next_sequence_set(input_list[current_index:])  # update current sequence
        test_list += current_sequence  # check
        test_count += 1  # check

        current_seq_string = ""  # store the sequence of current sequence in order to test nucleo_seg
        for row in current_sequence[1:]:  # exclude accession number row
            for nucl in row:
                if nucl.isalpha() and nucl.isupper():
                    current_seq_string += nucl

        if nucleo_segment in current_seq_string:
            output_list += current_sequence
            count_after_filter += 1

        current_index += len(current_sequence)

    print(f"\ncheck: 'test_list == input_list' : {test_list == input_list}")
    print(f"check: test_count: {test_count}")
    print(f"\nAfter filter '{nucleo_segment}' : {count_after_filter} are written into output")

    write(output_list, output_file)


main()




