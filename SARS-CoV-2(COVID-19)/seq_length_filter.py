"""
@author: Changze Han

10.1.2020
"""

from re import compile
import csv

"""
    This script extract sequences that meet the length requirement. 

    Input: fasta
    Output: fasta

"""

# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/9.18.20_sars_cov2_sequences/NCBI/"
in_fas_name = "B.SARS-CoV-2_Seq_4768.fas"
out_name = "C.SARS-CoV-2_Seq_Selected_.fas"

length_threshold = 13000
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


def main():
    global input_list, output_list

    readFasta(input_file, input_list)

    for i in range(1, len(input_list), 2):  # start from index1, and take step 2 because only need to check seq len
        print(len(input_list[i].replace('-', '')))
        if len(input_list[i].replace('-', '')) >= length_threshold:
            output_list.append(input_list[i-1])
            output_list.append(input_list[i])

    write(output_list, output_file)

    print(f"input file sample #: {len(input_list) / 2}")

    print(f"\nlength threshold: {length_threshold}"
          f"\nsample # after selection: {len(output_list)/2}")


main()

