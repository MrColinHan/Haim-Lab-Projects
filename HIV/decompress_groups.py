"""
Changze Han
7.29.21

    This program takes two input files:
    1. key.names
    2. groups.txt
    each accession number in the groups.txt will be expanded/decompressed into multiple accession according to the
    key file.

"""

import re
# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/7.29.21 decompress/"
group_input_name = "GTR_G_0.007.txt"
key_input_name = "Decompress_key.names"
output_name = "decompressed_groups.txt"
# ========================================================================================================
group_input_file = working_dir + group_input_name
key_input_file = working_dir + key_input_name
output_file = working_dir + output_name
group_input_list = list()
key_input_list = list()
key_input_dict = dict()
output_list = list()


def read_fasta(x,y): # read a fasta file x and store into a list y
    file = open(x,"r")
    for line in file:
        y.append(line)


def write(x, y):  # write the list x into y file
    output= open(y,"w+")
    for i in x:
        output.write(i)
    output.close


group_children_dict = dict()


def main():
    global group_children_dict, key_input_dict

    read_fasta(group_input_file, group_input_list)

    read_fasta(key_input_file, key_input_list)

    # construct dict for group:accession
    for i in range(len(group_input_list)):
        if 'Group' in group_input_list[i]:
            group_children_dict[group_input_list[i]] = list()
            for j in range(len(group_input_list)):
                if (j > i) and (group_input_list[j] != '\n'):
                    if 'Group' in group_input_list[j]:
                        break
                    else:
                        group_children_dict[group_input_list[i]].append(group_input_list[j])
    print(f"{len(group_children_dict)} groups in the group file.")

    # construct dict for key accession: sub accession
    for key_row in key_input_list:
        temp_k = key_row.split('\t')[0]
        temp_v = key_row.split('\t')[1]
        key_input_dict[temp_k] = list()
        if ',' in temp_v:
            for v in temp_v.split(','):
                key_input_dict[temp_k].append(v.strip())
        else:
            key_input_dict[temp_k].append(temp_v.strip())

    print(f"{len(key_input_dict)} keys total in the .names file")

    for group in group_children_dict:
        group_name_2ndDash_index = [i.start() for i in re.finditer('_', group)][1]
        temp_group_name_prefix = group[:group_name_2ndDash_index]  # need to add '_count' after prefix
        temp_children_list = list()
        for child in group_children_dict[group]:
            if child.strip() in key_input_dict:
                decompressed_child = key_input_dict[child.strip()]
                for d_c in decompressed_child:
                    temp_children_list.append(f"{d_c}\n")
            else:
                temp_children_list.append(child)
        output_list.append(temp_group_name_prefix + '_' + str(len(temp_children_list)) + ':\n')
        for c in temp_children_list:
            output_list.append(c)
        output_list.append("\n")


    write(output_list, output_file)



main()