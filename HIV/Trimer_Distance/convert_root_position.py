"""
Created on Jan 06 2020

@author: Changze Han
"""
import itertools
import csv
'''
    (Note: Trimer coordinates are downloaded from https://www.rcsb.org )
    For HIV project - trimer distance step1 (in order to calculate euclidean distance on a trimer): 
    NAG, BMA, MAN, GAL, FUC contain positions that need to be converted to their root position. 
    e.g. A1088 -> A88, A1089 -> A88   
    NOTE: need to make sure int always starts at string[1:]. Meaning only first digit is prefix letter. 
'''
# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/1.3.20_trimer_distance/"
in_csv_name = "need_convert.csv"
out_csv_name = "converted.csv"
# ========================================================================================================
in_csv_file = working_dir + in_csv_name
out_csv_file = working_dir + out_csv_name
in_csv_list = []  # store input csv file
out_csv_list = []  # store output csv file

child_position_mapping = {
    88: [1088, 1089, 1090],
    135: [1135, 1136],
    156: [1156, 1157, 1158, 1160, 1161, 1162],
    187: [1187],
    241: [1241, 1242, 1243, 1244, 1245, 1246],
    262: [1262, 1263, 1264, 1265, 1266, 1267, 1268],
    276: [1276, 1277, 1278],
    295: [1295, 1296],
    301: [1301, 1302, 1303],
    332: [1332, 1333, 1334],
    339: [1339, 1340],
    355: [1355, 1356],
    362: [1362, 1363, 1364],
    386: [1386, 1387, 1388, 1390],
    392: [1392, 1393, 1394],
    397: [1397],
    448: [1448, 1449, 1450, 1451, 1452, 1453, 1454, 1455],
    616: [1600],
    611: [1611, 1612, 1613, 1614, 1617, 1619, 1620, 1621, 1622, 1623, 1624],
    625: [1625, 1626],
    637: [1637, 1638, 1639, 1640, 1641, 1642, 1643, 1644, 1645, 1646, 1647, 1648, 1650]
}

# use this list below to check whether a input child position is missing from the current table
all_child_positions = []  # store all child positions in POS_1600_MAPPING
all_child_positions = list(itertools.chain(*list(child_position_mapping.values())))  # flat the list


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
    read_csv(in_csv_file, in_csv_list)  # store input csv file to a list

    for row in in_csv_list:
        if int(row[0][1:]) in all_child_positions:
            temp_row = row[:]  # make a copy of this row
            for root in child_position_mapping:  # check each root position in the dict
                if int(row[0][1:]) in child_position_mapping[root]:  # if found root
                    temp_row[0] = f"{row[0][0]}{root}"  # convert first cell to root pos
                    out_csv_list.append(temp_row)  # add this row to output list
                    print(f"{row[0]} -> {temp_row[0]}")  # check
        else:
            raise ValueError(f"Error: Couldn't locate {row[0]} in the current dictionary.")

    write_csv(out_csv_list, out_csv_file)  # write the output csv file

    print(f"\nChecking: ")
    print(f"{len(in_csv_list)} rows in Input csv file")
    print(f"{len(out_csv_list)} rows in Output csv file")


main()

