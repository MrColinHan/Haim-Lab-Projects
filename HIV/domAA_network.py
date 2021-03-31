"""
Mar 16, 2021

@author: Changze Han
"""

'''
    HIV Project: 
        Inputs: 
            1. fisher network (in two col pairs format) MUST BE SORTED BY POS1 AND P_VALUE
            2. dominant AA data
        
        Process: 
            1.For a target position x, find the top n (e.g. 5) correlated positions (y1,y2,y3,y4,y5) from fisher matrix
            2.extract [x,y1...y5] from dom AA data
            3. for every AA-1 in x, take out the corresponding AA-1/0 from y1...y5
            4. for each position y1...t5, T test between: 
                    (suppose x has Z-1, T-1, D-0, E-1)
                    Z-1  vs  T-1
                    Z-1  vs  D-0
                    Z-1  vs  E-1
                    Z-1  vs  (T-1 + D+0 + E-1)
                at last: 
                    treat all 5 position as a whole, do the same T test again
        
        
        Outputs: 
            1. csv file for step 3
            2. csv file for all T tests in step 4

'''

from scipy import stats
import csv

# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/3.12.21 Single Dom AA/"
dom_input_name = "SingleB_dominant_AA.csv"
fisher_input_name = "SingleB_fisher.csv"

data_output_name = "outdata SingleB.csv"
ttest_output_name = "T Test SingleB.csv"

main_position = 536
main_pos_domAA = 'T'  # among all the dom AA at this pos, what's the dom AA
top_n_correlated_pos = 5  # select top 5 correlated pos
# ========================================================================================================

dom_input_file = working_dir + dom_input_name
dom_input_list = list()
fisher_input_file = working_dir + fisher_input_name
fisher_input_list = list()

data_output_list = list()
data_output_file = working_dir + data_output_name
ttest_output_list = list()
ttest_output_file = working_dir + ttest_output_name


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


def twotail_t_test(l1, l2):  # l1 and l2 are two lists
    return stats.ttest_ind(l1, l2)[1]

