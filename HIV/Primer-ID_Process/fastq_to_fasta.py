"""
Created on Jul 21 2020

@author: Changze Han
"""

'''
    For HIV Primer-ID project: 
        1. fastq files are downloaded from NCBI website "https://www.ncbi.nlm.nih.gov/bioproject/?term=PRJNA356756" 
           Download process requires the usage of tool "sratoolkit" from NCBI
        2. this script converts fastq format file into fasta in order to read them in MEGA software
            
           each entry in fastq file consists of 4 lines: 
                (https://support.illumina.com/bulletins/2016/04/fastq-files-explained.html)
                1. sequence identifier with infor about the sequencing run and the cluster. 
                2. the sequence (the base calls; A,C,T,G,and N)
                3. separator ("+")
                4. the base call quality scores. 
           only 1. and 2. will be written into fasta file

'''

# ==========================================================================================
working_dir = r"/Users/Han/Downloads/PRJNA356756-SRX2421069(PrimerID)-3runs/"
input_filename = r"SRR5105435.fastq"
output_filename = r"SRR5105435(fasta).fasta"

identifier_spliter = " "  # information in the identifier row are usually separated by spliters
identifier_start_symbol = "@"  # the leading symbol in the identifier row

fasta_identifier_only_accession = False  # True: only accession number will be extracted to the fasta output
# ==========================================================================================
input_file = working_dir + input_filename
output_file = working_dir + output_filename

input_list = []
output_list = []


def read_fastq(x, y):  # read a fastq file x and store into a list y
    file = open(x,"r")
    for line in file:
        y.append(line)


def write(x, y):  # write the list x into y file
    output = open(y,"w+")
    for i in x:
        output.write(i)
    output.close


def main():
    global input_list
    global output_list
    read_fastq(input_file, input_list)

    # each entry has 4 rows
    # index 0: identifier (write to fasta)
    # index 1: sequence (write to fasta)
    # index 2: separator (ignore)
    # index 3: quality score (ignore)

    identifier_index = 0
    while identifier_index < len(input_list):
        if fasta_identifier_only_accession:  # extract the accession only in the identifier row
            output_list.append(input_list[identifier_index]
                               .split(identifier_spliter)[0]
                               .replace(identifier_start_symbol, ">", 1))  # add ">" for fasta format
        else:  # extract all information in the identifier row
            output_list.append(input_list[identifier_index]
                               .replace(identifier_spliter, "|")  # change current splitter to fasta splitter
                               .replace(identifier_start_symbol, ">", 1))  # add ">" for fasta format
        output_list.append(input_list[identifier_index+1])

        identifier_index += 4

    print(f"input files contains {len(input_list)/4} entries.")
    print(f"    Beginning and ending entry: ")
    print(f"{input_list[:4]}\n{input_list[-4:]}")

    print(f"\noutput files contains {len(output_list)/2} entries.")
    print(f"    Beginning and ending entry: ")
    print(f"{output_list[:2]}\n{output_list[-2:]}")

    write(output_list, output_file)

    # check the output file
    print("\n ... Check output file ...")
    check_i = 0
    while check_i < len(output_list):
        if (check_i % 2) == 0:
            if output_list[check_i][0] != '>':
                print(f"Supposed to be '>' on index {check_i} : {output_list[check_i]}")
        else:
            if output_list[check_i][0] == '>':
                print(f"Not supposed to be '>' on index {check_i} : {output_list[check_i]}")
        check_i += 1


main()










