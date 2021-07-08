"""
Apr 28, 2021

@author: Changze Han
"""


'''

    input: pair format trimer distance
            or
           pair format co vol 
           
    given a list of positions
    
    output: 
          rows that [0] [1] are all in the given pos list

'''

import csv
from scipy import stats
# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/4.28.21 5fuu vs covol/"
input_name = "5fuu eucli dist.csv"
output_name = "cd4_5fuu eucli dist.csv"

pos_list = [97, 276, 278, 279, 280, 281, 282, 283, 365, 366, 367, 368, 371, 427, 428, 429, 430, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 469, 472, 473, 474, 476, 1276]

# cd4: 97, 276, 278, 279, 280, 281, 282, 283, 365, 366, 367, 368, 371, 427, 428, 429, 430, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 469, 472, 473, 474, 476, 1276
# glycan: 137, 295, 301, 332, 339, 363, 386, 392, 448
# trimer associ domain: 128, 130, 132, 156, 160, 165, 167, 168, 169, 170, 171, 173, 197, 301, 161, 164

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

    read_csv(working_dir + input_name, input_list)
    print(f"input len: {len(input_list)}")

    for row in input_list:
        if (int(row[0]) in pos_list) and (int(row[1]) in pos_list):
            output_list.append(row)
    print(f"output len: {len(output_list)}")
    write_csv(output_list, working_dir + output_name)


main()
