"""
Feb 12, 2021

@author: Changze Han
"""

'''
    HIV Project: 
        calculate network volatility. 
        
        inputs: 
            1. fisher p value pairs: 
                    a. convert matrix format to column format, meanwhile apply threshold, like 0.05
                    b. -log(x)+3 conversion 
                    c. add header:  Pos1 | Pos2 | fisher_P | 
            2. log-Long-Vol value: 
                    a. if 0 then 0.00001 (or 0.0001 depends on the min of long-vol)
                    b. log(x)+5  (or +4 depends)
        
        calculation process: 
            for each row in log-Long-Vol:
                for each target position P_target in this row:
                    find out all p_value_pairs that have P_target
                    for each pait(p_target,p_i,fisher):   # there are n pairs
                        sum += fisher at this pair * log-long-vol of p_i
                    sum = sum/n  # this is the network vol for P_target
                
        
        Output: 
            csv file
            value can be either a number or a 'No Fisher Available' which means there were no fisher value found within the threshold
'''

import csv
# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/2.15.21_hiv_cleaned_seq/"
fisher_input_filename = "b_sing_fisher_p(pairs).csv"
longVol_input_filename = "4.19.21_709volatility.csv"
output_filename = "Rp_709_singleBnetwork.csv"

position_range = (1, 856)
# ========================================================================================================

fisher_inputfile = working_dir + fisher_input_filename
longVol_inputfile = working_dir + longVol_input_filename
output_file = working_dir + output_filename

fisher_list = list()
longVol_list = list()


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
    global fisher_list, longVol_list

    read_csv(fisher_inputfile, fisher_list)
    read_csv(longVol_inputfile, longVol_list)

    print_out_txt = open(working_dir+"console_output.txt","w+")

    position_list = list(range(position_range[0], position_range[1]+1))

    # for each position, extract their fisher pairs, save to dict
    pos_fisherPair_dict = dict()  # key: pos, value: [[fisher pair1],[fisher pair2],[]]
    for p in position_list:
        pos_fisherPair_dict[p] = list()  # init dict
    for pair in fisher_list:
        pos_fisherPair_dict[int(pair[0])].append(pair)
        pos_fisherPair_dict[int(pair[1])].append([pair[1], pair[0], pair[2]])
    for k in pos_fisherPair_dict:
        print_out_txt.write(f"key {k}: \n")
        for v in pos_fisherPair_dict[k]:
            print_out_txt.write(f"    {v}\n")

    long_vol_header_row = longVol_list[0]
    output_list.append(long_vol_header_row)
    for row in longVol_list[1:]:  # exclude header row
        print(f"current row {row[:5]}: ===============")
        print_out_txt.write(f"current row {row[:5]}: ===============\n")
        current_row_network_vol = row[:5]

        # pos_longVol dict for current row
        currentRow_Pos_longVol_dict = dict()
        for p in position_list:
            currentRow_Pos_longVol_dict[p] = float(row[long_vol_header_row.index(str(p))])
        print(currentRow_Pos_longVol_dict)

        for p_target in position_list:
            #print(f"    p_target = {p_target}:")
            print_out_txt.write(f"    p_target = {p_target}:\n")

            # now find out all fisher pairs:
            fisher_pairs = pos_fisherPair_dict[p_target]

            current_p_netVol = None
            if len(fisher_pairs) != 0:
                current_p_netVol = 0  # init

                for f_p in fisher_pairs:
                    current_p_netVol += float(f_p[2]) * currentRow_Pos_longVol_dict[int(f_p[1])]
                    print_out_txt.write(f"        fisher:{f_p[2]}({f_p}) *"
                                        f" long-vol:{currentRow_Pos_longVol_dict[int(f_p[1])]}({f_p[1]})\n")

                current_p_netVol = current_p_netVol / len(fisher_pairs)
                current_row_network_vol.append(current_p_netVol)
            else:
                current_row_network_vol.append("no available fisher")




        output_list.append(current_row_network_vol)



    write_csv(output_list, output_file)
    print_out_txt.close()



'''
    pos_mls_dict = dict()  # key: all target positions, value: m-l-s
    for mls_pair in longVol_list[1:]: # skip header row
        pos_mls_dict[int(mls_pair[0])] = float(mls_pair[1])

    for target_p in pos_mls_dict:
        print(f"Target Pos {target_p}: ==============")
        target_fisher_pairs = list()
        for pair in fisher_list[1:]:  # skip header row
            if int(pair[0]) == target_p:
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
'''




main()


