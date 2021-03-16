"""
Mar 8, 2021

@author: Changze Han
"""

'''
    HIV Project: 
        Input: network volatility
        
        this program takes a list of selected positions. 
        for each position:
            for each patient: 
                separate the network vol into two groups (and one ignore group) based on the reading of long vol file: 
                    group 1: long vol vol is 0, but next time point it becomes non-zero
                    group 2: long vol is 0, and next time point is still 0
        
        Outut: CSV
                    
'''

import csv

# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/3.8.21 Network Vol separator/"
long_vol_input_filename = "B Long vol.csv"
netVol_input_filename = "B network vol.csv"
#output_filename = "B Net Vol Separated Zero.csv"
#non_zero_output_filename = "B Net Vol Separated non-Zero.csv"

position_list = (426, 427, 429, 430, 431, 432, 446, 457, 458)
pos_start_index = 5 # position col starts at this index
patient_col_index = 3
day_col_index = 4

delta_day_cutoff = 120
# ========================================================================================================

long_vol_input_file = working_dir + long_vol_input_filename
netVol_input_file = working_dir + netVol_input_filename

#zero_output_file = working_dir + zero_output_filename
#non_zero_output_file = working_dir + non_zero_output_filename

long_vol_input_list = list()
netVol_input_list = list()

#zero_output_list = list()
#non_zero_output_list = list()


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
    global long_vol_input_list, netVol_input_list, zero_output_list, non_zero_output_list

    read_csv(long_vol_input_file, long_vol_input_list)
    read_csv(netVol_input_file, netVol_input_list)

    long_header = long_vol_input_list[0]
    long_content = long_vol_input_list[1:]

    netVol_header = netVol_input_list[0]
    netVol_content = netVol_input_list[1:]

    print(f"Long vol has {len(long_content)} rows")
    print(f"net vol has {len(netVol_content)} rows")

    for pos in position_list:

        # data struture:  {pat1: [(day1, vol1),(day2, vol2),(day3, vol3)], pat2: [(),()...], ...}

        pos_index = long_header.index(str(pos))
        print(f"pos{pos}, at idex {pos_index}: ========calculating=======")

        current_pos_dict = {}  # the above data structure
        for row in long_content:
            if row[patient_col_index] not in current_pos_dict:
                current_pos_dict[row[patient_col_index]] = [(row[day_col_index], row[pos_index])]
            else:
                current_pos_dict[row[patient_col_index]].append((row[day_col_index], row[pos_index]))

        current_zero_then_zero = list()  # save [(pat, day, vol), (pat, day+1, vol), ...] that day's long vol is 0 and day+1's long vol is also zero
        current_zero_then_NonZero = list()  # day's long vol is 0 and day+1's long vol is non zero
        for k in current_pos_dict:  # k is patient
            print(f"   {k}: --------")
            for i in range(len(current_pos_dict[k])):
                #print(f"        {current_pos_dict[k][i]}")
                if i != (len(current_pos_dict[k])-1):  # make sure it's not the last day
                    #print(current_pos_dict[k][i][1])
                    if (current_pos_dict[k][i][1] == str(0)) and (current_pos_dict[k][i+1][1] != str(0)):
                        day_t = current_pos_dict[k][i][0]
                        day_next_t = current_pos_dict[k][i+1][0]
                        delta_day = int(day_next_t) - int(day_t)
                        if delta_day < delta_day_cutoff:
                            current_zero_then_NonZero.append([k, current_pos_dict[k][i][0], delta_day,current_pos_dict[k][i][1]])
                        #print(f"        {current_pos_dict[k][i]}")
                            current_zero_then_NonZero.append([k, current_pos_dict[k][i+1][0], None,current_pos_dict[k][i+1][1]])
                        #print(f"        {current_pos_dict[k][i+1]}")
                            current_zero_then_NonZero.append([])
                        #print(f"        ~~~~~~~~~~")
                    elif (current_pos_dict[k][i][1] == str(0)) and (current_pos_dict[k][i+1][1] == str(0)):
                        day_t = current_pos_dict[k][i][0]
                        day_next_t = current_pos_dict[k][i + 1][0]
                        delta_day = int(day_next_t) - int(day_t)
                        if delta_day < delta_day_cutoff:
                            current_zero_then_zero.append([k, current_pos_dict[k][i][0], delta_day,current_pos_dict[k][i][1]])
                            print(f"        {current_pos_dict[k][i]}")
                            print(f"        {current_pos_dict[k][i+1]}\n")


        print("zero then non zero: ")
        print(current_zero_then_NonZero)
        # now match the corresponding network vol to this list
        # [[long_pat, long_day, delta_day,long_vol)], []]  --> [[long_pat, long_day, long_vol, , ,net_pat, net_day, delta day,net_vol)], []]
        for pat_day_i in range(len(current_zero_then_NonZero)):
            if current_zero_then_NonZero[pat_day_i] != []:

                for row in netVol_content:
                    if (current_zero_then_NonZero[pat_day_i][0] == row[patient_col_index]) and (
                            current_zero_then_NonZero[pat_day_i][1] == row[day_col_index]):
                        current_zero_then_NonZero[pat_day_i] += [None, None, None, row[patient_col_index],
                                    row[day_col_index], current_zero_then_NonZero[pat_day_i][2],row[pos_index]] # three empty coolumns between Long and Net

        print(current_zero_then_NonZero)
        # write this position into file
        #write_csv(current_zero_then_NonZero, working_dir+f"{pos}_zero_then_nonzero.csv")

        print("zero then zero")
        print(current_zero_then_zero)
        for pat_day_ii in range(len(current_zero_then_zero)):
            if current_zero_then_zero[pat_day_ii] != []:
                for row in netVol_content:
                    if (current_zero_then_zero[pat_day_ii][0] == row[patient_col_index]) and (
                            current_zero_then_zero[pat_day_ii][1] == row[day_col_index]):
                        current_zero_then_zero[pat_day_ii] += [None, None, None, row[patient_col_index],
                                    row[day_col_index], current_zero_then_zero[pat_day_ii][2],row[pos_index]] # three empty columns between Long and Net
        print(current_zero_then_zero)

        overall_output = [["long vol at day T is Zero, but Non-Zero at T+1"]] \
                         + [['patient', 'day(T and T+1)', 'delta day', 'Long Vol', None, None, None, 'patient', 'day(T and T+1)', 'Network Vol']] \
                         + current_zero_then_NonZero \
                         + [["long vol at day T is Zero, and also Zero at T+1"]] \
                         + [['patient', 'day(T)', 'delta day', 'Long Vol', None, None, None, 'patient', 'day(T)', 'Network Vol']] + current_zero_then_zero
        write_csv(overall_output, working_dir + f"B_{pos}_overall_output_>7.csv")



    






main()

