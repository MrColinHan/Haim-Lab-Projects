"""
Apr 26, 2021

@author: Changze Han
"""

'''
    HIV Project: 
        
        read cutoff fisher matrix, count rows that have target position and save as random_PosCount
        from position range, pick random_PosCount number of positions as the network for 332
        for each random picked network, calculate the Rp
        
        Output: 
            10,000 rows
            each row is one Rp for this pos
'''

import csv
import random
# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/2.15.21_hiv_cleaned_seq/Rp_Permutation/"
all_fisher_name = "(log)sing b fisher ALL(pairs).csv"
cutoff_fisher_name = "(log)sing_b_fisher_0.05.csv"
long_vol_name = "(log_oneSample)21721_b long vol(env8).csv"

target_pos = 169
shuffle_time = 10000
output_filename = "169_permutation_Rp.csv"

position_range = (1, 856)
# ========================================================================================================
all_fisher_list = list()
cutoff_fisher_list = list()
long_vol_list = list()

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

random_PosCount = 0
all_fisher_dict = dict()
def main():
    global all_fisher_list, cutoff_fisher_list, long_vol_list, random_PosCount, shuffle_time, all_fisher_dict

    read_csv(working_dir + all_fisher_name, all_fisher_list)
    read_csv(working_dir + cutoff_fisher_name, cutoff_fisher_list)
    read_csv(working_dir + long_vol_name, long_vol_list)

    print(f"all fisher len:{len(all_fisher_list)}")
    print(f"cutoff fisher len: {len(cutoff_fisher_list)}")
    print(f"long vol len:{len(long_vol_list)}")

    # now many pos in the original network?
    for row in cutoff_fisher_list:
        if (row[0] == str(target_pos)) or (row[1] == str(target_pos)):
            random_PosCount += 1
    print(f"random posCount is {random_PosCount}")

    # convert all fisher matrix into a dict
    # all_fisher_dict  # only include the pos that connected with target pos, key: pos, value: fisher
    for row in all_fisher_list:
        if int(row[0]) == target_pos:
            all_fisher_dict[int(row[1])] = float(row[2])
        elif int(row[1]) == target_pos:
            all_fisher_dict[int(row[0])] = float(row[2])
    print(f"all fisher dict len (should be {position_range[1]-1}): {len(all_fisher_dict)}")
    print(f"\nstart permutation: \n")
    while shuffle_time != 0:
        print(f"{shuffle_time}------")
        # randomly pick position network
        random_PosNetwork = dict()  # key:pos, value: fisher between this pos and target pos

        while len(random_PosNetwork) != random_PosCount:  # stop when random network has enough pos
            r_pick = random.randint(position_range[0], position_range[1])
            if (r_pick not in random_PosNetwork) and (r_pick != target_pos): # cant be in dict already, cant be target itself
                random_PosNetwork[r_pick] = all_fisher_dict[r_pick]
        #print(f"random network len: {len(random_PosNetwork)}")
        #print(random_PosNetwork)

        output_row = [f"permu_Rp_{target_pos}"]  # output row for current permutation
        for long_row in long_vol_list[1:]: # exclude first row
            current_sum = 0

            for p in random_PosNetwork:
                #print(f"{p}: {long_vol_list[0].index(str(p))}  {long_row[long_vol_list[0].index(str(p))]}")
                #print(random_PosNetwork[p])
                current_sum += (random_PosNetwork[p] * float(long_row[long_vol_list[0].index(str(p))]))

            output_row.append(current_sum/random_PosCount)  # add this patient Rp to this output row

        output_list.append(output_row)  # add this permutation output to final output

        shuffle_time -= 1




    write_csv(output_list, working_dir + output_filename)


main()


