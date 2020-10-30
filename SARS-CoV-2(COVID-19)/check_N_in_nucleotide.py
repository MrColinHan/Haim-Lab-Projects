"""
Created on Oct 29 2020

@author: Changze Han
"""

'''
    For Project COVID-19 Sars CoV 2 sequence:

    check different kinds of count of 'N' in nucleotide sequence. 
    
    then extract the sequence with no 'N' at all into a new fasta file
'''



# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/10.19.20_sars-2_spike&N/N_trees/"
fas_input_name = "(noIdentical)USA_N_nucleotide_aligned_SARS2_(530).fas"

output_name = "(noIdentical_noN)USA_N_nucleotide_aligned_SARS2_(497).fas"
# ========================================================================================================
fas_input_file = working_dir + fas_input_name
output_file = working_dir + output_name

input_list = []
output_list = []



def read_fasta(x,y): # read a fasta file x and store into a list y
    file = open(x,"r")
    for line in file:
        y.append(line)


def write(x, y):  # write the list x into y file
    output = open(y, "w+")
    for i in x:
        output.write(i)
    output.close


def main():
    global input_list, output_list

    read_fasta(fas_input_file, input_list)

    print(f"input sequence len: {len(input_list) / 2}\n")

    count_seq_no_N = 0
    count_seq_more_one_N = 0
    count_seq_more_ten_N = 0
    count_seq_ten_consecutive_N = 0

    for i in range(1, len(input_list), 2):  # seq index: 1, 3, 5...
        current_count_N = input_list[i].count('N')
        if current_count_N == 0:
            count_seq_no_N += 1
            output_list.append(input_list[i - 1])
            output_list.append(input_list[i])

        if current_count_N >= 1:
            count_seq_more_one_N += 1

        if current_count_N >= 10:
            count_seq_more_ten_N += 1

        current_count_ten_consecutive_N = input_list[i].count('NNNNNNNNNN')
        if current_count_ten_consecutive_N != 0:
            count_seq_ten_consecutive_N += 1

    print(f"# sequence with no N: {count_seq_no_N}\n")
    print(f"# sequence with more than one N: {count_seq_more_one_N}\n")
    print(f"# sequence with more than ten N(may be discontinuous): {count_seq_more_ten_N}\n")
    print(f"# sequence with ten consecutive N ('NNNNNNNNNN'): {count_seq_ten_consecutive_N}\n")

    write(output_list, output_file)
    print(f"output fasta contains {len(output_list)/2} sequences")


main()



