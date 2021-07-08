"""
Apr 26, 2021

@author: Changze Han
"""

'''
    HIV Project: 

        given a euclidean distance matrix of a trimer e.g. 5fuu
        give a list of target positions
        for each position, find out the closest 10 positions. 
'''

import csv
from scipy import stats
import operator
# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/4.26.21 trimer closest pos/"
input_name = "5fuu eucli dist.csv"
long_vol_name = "(log) C Long Vol.csv"

target_pos = [137, 289, 295, 301, 332, 339, 363, 386, 392, 448, 279, 280, 281, 282, 283, 365, 366, 367, 459, 460]

# ========================================================================================================
input_list = list()
output_list = list()


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
    global input_list, output_list, target_pos

    read_csv(working_dir + input_name, input_list)

    print(f"input list len:{len(input_list)}")

    for p in target_pos:
        print(f"{p}:")

        all_connected_pos_dict = dict()  # key: pos connected with p, value: dist

        for row in input_list:
            if int(row[0]) == p:
                if row[2] != "No Available Position":
                    all_connected_pos_dict[int(row[1])] = float(row[2])
            elif int(row[1]) == p:
                if row[2] != "No Available Position":
                    all_connected_pos_dict[int(row[0])] = float(row[2])

        sorted_all_connected_pos_dict = sorted(all_connected_pos_dict.items(), key=operator.itemgetter(1))
        #print(sorted_all_connected_pos_dict[:10])

        print([x[0] for x in (sorted_all_connected_pos_dict[:10])])
        print(f"=================================")


    # now extract long vol

    closest_positions = [461, 459, 462, 457, 458, 467, 463, 465, 464, 456]
    out_name = "c_460.csv"

    long_vol_list = list()
    read_csv(working_dir + long_vol_name, long_vol_list)

    closest_positions_index = list()
    for i in closest_positions:
        closest_positions_index.append(long_vol_list[0].index(str(i)))
    #print(closest_positions_index)

    for vol_row in long_vol_list:
        temp_out_row = vol_row[:5]
        for ii in closest_positions_index:
            temp_out_row.append(vol_row[ii])

        output_list.append(temp_out_row)
    write_csv(output_list, working_dir + out_name)







main()