main_dataStructure = dict()
def main():
    read_csv(fisher_input_file, fisher_input_list)
    read_csv(dom_input_file, dom_input_list)

    fisher_header = fisher_input_list[0]
    fisher_content = fisher_input_list[1:]

    dom_header = dom_input_list[0]
    dom_content = dom_input_list[1:]

    print(f"dom AA data len: {len(dom_content)}")
    print(f"fisher data len: {len(fisher_content)}")

    top_cor_pos = list()  # store the top correlated positions
    for pair in fisher_content:
        if int(pair[0]) == main_position:
            if (len(top_cor_pos)!= 5) and (int(pair[1]) != (2+int(pair[0]))):
                top_cor_pos.append(int(pair[1]))

    print(f"{main_position}: {top_cor_pos}")

    main_position_index = dom_header.index(str(main_position))
    #print(main_position_index)
    #print(dom_header[main_position_index])
    top_cor_pos_index = list()
    for p in top_cor_pos:
        top_cor_pos_index.append(dom_header.index(str(p)))
    print("convert to col index")
    print(f"{main_position_index}: {top_cor_pos_index}")
    top_pos_index_dict = dict(zip(top_cor_pos, top_cor_pos_index))
    print("Zip:\n")
    print(top_pos_index_dict)
    print(f"\n\n")

    # data structure: main_dataStructure
    #
    # {362_Z-1: {815:[], 389:[], 440:[], ...},
    #  362_T-1: {815:[], 389:[], 440:[], ...},
    #  ...
    # }

    for row in dom_content:
        key_AA = row[main_position_index]
        if key_AA not in main_dataStructure:
            main_dataStructure[key_AA] = dict.fromkeys(top_cor_pos)

        for top_p in top_cor_pos:
            if main_dataStructure[key_AA][top_p] == None:
                main_dataStructure[key_AA][top_p] = [row[top_pos_index_dict[top_p]]]
            else:
                main_dataStructure[key_AA][top_p].append(row[top_pos_index_dict[top_p]])



    # format output AA-1
    # data_output_list
    data_output_header = [main_position]
    data_output_content = [[p] for p in top_cor_pos]


    for k_aa in main_dataStructure:
        print(f"{k_aa}: {main_dataStructure[k_aa]}")
        data_output_header += [k_aa]*(len(main_dataStructure[k_aa][top_cor_pos[0]]))

        for line_i in range(len(data_output_content)):
            dict_value = main_dataStructure[k_aa][data_output_content[line_i][0]]
            data_output_content[line_i] += dict_value

    data_output_content_withoutAA = list()
    for row in data_output_content:
        temp_row = [row[0]]
        for ele in row[1:]:
            if ele == 'None':
                temp_row.append(0)
            else:
                temp_row.append(int(ele.split('-')[1]))
        data_output_content_withoutAA.append(temp_row)



    #print(data_output_header)
    #print(data_output_content)
    #print(data_output_content_withoutAA)

    data_output_list = [data_output_header] + data_output_content
    write_csv(data_output_list, data_output_file)

    data_output_list_2 = [data_output_header] + data_output_content_withoutAA
    write_csv(data_output_list_2, working_dir+"withoutAA.csv")

    # Now starts T tests
    # main_pos_domAA

    print(f"\n=======remove AA=========\n")
    for k in main_dataStructure:
        for p in main_dataStructure[k]:
            temp_list = list()
            for aa in main_dataStructure[k][p]:
                if aa == 'None':
                    temp_list.append(0)
                else:
                    temp_list.append(int(aa.split('-')[1]))
            main_dataStructure[k][p] = temp_list






    unqualified_aa_keys = list()
    for k in main_dataStructure:
        if (k == f"{main_pos_domAA}-0"):
            unqualified_aa_keys.append(k)
        if len(main_dataStructure[k][top_cor_pos[0]]) < 2:
            unqualified_aa_keys.append(k)
    print(f"\nunqualified aa keys: {unqualified_aa_keys}")

    print(f"main datastructure len before del: {len(main_dataStructure)}")
    for e in unqualified_aa_keys:
        del main_dataStructure[e]

    # combine positions by the way
    main_dataStructure_combine = dict()
    for k in main_dataStructure:
        main_dataStructure_combine[k] = list()
        for p in main_dataStructure[k]:
            main_dataStructure_combine[k] += main_dataStructure[k][p]

    domAA_dict = {f"{main_pos_domAA}-1": main_dataStructure[f"{main_pos_domAA}-1"]}
    domAA_dict_combine =  {f"{main_pos_domAA}-1": main_dataStructure_combine[f"{main_pos_domAA}-1"]}
    del main_dataStructure[f"{main_pos_domAA}-1"]
    del main_dataStructure_combine[f"{main_pos_domAA}-1"]

    print(f"main datastructure len AFTER del: {len(main_dataStructure)}:")
    print(f"\nbeing compared: \n{domAA_dict}\n")

    for k_aa in main_dataStructure:
        print(f"{k_aa}: {main_dataStructure[k_aa]}")

    #singlePos_singleAA_level_ttest = list()
    singlePos_singleAA_level_header = [main_position]
    for k in main_dataStructure:
        singlePos_singleAA_level_header.append(f"{main_pos_domAA}-1 vs {k}")
    singlePos_singleAA_level_pValue = [[p] for p in top_cor_pos]
    for pos_line in singlePos_singleAA_level_pValue:
        current_p = pos_line[0]
        for aa_0 in main_dataStructure:
            main_compare = domAA_dict[f"{main_pos_domAA}-1"][current_p]
            #print(f"  {current_p}_{main_pos_domAA}-1: {main_compare}")
            #print("  VS")
            second_compare = main_dataStructure[aa_0][current_p]
            #print(f"  {current_p}_{aa_0}: {second_compare}\n")


            pos_line.append(twotail_t_test(main_compare, second_compare))
    print(singlePos_singleAA_level_header)
    print(singlePos_singleAA_level_pValue)

    write_csv([singlePos_singleAA_level_header]+singlePos_singleAA_level_pValue, working_dir+"singlePos_singleAA_test.csv")




    # ================================================================================================
    #main_dataStructure
    # remove all -0
    unqualified_aa_keys_2 = list()
    for k in main_dataStructure:
        if k == 'None':
            unqualified_aa_keys_2.append(k)
        else:
            if int(k.split('-')[1]) == 0:
                unqualified_aa_keys_2.append(k)
    print(f"\nunqualified aa: {unqualified_aa_keys_2}")

    for e in unqualified_aa_keys_2:
        del main_dataStructure[e]
    print(f"remove...\n")
    for k_aa in main_dataStructure:
        print(f"{k_aa}: {main_dataStructure[k_aa]}")

    # ================================================================================================
    singlePos_AllAA_level_pValue = [[p] for p in top_cor_pos]
    singlePos_AllAA_level_header = [main_position]

    singlePos_AllAA_level_header.append(f"{main_pos_domAA}-1 vs {list(main_dataStructure.keys())}")
    #print(singlePos_AllAA_level_header)

    for pos_line in singlePos_AllAA_level_pValue:
        current_p = pos_line[0]

        main_compare = domAA_dict[f"{main_pos_domAA}-1"][current_p]
        second_compare = list()
        for aa_0 in main_dataStructure:
            second_compare += main_dataStructure[aa_0][current_p]
        #print(f"  {current_p}_{main_pos_domAA}-1: {main_compare}")
        #print("  VS")
        #print(f"  {current_p}_{list(main_dataStructure.keys())}: {second_compare}\n")
        pos_line.append(twotail_t_test(main_compare, second_compare))
    write_csv([singlePos_AllAA_level_header] + singlePos_AllAA_level_pValue,
              working_dir + "singlePos_AllAA_test.csv")

    # ================================================================================================
    print(f"\n\nall pos, all aa level: \n")

    AlllePos_AllAA_level_header = [main_position]
    AllPos_AllAA_level_pValue = [top_cor_pos]

    print(domAA_dict_combine)
    print('\n')

    for k_aa in main_dataStructure_combine:
        print(f"{k_aa}: {main_dataStructure_combine[k_aa]}")

    for k in main_dataStructure_combine:
        AlllePos_AllAA_level_header.append(f"{main_pos_domAA}-1 vs {k}")


    for aa_0 in main_dataStructure_combine:
        main_compare = domAA_dict_combine[f"{main_pos_domAA}-1"]
        #print(f"  {main_pos_domAA}-1: {main_compare}")
        #print("  VS")
        second_compare = main_dataStructure_combine[aa_0]
        #print(f"  {aa_0}: {second_compare}\n")
        AllPos_AllAA_level_pValue.append(twotail_t_test(main_compare, second_compare))
        #print(twotail_t_test(main_compare, second_compare))

    write_csv([AlllePos_AllAA_level_header, AllPos_AllAA_level_pValue],
              working_dir + "AllPos_AllAA_test.csv")


    # ================================================================================================
    print(f"\n\nall pos, all aa level, all together: \n")

    main_compare = domAA_dict_combine[f"{main_pos_domAA}-1"]
    print(main_compare)

    second_compare = list()
    for i in main_dataStructure_combine:
        if i != 'None':
            if int(i.split('-')[1]) == 1:
                print(f"***{i}{main_dataStructure_combine[i]}")
                second_compare += main_dataStructure_combine[i]
    print(second_compare)
    print(f"Total compare Ttest: {twotail_t_test(main_compare, second_compare)}")

    print(domAA_dict_combine)
    print(main_dataStructure_combine)


main()





