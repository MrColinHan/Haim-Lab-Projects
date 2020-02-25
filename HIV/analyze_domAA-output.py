"""
Created on Feb 21 2020

@author: Han
"""

'''
    For HIV Project: 
    Use this program to analyze the output of "identify_domAA_single_samp.py"
    Manual Step: 
        The input file is not the actual output of "identify_domAA_single_samp.py.
        Need to transpose paste the value part to ease the calculation in this script. 
    
    Results: 
        Count the AA-# in each column. (AA-# e.g. 'Z-1', 'T-0' ... )
        
        
    
'''
import csv
import operator

# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/2.21.20_b_single_dominantAA/B_ALL/"
input_name = "(transpose)B_all_single_dominant_AA.csv"
output_name = r"domAA_analysis_result.csv"

# ==========================================================================================
input_file = working_dir + input_name
output_file = working_dir + output_name
input_file_list = []
output_file_list = []



def read_csv(filedir, listname):
    file = open(filedir)
    reader = csv.reader(file)
    for row in reader:
        listname.append(row)


def write_csv(x, y):  # write list x into file y
    with open(y, 'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()


def main():
    global input_file_list
    global output_file_list

    read_csv(input_file, input_file_list)
    patient_number = len(input_file_list[0]) - 1  # count how many patients should be in one row
    for row in input_file_list:  # iterate rows(one row is one position)
        cur_dict = {}  # dict to save the count of each AA  ({'Z-1':15, 'T-0':3, 'P-0':6, ...})
        for AA in row[1:]:  # iterate this row's AA, exclude first index because it's a position
            if AA not in cur_dict:  # add this AA to dict
                cur_dict[AA] = 1
            else:  # found, then count + 1
                cur_dict[AA] = cur_dict[AA] + 1
        # check each row's dict's total count
        if sum(list(cur_dict.values())) != patient_number:
            raise ValueError(f"Total patient count is wrong at position {row[0]} row")
        # sort the dict based on value then,
        # flat the current dict to 2 lists and add to output. Also add the position number to the front

        sorted_cur_dict = dict(sorted(cur_dict.items(), key=operator.itemgetter(1), reverse=True))

        output_file_list.append([row[0]] + list(sorted_cur_dict.keys()))
        output_file_list.append([f"{row[0]} count"] + list(sorted_cur_dict.values()))

        #output_file_list.append([row[0]]+[[k, v] for k, v in cur_dict.items()])

    print(f"input contains {len(input_file_list)} positions")
    print(f"{patient_number} patients total")
    write_csv(output_file_list, output_file)


main()



