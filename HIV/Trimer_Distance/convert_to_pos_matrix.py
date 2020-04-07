"""
Created on Jan 07 2020

@author: Changze Han
"""

import csv
from sympy import *
'''
    For HIV project - trimer distance step3: 
    convert the entire chain-pos matrix to regular pos matrix. 
    Input: pairs format of the chain-pos matrix. (by using the extract_position_pairs.py)
    Output: A matrix 
    
    Algorithm: 
    1. remove all chain letter prefix first 
       NOTE: need to make sure int always starts at string[1:]. Meaning only first digit is prefix letter. 
    2. make a new pair dict with no pair duplications by keeping the smallest value
    3. format a matrix
'''
# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/3.11.20_trimer_distance/"
in_csv_name = "(chain pairs)6mzj_all_coords(atom&hetam).csv"
out_csv_name = "(position matrix)6mzj_all_coords(atom&hetam).csv"

# output matrix format (NOTE: range(1,6) means [1,2,3,4,5], doesn't cover 6)
position_range = list(range(33, 663))# + list(range(512, 665))
# ========================================================================================================

input_csv_file = working_dir + in_csv_name
output_csv_file = working_dir + out_csv_name
input_csv_list = []
cleaned_input_list = []  # rm prefix
smallest_input_dict = {}  # rm dup by taking smallest value, {(pos1, pos2):distance, (pos1, pos3):distance, ...}
output_csv_list = []


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


# remove all chain letters prefix then return the same list
def rm_chain_letters(l):  # l is the input csv list
    result_list = []
    for i in l:
        temp_pair = [i[0][1:], i[1][1:], i[2]]
        #print(temp_pair)
        result_list.append(temp_pair)
    return result_list


def main():
    global cleaned_input_list
    global smallest_input_dict

    read_csv(input_csv_file, input_csv_list)  # read input csv file

    cleaned_input_list = rm_chain_letters(input_csv_list)  # rm chain letter prefix

    # remove dup by find the smallest
    first_larger_count = 0  # first position is larger. (This is what we need)
    second_larger_count = 0  # second is larger. reverse duplication
    equal_count = 0  # two positions equal to each other
    for pair in cleaned_input_list:
        if int(pair[0]) > int(pair[1]):  # first pos is larger. Only need half matrix, so need col > row
            first_larger_count += 1
            if (pair[0], pair[1]) not in smallest_input_dict:  # check if current dict contains this pair
                smallest_input_dict[(pair[0], pair[1])] = float(pair[2])  # add this new pair to dict
            else:
                if float(pair[2]) < smallest_input_dict[(pair[0], pair[1])]:  # if new distance is smaller
                    smallest_input_dict[(pair[0], pair[1])] = float(pair[2])
        if int(pair[0]) < int(pair[1]):  # second is larger, reverse and then compare distance
            second_larger_count += 1
            if (pair[1], pair[0]) not in smallest_input_dict:
                smallest_input_dict[(pair[1], pair[0])] = float(pair[2])  # add this new pair to dict
                #raise ValueError(f"Reverse position pair is missing from dictionary:"
                                 #f" original:{(pair[0], pair[1])}, reverse:{pair[1], pair[0]}")
            else:
                if float(pair[2]) < smallest_input_dict[(pair[1], pair[0])]:  # if new distance is smaller
                    smallest_input_dict[(pair[1], pair[0])] = float(pair[2])
        if int(pair[0]) == int(pair[1]):  # two positions equal
            equal_count += 1

    # construct output file format:
    copy_pos_range = position_range[:]  # use copy because insert could modify data in original position_range
    output_csv_list.append(copy_pos_range)  # first row
    output_csv_list[0].insert(0, '')  # add an empty space at the beginning
    for pos in position_range:
        output_csv_list.append([pos])

    # fill in the matrix:
    empty_need = 1
    no_available_pos = 0
    available_pos = 0
    for row in output_csv_list[1:]:
        row.extend('' for i in range(empty_need))
        for col in output_csv_list[0][empty_need+1:]:
            print(f"{col} VS {row[0]}")
            if (str(col), str(row[0])) in smallest_input_dict:
                available_pos += 1
                row.append(smallest_input_dict[(str(col), str(row[0]))])  # same as above (pair[0],pair[1]) and first pos is larger
            else:
                no_available_pos += 1
                row.append("No Available Position")
        empty_need += 1

    print("\nChecking ...... ")
    pairs = len(input_csv_list)  # total pairs in the input csv file
    x = Symbol('x')
    sols = solve(x**2 - x - pairs*2)  # use n(n-1)/2 trace back to original matrix format
    sol = 0
    for i in sols:
        if i > 0:
            sol = i  # take the positive sol from all function sols
    print(f"{pairs} pairs in input csv file = {sol} by {sol} matrix")
    print(f"{len(cleaned_input_list)} pairs in cleaned input list (rm prefix)")
    print(f"    First position larger pairs {first_larger_count} (Need this)")
    print(f"    Second position larger pairs {second_larger_count} (check reverse pos)")
    print(f"    Equal position pairs {equal_count} (ignore)")
    print(f"  Overall pairs: {first_larger_count + second_larger_count + equal_count}")
    print("...after taking smallest and checking reverse pos...")
    print(f"{len(list(smallest_input_dict.keys()))} pairs in smallest dict (this will be written into output)")

    print(f"\nOutput half matrix should have {len(position_range)*(len(position_range)-1)/2} values")
    print(f"\nBetween given input position range:")
    print(f"{available_pos} available positions(found on smallest dict)")
    print(f"{no_available_pos} no available positions(missing from smallest dict)")
    print(f"{available_pos} + {no_available_pos} = {no_available_pos + available_pos}")
    print(f"smallest dict VS available pos = {len(list(smallest_input_dict.keys()))} VS {available_pos}")

    write_csv(output_csv_list, output_csv_file)


main()



