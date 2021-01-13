"""
Created on Dec 1 2020

@author: Changze Han
"""

'''
    For Volatility project:
    
    After downloading new Long sequence from Lanl, compare the new patient names with the 
    old sequences. Identify the names that didnt appear in old ones. 
    
    input: old sequence file in csv 
           new sequence file in fasta
        
    Note: 
        csv old seq attributes order: Clade Country Year Patient Days Accession
        
        fasta new seq attributes order: (separated by '.')
            # only use two attributes to simplify things
            >clade.patient code
            
            
            # complete attributes is below, but abondoned this option
            Subtype.Country.Sampling Year.Name.Accession.#of patient timepoints.Patient Code.PAT id(SSAM).Se ID.#of patient seqs.Sequence Length.Organism                                     
            e.g. >B.FR.1983.HXB2-LAI-IIIB-BRU.K03455.3.LAI.19535.189022.391.9719.HIV-1

'''

import csv
# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/12.1.20_Flu&HIV/HIV/"
old_seq_filename = "(B&C)old_Long_seq_attributes.csv"
new_seq_filename = "HIV_Long_27846(clade_code).fasta"

output_filename = "compare_seqs_results.csv"
# ==========================================================================================
old_seq_file = working_dir + old_seq_filename
new_seq_file = working_dir + new_seq_filename
output_file = working_dir + output_filename

old_seq_list = list()
new_seq_list = list()
output_list = list()


def read_fasta(x, y):  # read a fasta file x and store into a list y
    file = open(x, "r")
    for line in file:
        y.append(line)


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


old_seq_unique_code_list = list()
new_seq_unique_code_list = list()
old_clade_code_dict = dict()
new_clade_code_dict = dict()


def main():
    global new_seq_file, old_seq_file, new_seq_list, old_seq_list,\
        old_seq_unique_code_list, new_seq_unique_code_list, old_clade_code_dict, new_clade_code_dict


    read_csv(old_seq_file, old_seq_list)

    for i in old_seq_list[1:]:  # exclude header row

        if i[3] not in old_seq_unique_code_list:  # [3] is the patient code column
            old_seq_unique_code_list.append(i[3])

            if i[0] not in old_clade_code_dict:  # count num of names in each clade
                old_clade_code_dict[i[0]] =  list()
                old_clade_code_dict[i[0]].append(i[3])
            else:
                old_clade_code_dict[i[0]].append(i[3])

    print(f"old seq contains {len(old_seq_list) - 1} seqs, {len(old_seq_unique_code_list)} unique patient code")
    print(f"# of patient codes in each clade: ")
    for k in old_clade_code_dict:
        print(f"{k} : {len(old_clade_code_dict[k])}")

    read_fasta(new_seq_file, new_seq_list)
    new_seq_count = 0

    for l in new_seq_list:

        if l[0] == '>':
            new_seq_count += 1
            current_clade = l.split('.')[0][1:]  # [0] is '>B', [0][1:] is 'B'
            current_code = l.split('.')[1].strip()

            if current_code not in new_seq_unique_code_list:
                new_seq_unique_code_list.append(current_code)

                if current_clade not in new_clade_code_dict:
                    new_clade_code_dict[current_clade] = list()
                    new_clade_code_dict[current_clade].append(current_code)
                else:
                    new_clade_code_dict[current_clade].append(current_code)

    print(f"\n\nnew seq contains {new_seq_count} seqs, {len(new_seq_unique_code_list)} unique patient code")
    print(f"# of patient code in each clade: ")
    for k in new_clade_code_dict:
        print(f"{k} : {len(new_clade_code_dict[k])}")

    # format output
    output_list = [["Old Seq Info:"],
                   ["Total # of seq:", len(old_seq_list) - 1],
                   ["# of unique seq:", len(old_seq_unique_code_list)],
                   ['Break down to clades:'],
                   ]
    for i in old_clade_code_dict:
        output_list.append([f"{i} :", len(old_clade_code_dict[i])])
        output_list.append(old_clade_code_dict[i])

    output_list += [[], [], [],
                    ["New Seq Info:"],
                    ["Total # of seq:", new_seq_count],
                    ["# of unique seq:", len(new_seq_unique_code_list)],
                    ['Break down to clades:'],
                    ]
    for i in new_clade_code_dict:
        output_list.append([f"{i} :", len(new_clade_code_dict[i])])
        output_list.append(new_clade_code_dict[i])


    # compare difference between two unique code lists:
    in_old_not_in_new = list()
    in_new_not_in_old = list()
    in_old_also_in_new = list()
    for code in old_seq_unique_code_list:
        if code not in new_seq_unique_code_list:
            for k in old_clade_code_dict:
                if code in old_clade_code_dict[k]:
                    in_old_not_in_new.append(f"{code}~~~{k}")

    for code in new_seq_unique_code_list:
        if code not in old_seq_unique_code_list:
            for k in new_clade_code_dict:
                if code in new_clade_code_dict[k]:
                    in_new_not_in_old.append(f"{code}~~~{k}")

    for code in new_seq_unique_code_list:
        if code in old_seq_unique_code_list:
            for k in new_clade_code_dict:
                if code in new_clade_code_dict[k]:
                    in_old_also_in_new.append(f"{code}~~~{k}")

    print(f"in_old_not_in_new: {len(in_old_not_in_new)}")
    print(in_old_not_in_new)
    print(f"in_new_not_in_old: {len(in_new_not_in_old)}")
    print(in_new_not_in_old)
    print(f"in_old_also_in_new: {len(in_old_also_in_new)}")
    print(in_old_also_in_new)
    output_list += [[], [], [],
                    ["in_old_not_in_new:", len(in_old_not_in_new)],
                    in_old_not_in_new,
                    [], [],
                    ["in_new_not_in_old:", len(in_new_not_in_old)],
                    in_new_not_in_old,
                    [], [],
                    ["in_old_also_in_new:", len(in_old_also_in_new)],
                    in_old_also_in_new
                    ]

    write_csv(output_list, output_file)


main()




