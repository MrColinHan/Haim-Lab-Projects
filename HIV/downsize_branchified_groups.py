"""
Changze Han
7.26.21

    This program takes a branchified groups txt file. divide the large groups (larger than the ceiling number) into
    multiple smaller groups. Also removes the groups that are smaller than the cutoff number.

"""

import re
# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/7.26.21 grouping/"
input_name = "GTR_G_0.007.txt"
output_name = "divided_groups.txt"

ceiling = 190
cutoff = 10
# ========================================================================================================
input_file = working_dir + input_name
output_file = working_dir + output_name
input_list = list()
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


def chunks(l, n):  # divide list l into chunks and each chunk size is n
    result = list()
    for i in range(0, len(l), n):
        result.append(l[i: i + n])
    return result


temp = [1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9]
print(chunks(temp, 3))


group_children_dict = dict()
new_group_children_dict = dict()


def main():
    global input_list, output_list, group_children_dict

    read_fasta(input_file, input_list)

    for i in range(len(input_list)):
        if 'Group' in input_list[i]:
            group_children_dict[input_list[i]] = list()
            for j in range(len(input_list)):
                if (j > i) and (input_list[j] != '\n'):
                    if 'Group' in input_list[j]:
                        break
                    else:
                        group_children_dict[input_list[i]].append(input_list[j])

    print(f"Start: {len(group_children_dict)} groups total")
    for group in group_children_dict:
        # greater than the ceiling
        if len(group_children_dict[group]) > ceiling:
            # divide into equal size chunks
            divided_group = chunks(group_children_dict[group], ceiling)
            group_name_2ndDash_index = [i.start() for i in re.finditer('_', group)][1]
            group_name_prefix = group[:group_name_2ndDash_index]
            count_new_groups = 0
            for new_group in divided_group:
                if len(new_group) >= cutoff:
                    new_group_name = group_name_prefix + f"_{count_new_groups}_" + str(len(new_group)) + "\n"
                    new_group_children_dict[new_group_name] = new_group
                    count_new_groups += 1
        # smaller than the ceiling
        else:
            if cutoff <= len(group_children_dict[group]) <= ceiling:
                new_group_children_dict[group] = group_children_dict[group]


    print(f"End: {len(new_group_children_dict)} groups total")

    for each_new_key in new_group_children_dict:
        output_list.append(each_new_key)
        for each_new_value in new_group_children_dict[each_new_key]:
            output_list.append(each_new_value)
        output_list.append("\n")

    write(output_list, output_file)

main()
