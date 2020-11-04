"""
Created on Oct 19 2020

@author: Changze Han
"""

"""
    For Project COVID-19 Sars CoV 2 sequence:
        This program trim a Sam format sequence file down to a specific range
        then convert the output to fasta format. 
        
        Input: 
            1. Sam file
            2. two sequence segments to set the range of sequence to keep: 
                example: 
                    start_seg = "ATGTTGTTATTAAAG"  # everything before the start seg will be deleted
                    end_seg = "TTACATTACACATAA"  # everything after the end seg will be deleted 
                    
        Output: 
            1. fasta file: for output
            2. fasta file: for left out list
"""

from simplesam import Reader
from re import compile

# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/10.19.20_sars-2_spike&N/"
sam_input_name = "B. SAM aligment SARS CoV 2.sam"
fas_output_name = "C_allGeno_nucleotide_aligned_SARS2.fasta"

start_seg = "ATGTCTGATAA"
end_seg = "TCAGGCCTAA"
# ========================================================================================================
sam_input_file = working_dir + sam_input_name
fas_output_file = working_dir + fas_output_name

sam_input_list = []
preprocess_list = []  # before output list
output_list = []
leftout_list = []  # for reads that dont have either start_seg or end_seg


def write(x, y):  # write the list x into y file
    output = open(y, "w+")
    for i in x:
        output.write(i)
    output.close


def main():
    global sam_input_list, preprocess_list, output_list, leftout_list

    file = open(sam_input_file, "r")  # open sam file
    in_sam = Reader(file)  # convert to a Reader object

    for read in in_sam:
        preprocess_list.append([read.qname, read.seq])

    print(f"Input sam file contains {len(preprocess_list)} reads\n")

    print("Leftout reads(dont have either start_seg or end_seg):")
    for i in preprocess_list:
        if (start_seg not in i[1]) or (end_seg not in i[1]):
            print(i)
            leftout_list.append(f">{i[0]}\n")
            leftout_list.append(f"{i[1]}\n")
        else:
            # now define the range of the seg we need to extract
            output_list.append(f">{i[0]}\n")
            start_index = i[1].find(start_seg)
            end_index = i[1].find(end_seg) + len(end_seg)
            output_list.append(f"{i[1][start_index:end_index]}\n")


    print(f"total {len(leftout_list)/2} leftout reads")
    print(f"total {len(output_list)/2} output reads")

    write(output_list, fas_output_file)
    write(leftout_list, working_dir + "leftout_noSpike.fasta")




main()

