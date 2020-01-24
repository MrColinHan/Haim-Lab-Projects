#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 13:49:23 2019

@author: Changze Han
"""
import csv
from re import compile

'''
    For HIV Volatility Project: 
        This program calculates the in-host variance(volatility) for HIV. 
        More details : https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.2001549 
        
        Inputs: 
                1. PNGS converted AA sequences (positions need to be consecutive, no '-')
                  (attributes must contain 'Patient name', 'Days', 'Accession'. Other attributes are optional)
                   example format: 
                    | Clade | Country | Year | Patient | Days | Accession | 1 | 2 | 3 | ...
                    |   B   |    FR   | 1983 |   LAI   |  30  |   K03455  | M | R | V | ...
                
                2. Genetic distance matrix (from Mega)
                    
        Algorithm: 
                1. (Done by another program: hic_csv_splitter)
                   Separate PNGS sequences into multiple groups based on distinct 'PatientName-Days'. 
                   Each group contains multiple samples but they are all from the same patient and same days. 
                
                2. For each group: 
                        a. Construct a Phenotypic Distance Matrix for each Position 
                            a.1. if sequences are Amino acids, use hydropathy value for calculation
                            a.2. if sequences are already numbers, then use the current value for cal
                    
                    example: A.i.1 means patient name A, Days i, accession number 1
                        
                    --------------------------------------------------------------
             position 225 | A.i.1           | A.i.2           | A.i.3        | 
                    --------------------------------------------------------------
                    A.i.1 |                 |                 |              | 
                    --------------------------------------------------------------
                    A.i.2 | (A.i.1-A.i.2)^2 |                 |              | 
                    --------------------------------------------------------------
                    A.i.3 | (A.i.1-A.i.3)^2 | (A.i.2-A.i.3)^2 |              | 
                    --------------------------------------------------------------
                        
                        b. (Optional)Divide each Phenotypic Distance by corresponding Genetic distance
                        c. add the results together then divide by the count which is n(n-1)/2
                        d. the final result is the volatility for this positon in this group  
        Output: 
            | #ofEnv | Country | Year | Patient | Days | 1 | 2 | ......

            
            (to look for accession numbers in each group, go to the input 'separated_csv/' folder)
        
        Rules: 
            1. Ignore X, plus 0 and then (current_pos_divisor - 1)
            2. When GD = 0, numerator must be 0 too, so set GD = 1 and then (current_pos_divisor - 1)
            3. 'Not Valid' in the output meaning: maybe size too small and also contains many GD=0 which causes current_pos_divisor = 0


'''

# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/12.5.19_hiv_single/volatility/B_Val/B_Eur_val/"
png_seq_folder_name = "separated/"  # slash at the end
div_genetic_dis = True  # True: divides Phenotypic Distance by Genetic distance; False: divides Phenotypic Distance by 1                              
genetic_dis_file_name = "B_Eur_val_GD_Matrix.csv"
hydro = True  # True: use hydrophy value to calculate  False: Input sequences are already numbers instead of AA
average = False # True: calculate the average instead of volatility (just the avg of current position column's value, each cell must be number instead of AA)
output_file_name = "B_Eur_val_volatility.csv"
# average has its own build-in output name, no need to change this variable for average output

# tuples: attribute name and column number. !!! Col count starts from 0, NOT 1 !!!
# png_clade = ("Clade", 0)
png_country = ("Country", 0)
png_year = ("Year", 1)
png_name = ("Patient", 2)
png_days = ("Days", 3)  # IN single sample sequences, there's no Days
png_acc = ("Accssion", 3)
png_seq_start = 4  # start column number of sequences which is position 1

position_range = (1, 856)
# customize the output attributes
output_attributes = (png_country, png_year, png_name)
# note: #ofEnv for each group will always be added to the output

#debug = False  # True: write debug file;  False:
#debug_folder_name = "debug/" # for program debugging purpose, slash at the end
# ==========================================================================================

png_seq_folder = working_dir + png_seq_folder_name
name_list_file = working_dir + png_seq_folder_name + "allPatientNames.txt"
gd_file = working_dir + genetic_dis_file_name
output_file = working_dir + output_file_name
print_total_sample_num = 0 # store the total sample number in the folder check function
check_folder = False  # check folder function will change this to True

png_seq_header_row = []  # after checking the png file folder, save a header row here for final output
name_list = []  # read name list file and store the name list here
gd_list = []  # read the gd file and store here
all_groups_out_list = [] # for final outputs

ACCESSION_MATCHER = compile(r'[A-Za-z]{2}\d{6}|[A-Za-z]{1}\d{5}|[A-Za-z]{3}\d{5}')
HYDROPATHY_SCORE_TABLE = {
        'A': 0.68,
        'C': 0.733,
        'D': 0.19,
        'E': 0.203,
        'F': 1,
        'G': 0.584,
        'H': 0.304,
        'I': 0.958,
        'K': 0.403,
        'L': 0.953,
        'M': 0.782,
        'N': 0.363,
        'P': 0.759,
        'Q': 0.376,
        'R': 0.167,
        'S': 0.466,
        'T': 0.542,
        'V': 0.854,
        'W': 0.898,
        'Y': 0.900,
        'Z': 0,
        '-': 1.5,
        'X': 'unknown'
        }


def read_txt(x,y): # read a txt file x and store into a list y
    file = open(x,"r")
    for line in file:
        y.append(line)


def read_csv(filedir,listname):
    file = open(filedir)
    reader = csv.reader(file)
    for row in reader:
        listname.append(row)


def write_csv(x,y):  # write list x into file y
    with open(y,'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()


#extract accession from the given string, returns the first match if there are multiple matches
def getAccessNum(string):
    return ACCESSION_MATCHER.findall(string)[0]


def check_png_seq_folder(n):  # n is the name list. Use name list to search for files
    global png_seq_header_row
    global print_total_sample_num
    global check_folder
    for i in n:
        temp_list = []
        try:
            read_csv(f"{png_seq_folder}{i}.csv", temp_list)
            print_total_sample_num += (len(temp_list)-1)
        except:
            raise ValueError (f"Input file Error: Couldn't find file {i}.csv")
    check_folder = True  # everything is correct, give it True
    local_temp_png_list = []
    read_csv(f"{png_seq_folder}{n[0]}.csv", local_temp_png_list)  # read one seq file in the folder
    png_seq_header_row = local_temp_png_list[0]  # add the header row for final output use



# Genetic distance look up function: l is the list, x,y is a pair of accession number. Return a float value. 
def gd_look_up(l, x, y):
    # use two coordinates to locate the gd value
    gd = 0
    coord_1 = 0
    coord_2 = 0
    acc_row = l[0]  # first row is the accession number row
    check_access_pair = []  # (Double check procedure)after found the gd, add the two accessions to this list and compare with x,y
    #i = 0  # tracking index
    '''
    while coord_1 < len(acc_row):  # get the coord of 1st accession
        if acc_row[coord_1] == x: 
            break
        coord_1 += 1'''
    coord_1 = acc_row.index(x)
    '''
    while coord_2 < len(acc_row):  # get the coord of 2nd accession
        if acc_row[coord_2] == y: 
            break
        coord_2 += 1'''
    coord_2 = acc_row.index(y)
    if l[coord_1][coord_2] == '':  # this gd matrix only contains left half triangle, so value might be ''
        gd = l[coord_2][coord_1]
        check_access_pair.append(l[coord_2][0])
        check_access_pair.append(l[0][coord_1])

    else:
        gd = l[coord_1][coord_2]
        check_access_pair.append(l[coord_1][0])
        check_access_pair.append(l[0][coord_2])

    # check two accessions 
    if (x not in check_access_pair) or (y not in check_access_pair):
        raise ValueError("GD loop_up Error: accession pair doesn't match the input pair")

    return float(gd)


def find_all_comb(l): # find all combinations from a list
    result = []
    for i in range(len(l)):
        for j in range(i+1, len(l)):
            result.append([l[i],l[j]])

    return result



# calculate Phenotypic Distance within one group. png is png seq list; 
def one_group_volatility(png):
    global png_seq_start
    global output_attributes
    global png_acc
    global HYDROPATHY_SCORE_TABLE
    group_sample_ct = len(png)-1  # # store the group sample number, len of png minus the header row
    ini_gd = 1  # initial gd is 1
    one_group_out_list = []  # store the current group's final result to a list, reset every time the function called 
    divisor = int(group_sample_ct * (group_sample_ct-1) /2)  # n(n-1)/2 is the count of half a matrix; Use this number to check the combination counts later
    accession_list = []  # store current group's accession number in the list 

    one_group_out_list.append(group_sample_ct)  # add the group sample number to the beginning of the out list
    for i in output_attributes:  # go through customized output attributes
        # add this group's attribute values to the output in order; Use png[1] because they all have the same value anyway
        one_group_out_list.append(png[1][i[1]])

    acc_i = 1  # keep track accession number index
    while acc_i < len(png):
        if (png[acc_i][png_acc[1]],acc_i) not in accession_list:
            accession_list.append((png[acc_i][png_acc[1]],acc_i))
        acc_i += 1
    comb_accession_list = find_all_comb(accession_list)  # construct the Phenotypic Dis matrix in combinarion pairs
    # format of comb_accession_list:  all combination pairs of tuple (accession number, index of this row)
    #       [ [(acc1, 1),(acc2, 2)], [(acc1, 1),(acc3, 3)], [(acc2, 2),(acc3, 3)] ]

    #print(accession_list)
    #print(comb_accession_list)
    if group_sample_ct == len(accession_list):  # check the total sample count again
        print(f"       {group_sample_ct} samples; {len(comb_accession_list)} pairs in the Pheno dis matrix")
    else:
        raise ValueError("Sample Count Error in accession_list of one_group_volatility(png) function! ")

    # check if the count of comb matches the divisor n(n-1)/2
    if len(comb_accession_list) != divisor:
        raise ValueError("Divisor doesn't match the total count of all combination pairs! ")

    start_pos = position_range[0]
    end_pos = position_range[1]
    while start_pos <= end_pos: # loop through all positions
        current_pos_divisor = divisor  # copy the divisor for each position. Divisor -1 when met gd = 0
        current_pos_vol = 0  # volatility of current position
        current_pos_index = png_seq_start + start_pos -1  # index of the current position
        if png[0].index(str(start_pos)) != current_pos_index:  # check the all positions' index just incase
            raise ValueError(f"Input Error: Sequence Starting column number is wrong at {start_pos} ")

        for pair in comb_accession_list:  # calculate the distance for each pair
            if hydro == True:  # assign hydropathy value
                diff_1 = HYDROPATHY_SCORE_TABLE[png[pair[0][1]][current_pos_index]]  # png[pair[0][1]] finds the row, [current_pos_index] finds the pos col
                diff_2 = HYDROPATHY_SCORE_TABLE[png[pair[1][1]][current_pos_index]]
            else:   # use current value in the sequence
                diff_1 = int(png[pair[0][1]][current_pos_index])
                diff_2 = int(png[pair[1][1]][current_pos_index])

            if (diff_1 == 'unknown') or (diff_2 == 'unknown'):  # check for 'X'
                diff_sq = 0  # ignore 'X' AA, just set diff_sq to 0
                current_pos_divisor -= 1  # total count -1
            else:
                diff_sq = (diff_1 - diff_2)**2  # square the difference

            if div_genetic_dis == True:  # look up value on GD matrix
                ini_gd = gd_look_up(gd_list, pair[0][0], pair[1][0]) # look up the gd by accession number pair
                if ini_gd == 0:  # When GD = 0, numerator must be 0 too
                    ini_gd = 1  # so set gd to 1 because it doesnt matter when numerator is 0
                    current_pos_divisor -= 1  # total count -1

            current_pos_vol += (diff_sq/ini_gd)

        if current_pos_divisor != 0:
            current_pos_vol = current_pos_vol/current_pos_divisor

        else:
            current_pos_vol = 'Not Valid'
        one_group_out_list.append(current_pos_vol)  # add current position's volatility to the out list
        start_pos += 1

    return one_group_out_list


temp_png_list = []
def cal_each_group_volatility():
    global output_attributes
    global all_groups_out_list  # final output list
    current_group_png = []  # read one png file at a time and save it to this list
#======================temporary variable for average cal=======================
    all_group_average_out_list = []
#===============================================================================
    header_row = []  # a local list for constructing and storing the header row for the final output
    header_row.append("#ofEnv")  # add the sample number attribute to the front
    for i in output_attributes:  # go through customized output attributes
        header_row.append(png_seq_header_row[i[1]])  # add the header attributes in the first row
    all_groups_out_list.append(header_row + png_seq_header_row[png_seq_start:])  # add the positions in the first row and add to the final output list

    for i in name_list:  # formal loop for calculating each group's volatility and constructing final output list
        current_group_png = []  # reset the list just in case
        read_csv(f"{png_seq_folder}{i}.csv" , current_group_png)
        print(f"{i}: ")
         # cal current group's volatiloty and add it to all groups' final output
        all_groups_out_list.append(one_group_volatility(current_group_png))


    write_csv(all_groups_out_list, output_file)  # write the final output file
#======================calculate average code===================================
'''
        current_group_average_out_list = []  # save current group's 
        current_group_average_out_list = [len(current_group_png)-1] + current_group_png[1][:(png_acc[1])]
        ave_pos_start = position_range[0]  # starting position
        ave_pos_end = position_range[1]  # ending position
        average_row_count = 0  #  check sample number for debugging
            
        while ave_pos_start <= ave_pos_end:  # iterate through all required positions
            ave_pos_current = png_seq_start + ave_pos_start -1  # translate current position to correct index
            ave_pos_current_list = []
            for row in current_group_png[1:]: #add each row's current position's value to list
                ave_pos_current_list.append(int(row[ave_pos_current]))  # add this position's value to list
                average_row_count += 1
            current_group_average_out_list.append(sum(ave_pos_current_list)/len(ave_pos_current_list))  # calculate average of this position 
            ave_pos_start += 1
        
        all_group_average_out_list.append(current_group_average_out_list)  # add this group's average to output as a row
    
    # add header row: '#ofEnv' + all attributes except accession + positions
    all_group_average_out_list.insert(0,["#ofEnv"] + current_group_png[0][:(png_acc[1])] + current_group_png[0][png_seq_start:])
    if average == True:   
        write_csv(all_group_average_out_list, f"{working_dir}average.csv")
 '''
#===============================================================================
    #write_csv(all_groups_out_list, output_file)  # write the final output file



def main():
    global name_list
    global gd_list
    read_txt(name_list_file, name_list)  # read the name list file and save to a list
    name_list = name_list[0].split(",")  # comma-delimited

    check_png_seq_folder(name_list)  # check the seq file folder

    read_csv(gd_file, gd_list)  # read the gd file to a list

    cal_each_group_volatility()

    if check_folder == True:
        print(f"\n{len(name_list)} PNGS sequence files found in the folder")
        print(f"with a total sample number: {print_total_sample_num}\n")

    print(f"{len(gd_list[0])-1} samples found in the genetic distance file")

    if average == True:
        print("\nAlso calculated average")


main()




