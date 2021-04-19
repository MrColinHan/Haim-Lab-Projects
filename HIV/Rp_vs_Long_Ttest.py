"""
4.12.21
Changze Han

construct matrix for t-test between Rp(network volatility) and original Long volatility

inputs:
    1. Rp
    2. Long vol

pre-process inputs:
    sort by #env, remove <= 7 samples, then sort by patient and days

    use excel rm dup, keep one patient sample for each patient name

algorithm:

    e.g. Rp at pos 1 vs Long at pos 1

        put Rp and Long together, sort by Long

        the rows that Long = 0 is part A
        the rows that Long != 0 is part B

        T test between Rp part A and Rp part B

    at the end, -log10(x) for each t test p value


    output:
        first column is Rp
        first row is Long

"""
import csv
from scipy import stats
import itertools
from statistics import mean
from scipy.stats import sem
import math

# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/4.12.21 Rp Ttest/"
Rp_file_name = "Rp (use c pred c).csv"
long_file_name = "long c.csv"
output_file_name = "(all sample)Rp Ttest matrix(Use c pred c).csv"

pos_range = range(1, 857)

neg_log10 = False  # adjust t test p value to negative log 10
# ========================================================================================================
Rp_file = working_dir + Rp_file_name
long_file = working_dir + long_file_name
output_file = working_dir + output_file_name

rp_list = list()
long_list = list()
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


def pull_pos_valuelist(p, whole):
    # whole list as header
    result = list()
    p_index = None
    for i in whole[0]: # go through header
        if str(p) == i:
            p_index = whole[0].index(i)
    for row in whole[1:]:  # exclude header
        result.append(row[p_index])
    if result[0] == "no available fisher":
        return ("no available fisher")
    else:
        return ([float(x) for x in result])

def twotail_t_test(l1, l2):  # l1 and l2 are two lists
    return stats.ttest_ind(l1, l2)


def main():
    global rp_list, long_list, output_list

    read_csv(Rp_file, rp_list)
    read_csv(long_file, long_list)

    print(f"rp file len: {len(rp_list)}")
    print(f"long file len: {len(long_list)}")

    # check if two file have the same patient order
    for i in range(len(rp_list)):
        if rp_list[i][:5] != long_list[i][:5]:
            print('patient order messed up')

    output_list.append([None]+(list(pos_range)))
    for r_p in pos_range:  # rp's pos
        print(f"{r_p}...")
        temp_row = [r_p]
        for l_p in pos_range:  # long's pos

            rp_value_list = pull_pos_valuelist(r_p, rp_list)
            long_value_list = pull_pos_valuelist(l_p, long_list)

            if (rp_value_list == "no available fisher") or (long_value_list == "no available fisher"):
                temp_row.append("no available fisher")
            else:

                rp_partA = list()  # where long is 0
                rp_partB = list()  # where long is non 0

                for l_index in range(len(long_value_list)):
                    if long_value_list[l_index] == 0:
                        rp_partA.append(rp_value_list[l_index])
                    else:
                        rp_partB.append(rp_value_list[l_index])
                if neg_log10 == True:
                    temp_row.append (-math.log10(twotail_t_test(rp_partA, rp_partB)[1]))
                else:
                    temp_row.append(twotail_t_test(rp_partA, rp_partB)[1])

        output_list.append(temp_row)


    write_csv(output_list, output_file)


main()