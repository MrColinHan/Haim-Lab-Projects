"""
Created on Feb 25 2020

@author: Han
"""

'''
    For HIV Project(long): 
    Use this program to analyze the output of "identify_FD_domAA.py"
    Manual Step: 
        The input file is not the actual output of "identify_FD_domAA.py.
        Need to separate the 'Patient-Days' identifier into two columns 'Patient' 'Days'. 
        Then do two level sort in excel. Sort 'Patient' first then 'Days'
                | Patient | Days |   332   |
                |  name1  |   0  |   M-1   | 
                
        Then transpose paste: 
                | Patient | name1|  name1  | name1 |
                |   Days  |   0  | 	2153   |  4103 | 
                |   332	  |  M-1 |	 M-1   |  M-1  |
                |   333	  |  R-0 | 	R-0	   |  R-0  |
            
                
    Algorithm: 
        For each column, identify the count of AAs that are 'emerge' or 'no-emerge'
        Rules: 
            no-emerge for 'Z':
                | Patient | Days |   332   |
                |    1    |   0  |   Z-1   | 
                |    1    |  10  |   Z-1   |
                  
            emerge for 'Z':
                | Patient | Days |   332   |
                |    1    |   0  |   Z-1   | 
                |    1    |  10  |   Z-0   |
            
            If starts at 0 then ignore this patient. ('Z-0' means starts at volatile): 
                | Patient | Days |   332   |
                |    1    |   0  |   Z-0   | 
                |    1    |  10  |   Z-1   |
            
            emerge for 'Z', not for 'Q':
                | Patient | Days |   332   |
                |    1    |   0  |   Z-1   | 
                |    1    |  10  |   Q-1   |
            
    Output Notation: 
        "Z/1"  =  Emerge
        "Z/0"  =  NO-Emerge 


'''
import csv
import operator

# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/2.21.20_b_single&long_dominantAA/B_ALL_Long/"
input_name = "(transpose)input for emerge.csv"
output_name = r"domAA_emerge_analysis_result.csv"

pos_row_starts_at = 2  # positions start at this row (index starts from 0, NOT 1)
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

    pat_col_dict = {}  # {name1:[1,3], name2:[4,8], ... } key is patient name, value is starting and ending col index
                       # name1:[1,3]  means patient name1 starts from col index 1 to col index 3
    for col in range(len(input_file_list[0][1:])):  # [1:]excludes first cell 'Patient', then go through index of all pat names
        # check if each patient is already in the dict
        if input_file_list[0][col+1] not in pat_col_dict:
            pat_col_dict[input_file_list[0][col + 1]] = [col+1]
            # input_file_list[0] is first row, [col + 1] is the index of this patient name
            # [col + 1]: col plus 1 because the first index was excluded, so now need to add 1 back
        else:  # this patient is already in the dict
            if len(pat_col_dict[input_file_list[0][col + 1]]) == 1:  # if this patient only has starting index
                pat_col_dict[input_file_list[0][col + 1]].append(col+1)  # then append the second index(may or may not be the ending index)
            else:  # this patient has two index, now update the second index because that one was not the ending index
                pat_col_dict[input_file_list[0][col + 1]][1] = col+1
    print(pat_col_dict)

    for row in input_file_list[2:]:  # iterate rows, [2:]exclude two header rows 'Patient' & 'Days'
        emerge_aa_count_dict = {}  # dict for this row, {'Z/1':5, 'Z/0':1, 'T/0':9, ...} count each emerge or no-emerge
        for key in pat_col_dict: # go through patients' cols
            cur_pat_start_index = pat_col_dict[key][0]  # pat_col_dict[key][0] is starting col index of this patient
            cur_pat_end_index = pat_col_dict[key][1]  # ending col index of this patient
            has_emerge = False  # when emerge found, change this to True in the while loop
            if row[cur_pat_start_index][2] == '1':  # make sure this patient starts at non-volatile
                                                       # row[] locates the 'aa-1', [2] locates the '1' part
                while cur_pat_start_index <= cur_pat_end_index:
                    if row[cur_pat_start_index] != row[pat_col_dict[key][0]]:  # pat_col_dict[key][0] locates the original start cell 'aa-1'
                        if f"{row[cur_pat_start_index][0]}/1" not in emerge_aa_count_dict:  # 'aa/1' means emerge
                            # row[cur_pat_start_index][0] locates the aa part of 'aa-1'
                            emerge_aa_count_dict[f"{row[cur_pat_start_index][0]}/1"] = 1
                        else:
                            emerge_aa_count_dict[f"{row[cur_pat_start_index][0]}/1"] += 1
                        has_emerge = True
                        break  # no need to check to rest
                    else:
                        cur_pat_start_index += 1
                if not has_emerge:  # no emerge found during the while loop
                    if f"{row[pat_col_dict[key][0]][0]}/0" not in emerge_aa_count_dict:  # 'aa/0' means no-emerge
                        emerge_aa_count_dict[f"{row[pat_col_dict[key][0]][0]}/0"] = 1
                    else:
                        emerge_aa_count_dict[f"{row[pat_col_dict[key][0]][0]}/0"] += 1
        print(f"{row[0]}: {emerge_aa_count_dict}")

        output_file_list.append([row[0]] + list(emerge_aa_count_dict.keys()))
        output_file_list.append([f"{row[0]} count"] + list(emerge_aa_count_dict.values()))


    print(f"{len(input_file_list[0])-1} samples in the input file")
    print(f"Positions from {input_file_list[pos_row_starts_at][0]} to {input_file_list[-1][0]}")
    write_csv(output_file_list, output_file)


main()



