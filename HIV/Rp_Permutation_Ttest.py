"""
Apr 26, 2021

@author: Changze Han
"""

'''
    HIV Project: 

        T test for Rp Permutation
'''

import csv
from scipy import stats
# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/2.15.21_hiv_cleaned_seq/Rp_Permutation/"
input_name = "169_permutation_Rp.csv"
output_name = "169_Rp_permutation_Ttest_OUTPUT.csv"
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


def twotail_test(l1, l2):  # l1 and l2 are two lists
    return stats.ttest_ind(l1, l2)


def main():
    read_csv(working_dir + input_name, input_list)

    print(f"input len {len(input_list)}")
    long_vol = [float(x) for x in input_list[0][1:]]
    #print(long_vol)

    real_Rp = [float(x) for x in input_list[1][1:]]
    #print(real_Rp)

    real_Ttest = twotail_test(long_vol, real_Rp)[1]
    print(f"real Ttest P value: {real_Ttest}")

    permu_ttest_list = ["T-test between Permu Rp and Long Vol"]
    for row in input_list[2:]:
        #print(row[1:])
        permu_Rp = [float(x) for x in row[1:]]
        permu_ttest_list.append(twotail_test(long_vol, permu_Rp)[1])

    # how many permu less than real
    count = 0
    for i in permu_ttest_list[1:]:
        if i < real_Ttest:
            count += 1

    output_list.append(["T-test between Real Rp and Long Vol", real_Ttest])
    output_list.append(permu_ttest_list)
    output_list.append(["(count permu < real)/10,000", count/10000])
    write_csv(output_list, working_dir + output_name)




main()