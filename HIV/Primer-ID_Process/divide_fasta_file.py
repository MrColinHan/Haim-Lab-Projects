"""
Created on Jul 21 2020

@author: Changze Han
"""

'''
    For HIV Primer-ID project: 
        fastq-converted fasta files are usually too big to open for MEGA software. 
        This script divide one giant fasta file into multiple smaller fasta file so 
        that we can visually read the sequence on MEGA. 
        
        note: there should be no empty line between each sequence
        
'''

# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/9.18.20_sars_cov2_sequences/NCBI/"#r"/Users/Han/Downloads/PRJNA356756-SRX2421069(PrimerID)-3runs/SRR5105435(Fasta Format)/"
input_filename = r"sars-cov-2_Nucleotide_ALL(16975).fasta"#r"SRR5105435(fasta)_ALL_(1,153,558).fasta"
output_file_prefix = r"sars-cov-2_Nucleotide_part" # r"SRR5105435(fasta)_part"  # numbers after '_part' will be consecutively generated
# complete output name format: e.g. SRR5105426(fasta)_part1_(#ofEntries).fasta

seq_amount_per_file = 1000000
# ==========================================================================================
input_file = working_dir + input_filename

input_list = []


def read_fasta(x, y):  # read a fastq file x and store into a list y
    file = open(x,"r")
    for line in file:
        y.append(line)

def write(x, y):  # write the list x into y file
    output = open(y,"w+")
    for i in x:
        output.write(i)
    output.close

def main():
    read_fasta(input_file, input_list)
    print(f"Input file contains {len(input_list) / 2} entries, {len(input_list)} rows")

    total_rows = len(input_list)
    each_file_rows = seq_amount_per_file * 2  # multiply 2 because each seq contains 2 rows
    print(f"\nEach partial file will contain {seq_amount_per_file} entries, {each_file_rows} rows")

    if total_rows < each_file_rows:
        raise Exception("ERROR: seq_amount_per_file exceeds file size!!!")

    target_out_amt = 0
    if (total_rows % each_file_rows) == 0:
        target_out_amt = total_rows // each_file_rows
        print(f"\n{target_out_amt} files will be written"
              f"(the last file contains {seq_amount_per_file} entries as well) ")
    else:
        target_out_amt = (total_rows // each_file_rows) + 1
        print(f"\n{target_out_amt} files will be written "
              f"(the last file contains less entries {total_rows % each_file_rows/2})")

    print("         ......writing......")

    current_out_file = 1  # number of partial file being written right now
    check_total_lens = 0  # add up each output's lens then check with the total lens at the endd
    while current_out_file <= target_out_amt:
        temp_out_list = []
        if current_out_file != target_out_amt:
            temp_out_list = input_list[((current_out_file-1)*each_file_rows):(current_out_file*each_file_rows)]

            print(f"current output: part{current_out_file}"
                  f", rows_index_range = [{(current_out_file-1)*each_file_rows} : {current_out_file*each_file_rows}]"
                  f", rows_length = {len(temp_out_list)}({len(temp_out_list)/2}entries)")
            check_total_lens += len(temp_out_list)

            write(temp_out_list, f"{working_dir}{output_file_prefix}{current_out_file}_({len(temp_out_list)/2}).fasta")
            current_out_file += 1
        else:
            temp_out_list = input_list[(current_out_file-1)*each_file_rows:]

            print(f"current output: part{current_out_file}"
                  f", rows_index_range = [{(current_out_file-1) * each_file_rows} : ]"
                  f", rows_length = {len(temp_out_list)}({len(temp_out_list)/2}entries)")
            check_total_lens += len(temp_out_list)

            write(temp_out_list, f"{working_dir}{output_file_prefix}{current_out_file}_({len(temp_out_list)/2}).fasta")
            current_out_file += 1

    # check total lens
    print(f"Check: total lens of all partial outputs = {check_total_lens}({check_total_lens/2}entries)")


main()