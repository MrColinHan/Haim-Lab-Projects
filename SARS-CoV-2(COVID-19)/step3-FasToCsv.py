"""
@author: Changze Han
"""

from re import compile
import csv

"""
    This program convert fasta sequence(after step2) to CSV format
  
    Input: fasta
    Output: csv

"""

# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/4.26.20_sars_cov-2/complete_record/"
in_fas_name = "D.complete_record(extracted_filtered_cut&aligned_262).fas"
out_name = "E.complete_record(extracted_filtered_cut&aligned_262).csv"
# ==========================================================================================
input_file = working_dir + in_fas_name
input_list = []  # save input sequences
output_file = working_dir + out_name
output_list = []  # save output sequences


# possible accession format : "MT292582.1", "NM_001935.4", "NM_001379606.1"
ACCESSION_MATCHER = compile(r'[A-Za-z]{2}\d{6}\.\d{1}|[A-Za-z]{2}_\d{6}\.\d{1}|[A-Za-z]{2}_\d{9}\.\d{1}')


def readFasta(x, y):  # read a fasta file x and store into a list y
    file = open(x, "r")
    for line in file:
        y.append(line)


def write_csv(x, y):  # write list x into file y
    with open(y, 'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()


def getAccessNum(string):
    # extract accession from the given string, returns the first match if there are multiple matches
    return ACCESSION_MATCHER.findall(string)[0]


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

        # construct csv output
        current_csv_row = [getAccessNum(current_sequence[0])]  # store the current row of csv output
        for row in current_sequence[1:]:  # exclude accession number row
            for nucl in row:
                if nucl.isalpha() and nucl.isupper():
                    current_csv_row.append(nucl)

        output_list.append(current_csv_row)
        current_csv_row = []  # reset
        current_index += len(current_sequence)

    print(f"\ncheck: 'test_list == input_list' : {test_list == input_list}")
    print(f"check: test_count: {test_count}\n")

    print(f"CSV output : {len(output_list)} rows")
    write_csv(output_list, output_file)


main()




