"""
Created on Mar 3 2020

@author: Changze Han
"""
import csv
import numpy as np
import random
import copy
import math
import itertools
'''
    For HIV project: 
        After seeing clear clustering on MDS graph. 
        Use this program to analyze the significance of speciicity for each clustering on MDS. 
    
    Input: 
        Same input file that is put into the Orange. 
        Format:(not all attributes are required. only the shuffled one is necessary) 
        #ofEnv	Country	    Year	Patient	    Days	     137	        295       .....
         22	      US	    2010	  9018	    493	     0.819715305	0.197985387   .....
         20	      US	    2009	  9018	    189	     0.459186206	0.184845545   .....
         22	      US	    2006   700010040	 87	          0	        5.568233093
         .....
    
    Algorithms: 
        1. (optional, do this step in Excel) convert input data to binary ( 0 --> 0, non-0 --> 1)
        2. calculate a True value for each patient(or whatever attribute on the shuffle column): 
            2.a. calculate the centroid of each patient
            2.b. for each patient, calculate average distance (T) from its centroid to its points
        3. shuffle the patient name list 10,000 times:
            3.a. calculate the same average distance (t) for each patient during each shuffle
        4. Compare the 10,000 avg distance t with the true value T: 
            4.a. calculate how many times t are smaller than the T? 
'''
# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/3.29.21 MDS 10pat 10pos/"
#r"/Users/Han/Documents/Haim_Lab(2018_summer)/3.9.20_Orange/"
in_csv_name = r"(for P value)3.29.21 B&C 10pos 10 pat BINARY.csv"
#"(for p value)(cutoff10)(bin)B&C_10pos_12patients.csv"
# Final P value will be printed out in the console

shuffle_t = 100000  # shuffle times
shuffle_col = 3  # shuffle identifiers is at this col (will be shuffled)(starts at index 0)
pos_start = 5  # position starts at this col (starts at index 0)
# ========================================================================================================
input_file = working_dir + in_csv_name
input_file_list = []  # store input file to list

# separate input list into two parts
true_shuffle_column_list = []
true_value_columns_list = []

# dicts for True value
true_pat_value_dict = {}  # save original input value for each patient (each value start from pos_start)
true_pat_centroid_dict = {}  # save original centroid for each patient
true_pat_avgDis_dict = {}  # save original average distance for each patient

# dicts for shuffled vale
shuf_pat_value_dict = {}
shuf_pat_centroid_dict = {}
shuf_pat_avgDis_dict = {}


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


def find_centroid(lol):  # find the centroid of a list of multi-vector lists. e.g. [ [1,1,0,1],[0,0,1,1],[1,0,0,1],... ]
    cen_list = []
    length = len(lol)
    zip_lol = list(zip(*lol))
    for col in zip_lol:
        cen_list.append(sum([float(i) for i in col])/length)
    return cen_list


def comp_euclidean(list1, list2):  # compute euclidean distance between two multi-vector lists
    square_sum = 0
    for i in range(len(list1)):
        square_sum = square_sum + ((float(list2[i]) - float(list1[i]))**2)
    return math.sqrt(square_sum)


# go through input file, put same patient's value in one dict
# { pat1:[[row1],[row2],[row3],[row4]], pat2:[[row5],[row6]], ... }
# key is patient name, value is a list of lists, each inner value list starts from 'pos_start' col for each row
# s_c is the shuffle_col, p_s is the pos_start
def build_pat_val_dict(s_c, p_s, input_l, dic: dict):  # input_l is input list, save result to target dictionary dic
    for row in input_l[1:]:  # [1:] exclude header row
        if row[s_c] not in dic:  # row[shuffle_col] locates the shuffled attribute. e.g.'patient name'
            dic[row[s_c]] = []
            dic[row[s_c]].append(row[p_s:])  # add first inner-list value
        else:  # already in the dict
            dic[row[s_c]].append(row[p_s:])


# calculate the centroid for each patient
# in_dict the output dic from build_pat_val_dict(), save the centroids to out_dict
def build_pat_cen_dict(in_dic, out_dic):
    for pat in in_dic:  # iterate each patient key
        out_dic[pat] = find_centroid(in_dic[pat])  # save the centroid to new dict2


# calculate the average distance for each patient
# points_dict is the pat_value_dict, cen_dict is the pat_centroid_dict
def build_pat_aveDis_dict(points_dict, cen_dict, out_dict):
    for pat in points_dict:
        current_dis_sum = 0
        for point in points_dict[pat]:
            current_dis_sum += comp_euclidean(point, cen_dict[pat])
            print(f"{pat}: {comp_euclidean(point, cen_dict[pat])}")

        if pat not in out_dict:  # value is a list of average-distances. to record each shuffle's result
            out_dict[pat] = []
            out_dict[pat].append(current_dis_sum/len(points_dict[pat]))
        else:
            out_dict[pat].append(current_dis_sum/len(points_dict[pat]))


# separate input list into shuffle_column and the rest value_columns in order to re-combine after each shuffle
# the process is similar with build_pat_val_dict() function
def separate_input_list(in_list, shuf_col_list, value_cols_list):
    global shuffle_col
    global pos_start
    for row in in_list[1:]:  # exclude header row
        shuf_col_list.append(row[shuffle_col])
        value_cols_list.append(row[pos_start:])


