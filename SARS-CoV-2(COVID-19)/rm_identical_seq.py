"""
Created on Oct 28 2020

@author: Changze Han
"""

'''
    For Project COVID-19 Sars CoV 2 sequence:
    
    it's possible that there are identical sequences in fasta file. 
    this program remove duplicate sequences. 
'''


# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/10.19.20_sars-2_spike&N/N_trees/"
fas_input_name = "USA_N_nucleotide_aligned_SARS2_(8128).fas"

output_name = "(no-identical)USA_N_nucleotide_aligned_SARS2_(8128).fas"
# ========================================================================================================
fas_input_file = working_dir + fas_input_name
output_file = working_dir + output_name

input_list = []
unique_seq_list = []
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
    global input_list, output_list, unique_seq_list

    read_fasta(fas_input_file, input_list)

    print(f"input sequence len: {len(input_list)/2}\n")

    print(f"...remove identical sequence...")

    for i in range(1, len(input_list), 2):  # seq index: 1, 3, 5...
        if input_list[i] not in unique_seq_list:
            unique_seq_list.append(input_list[i])

            output_list.append(input_list[i-1])
            output_list.append(input_list[i])
    print(f"output seq len after removal: {len(output_list)/2}")

    write(output_list, output_file)

main()


