"""
Created on Oct 28 2020

@author: Changze Han
"""

"""
    For Project COVID-19 Sars CoV 2 sequence:
        
        This program extract sequences from a fasta file based on a list of accession list

        Input: 
            1. accession number list saved in a column in a text file
            2. fasta sequence (output from the 'trim_sam_fasta.fasta')
               
        Output: 
            a new fasta file
"""
# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/10.19.20_sars-2_spike&N/N_trees/"
txt_input_name = "USA_accession(8128).txt"
fas_input_name = "(c)_N_nucleotide_aligned_SARS2_(13698).fas"

output_name = "USA_N_nucleotide_aligned_SARS2_(8128).fas"
# ========================================================================================================
txt_input_file = working_dir + txt_input_name
fas_input_file = working_dir + fas_input_name
output_file = working_dir + output_name

accession_list = []
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
    global input_list, output_list, accession_list

    read_fasta(fas_input_file, input_list)

    read_fasta(txt_input_file, accession_list)

    # strip each accession list
    for a in range(len(accession_list)):
        accession_list[a] = accession_list[a].strip()

    for i in range(0, len(input_list), 2):  # use step 2 to take only index 0, 2, 4...
        if input_list[i][1:].strip() in accession_list:  # [1:] removes '>', strip remove ending '\n'
            output_list.append(input_list[i])
            output_list.append(input_list[i+1])

    print(f"{len(input_list)/2} sequences in fas input: \n{input_list[0]}{input_list[1]}")
    print(f"{len(accession_list)} accession numbers in txt file:\n{accession_list[:5]}...\n")

    print(f"output file has {len(output_list)/2} sequences")

    write(output_list, output_file)

main()