def main():
    global input_file_list
    global shuffle_t
    global true_pat_value_dict
    global true_pat_centroid_dict
    global true_pat_avgDis_dict
    global true_shuffle_column_list
    global true_value_columns_list
    global shuf_pat_value_dict
    global shuf_pat_centroid_dict
    global shuf_pat_avgDis_dict

    read_csv(input_file, input_file_list)  # read input file
    total_sample_rows = len(input_file_list)-1  # input file's sample number, exclude header row

    print("========================================= Find True Value: ")
    # convert input list to dict **********************
    build_pat_val_dict(shuffle_col, pos_start, input_file_list, true_pat_value_dict)  # distribute input list to a dictionary
    if len(list(itertools.chain(*(true_pat_value_dict.values())))) != total_sample_rows:
        raise ValueError("ERROR: Total sample row in the dictionary doesn't match the input file. ")

    # find True centroid for each patient **********************
    build_pat_cen_dict(true_pat_value_dict, true_pat_centroid_dict)  # calculate the True centroid for each patient
    write_true_centroid_list = []  # write a buffer file to validate
    for pat_n in true_pat_centroid_dict:
        write_true_centroid_list.append([pat_n]+true_pat_centroid_dict[pat_n])
    write_csv(write_true_centroid_list, working_dir+"True_cen.csv")

    # compute True average distance for each patient **********************
    build_pat_aveDis_dict(true_pat_value_dict, true_pat_centroid_dict, true_pat_avgDis_dict)
    write_true_aveDis_list = []  # write a buffer file to validate
    for pat_n in true_pat_avgDis_dict:
        write_true_aveDis_list.append([pat_n]+true_pat_avgDis_dict[pat_n])
    write_csv(write_true_aveDis_list, working_dir+"True_avgDis.csv")

    # separate shuffle_column and the rest value_columns in order to re-combine after each shuffle
    separate_input_list(input_file_list, true_shuffle_column_list, true_value_columns_list)
    if (len(true_shuffle_column_list) != total_sample_rows) or (len(true_value_columns_list) != total_sample_rows):
        raise ValueError("ERROR: Total sample row in the divided_input_list doesn't match the input file. ")
    write_csv([true_shuffle_column_list] + true_value_columns_list, working_dir+"True_divided_input_list.csv")

    # ================== start shuffling process: re-generate input_list each shuffle =====================
    save_true_shuffle_t = copy.deepcopy(shuffle_t)  # keep a record for final p value division calculation
    while shuffle_t != 0:
        print(f"========================================= shuffle count down --- {shuffle_t}: ")
        # shuffle the target column
        new_shuffle_column = random.sample(true_shuffle_column_list, len(true_shuffle_column_list))
        # deepcopy so that the original value columns never change
        new_value_columns = copy.deepcopy(true_value_columns_list)
        # now re-combine shuffled input list
        for row in range(len(new_value_columns)):
            new_value_columns[row] = [new_shuffle_column[row]] + new_value_columns[row]
        new_value_columns.insert(0, [])  # insert a fake empty header row b/c the entire program assumes a header row
        # now new_value_columns is the new input_list

        # uncomment this line if want to see each shuffle's input
        '''
        write_csv(new_value_columns, working_dir+f"{shuffle_t}_input_list.csv")
        '''

        # now start analysis for this shuffle

        # convert shuffled input list to dict **********************
        shuf_pat_value_dict = {}  # reset this dict each shuffle
        build_pat_val_dict(0, 1, new_value_columns, shuf_pat_value_dict)
        if len(list(itertools.chain(*(shuf_pat_value_dict.values())))) != total_sample_rows:
            raise ValueError(f"ERROR during Shuffle {shuffle_t}: Total sample row in the dictionary doesn't match the input file. ")

        # find shuffled centroid for each patient **********************
        shuf_pat_centroid_dict = {}  # reset this dict each shuffle
        build_pat_cen_dict(shuf_pat_value_dict, shuf_pat_centroid_dict)
        # uncomment this block of code if want to see this shuffle's centroid
        '''
        temp_list = []
        for i in shuf_pat_centroid_dict:
            temp_list.append([i] + shuf_pat_centroid_dict[i])
        write_csv(temp_list, working_dir+f"{shuffle_t}_shuf_cen.csv")
        '''

        # compute shuffled average distance for each patient **********************
        print("       average distances: ")
        build_pat_aveDis_dict(shuf_pat_value_dict, shuf_pat_centroid_dict, shuf_pat_avgDis_dict)

        shuffle_t -= 1
    # ================== Finish shuffling process =====================

    # write all shuffled average distances to a file
    write_all_shuffled_aveDis_list = []
    for i in true_pat_avgDis_dict:  # use 'true_pat_avgDis_dict' to keep the order of patients the same in the output
        write_all_shuffled_aveDis_list.append([i] + shuf_pat_avgDis_dict[i])
    write_csv(write_all_shuffled_aveDis_list, working_dir+"all_shuffled_avgDis.csv")

    # now compare average distances in 'shuf_pat_avgDis_dict' with 'true_pat_avgDis_dict'

    final_pat_p_value_dict = {}
    for pat_name in shuf_pat_avgDis_dict:
        current_pat_count = 0  # count how many ave dis is less than the True ave dis
        for dis in shuf_pat_avgDis_dict[pat_name]:
            if dis < true_pat_avgDis_dict[pat_name][0]:
                current_pat_count += 1
        final_pat_p_value_dict[pat_name] = current_pat_count/save_true_shuffle_t


    # print all related info:
    print("\n========================================= info: ")
    print(f"input file :{total_sample_rows} rows data")
    print(f"found {len(list(true_pat_value_dict.keys()))} patients : {list(true_pat_avgDis_dict.keys())}")
    print(f"shuffle times : {save_true_shuffle_t}")
    print("P Values:")
    for final_pat in true_pat_avgDis_dict:
        print(f"{final_pat} : {final_pat_p_value_dict[final_pat]}")




main()



