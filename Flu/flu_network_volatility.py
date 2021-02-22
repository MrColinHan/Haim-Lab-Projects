"""
Feb 3, 2021

@author: Changze Han
"""

'''   !!!!!!!!!!!!!!!!! THERE IS A BUG AT LINE 78 !!!!!!!!!!!!!!!!!'''

'''
    Flu Project: 
        calculate network volatility. 
        
        inputs: 
            1. fisher p value: 
                    a. convert matrix format to column format, meanwhile apply threshold, like 0.05
                    b. -log(x)+3 conversion 
                    c. add header:  Pos1 | Pos2 | fisher_P | 
            2. Mean-log-stdev value: 
                    a. transpose paste to column format :  Position | value | 
        
        calculation process: 
            for each P_target in mean-log-stdev:
                extract all Pos pairs that have P from fisher values
                for each pair (P_target, P_i, fisher):   # there are n pairs, from P_1 to P_i
                    sum += fisher at this pair * m-l-s for P_i
                sum = sum / n  # this is the network volatility for position P_target
        
        Output: 
            csv file
            value can be either a number or a 'None' which means there were no fisher value found within the threshold
'''

import csv
# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/2.3.21_flu_network_volatility/"
fisher_input_filename = "(negLog)(pairs)H3N2_allSample_fisher.csv"
meanLogStd_input_filename = "3C3_beforeShift_mean-log-stdev.csv"
output_filename = "network_volatility_3C3_beforeShift.csv"

# ========================================================================================================

fisher_inputfile = working_dir + fisher_input_filename
meanLogStd_inputfile = working_dir + meanLogStd_input_filename
output_file = working_dir + output_filename

fisher_list = list()
meanLogStd_list = list()


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

output_list = list()
def main():
    global fisher_list, meanLogStd_list

    read_csv(fisher_inputfile, fisher_list)
    read_csv(meanLogStd_inputfile, meanLogStd_list)

    pos_mls_dict = dict()  # key: all target positions, value: m-l-s
    for mls_pair in meanLogStd_list[1:]: # skip header row
        pos_mls_dict[int(mls_pair[0])] = float(mls_pair[1])

    for target_p in pos_mls_dict:
        print(f"Target Pos {target_p}: ==============")
        target_fisher_pairs = list()
        for pair in fisher_list[1:]:  # skip header row
            if (int(pair[0]) == target_p) or (int(pair[1]) == target_p):
                target_fisher_pairs.append(pair)
                print(f"   {pair}")
        target_sum = None
        if len(target_fisher_pairs) != 0:  # when where are available fisher values
            target_sum = 0
            for selected_pair in target_fisher_pairs:
                target_sum += float(selected_pair[2]) * pos_mls_dict[int(selected_pair[1])]
            print(f"          Sum: {target_sum} *******************")
            target_sum = target_sum/len(target_fisher_pairs)
            print(f"          network volatility: {target_sum} *******************")
            output_list.append([target_p, target_sum])
        else:
            output_list.append([target_p, 'No Fisher Available'])

    write_csv(output_list, output_file)



main()


