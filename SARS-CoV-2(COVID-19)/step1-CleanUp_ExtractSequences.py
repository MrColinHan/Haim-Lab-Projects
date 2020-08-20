"""
@author: Changze Han
"""


from re import compile
import csv

"""
    This program clean up the raw SARS-Cov-2 nucleotide sequences downloaded from NCBI. 
    The raw sequences contain duplicate accession numbers. 
    Input: fasta
    Output: fasta, csv(unique accession list)

"""

# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/4.26.20_sars_cov-2/"
in_fas_name = "complete_record.fasta"#"SARS-CoV-2_(15279).fasta"
out_name = "complete_record(extracted).fasta"#"SARS-CoV-2_(extracted).fasta"
# ==========================================================================================
input_file = working_dir + in_fas_name
input_list = []  # save input sequences
output_file = working_dir + out_name
output_list = []  # save output sequences

accession_dict = {}  # save unique accession numbers as keys, value is [starting row index, ending row index]
write_accession_list = []  # special format to write a csv file for accession_list

# possible accession format : "MT292582.1", "NM_001935.4", "NM_001379606.1"
ACCESSION_MATCHER = compile(r'[A-Za-z]{2}\d{6}\.\d{1}|[A-Za-z]{2}_\d{6}\.\d{1}|[A-Za-z]{2}_\d{9}\.\d{1}')


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


def getAccessNum(string):
    # extract accession from the given string, returns the first match if there are multiple matches
    return ACCESSION_MATCHER.findall(string)[0]


def main():
    global input_list
    global output_list
    global accession_dict
    global write_accession_list
    readFasta(input_file, input_list)  # read input fasta

    # ======extract unique accession number list and starting&ending row index======
    total_seq_count = 0  # count sequences in the input file
    for row_i in range(len(input_list)):
        if input_list[row_i][0] == '>':
            total_seq_count += 1
            current_access = getAccessNum(input_list[row_i])
            if current_access not in accession_dict:
                accession_dict[current_access] = [row_i, '?']  # update the starting row index
                write_accession_list.append([current_access, input_list[row_i]])
                print(f"{current_access}: [{row_i}, ?]")
                # now update the ending row index
                count_end_row = 0
                for end_row in input_list[row_i+1:]:
                    if end_row[0].isalpha() and end_row[0].isupper():
                         count_end_row += 1
                    else:
                        break
                accession_dict[current_access][1] = row_i + count_end_row + 1  # add one more index
                print(f"    {current_access}: {accession_dict[current_access]}")

    # ======extract final output======
    output_rowcount_check = 0
    for key in accession_dict:
        c_r_i = accession_dict[key][0]  # c_r_i is current row index
        output_list.append(f">{getAccessNum(input_list[c_r_i])}\n")  # add accession number row
        c_r_i += 1
        output_rowcount_check += 1
        while c_r_i < accession_dict[key][1]:
            output_list.append(input_list[c_r_i])
            c_r_i += 1
            output_rowcount_check += 1
    if len(output_list) != output_rowcount_check:
        raise Exception

    print(f"\nInput fasta file '{in_fas_name}' contains : {total_seq_count} sequences")
    print(f"Extracted {len(accession_dict)} unique accession numbers.")
    write_csv(write_accession_list, working_dir+"unique_accession_list.csv")

    # write output list into file
    print(f"\nOutput fasta file '{out_name}' contains : {len(accession_dict)} sequences ({len(output_list)} rows)")
    write(output_list, output_file)


main()


# ============================= Check =============================================================
print(f"\n\n========== Check ============")
complete_record_file_name = "complete_record_summary(1336).txt"
complete_record_file = working_dir + complete_record_file_name

complete_record_list = []
complete_record_accession_list = []


def check_complete_record():
    readFasta(complete_record_file, complete_record_list)

    for row_i in range(len(complete_record_list)):
        # check missing accession numbers in current accession_list
        try:
            complete_record_accession_list.append(getAccessNum(complete_record_list[row_i]))
        except:
            continue
    print(f"complete record contains: {len(complete_record_accession_list)} accession numbers")
    print(f"Extracted list is missing : ")
    for item in complete_record_accession_list:
        if item not in accession_dict:
            print(item)
    for item_2 in accession_dict:
        if item_2 not in complete_record_accession_list:
            print(f"complete_record_accession_list is missing: {item_2}")


check_complete_record()



