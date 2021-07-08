

import csv

# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/5.10.21 B gp120 gp160dynaFD/"
FD_name = "Clade B gp120 Dyna-FD.csv"
Anc_dict_name = "B Ancestor AA PNGS.csv"
output_name = "Clade B gp120 Ancestor-FD.csv"
# ========================================================================================================


def read_csv(filedir ,listname):
    file = open(filedir)
    reader = csv.reader(file)
    for row in reader:
        listname.append(row)


def write_csv(x ,y):  # write list x into file y
    with open(y ,'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()


fd_list = list()
anc_dic_list = list()

fd_content = list()

output_list = list()

def main():
    global fd_list, anc_dic_list, fd_content

    read_csv(working_dir + FD_name, fd_list)
    read_csv(working_dir + Anc_dict_name, anc_dic_list)

    fd_header = fd_list[0]
    fd_content = fd_list[1:]

    anc_dic_content = anc_dic_list[1:]

    print(f"fd len: {len(fd_content)}")
    print(f"anc len: {len(anc_dic_content)}")

    anc_Dict = dict()
    for row in anc_dic_content:
        anc_Dict[row[0]] = row[1]

    print(f"\nanc dic len: {len(anc_Dict)}")
    print(anc_Dict)


    for i in fd_content:
        current_anc = anc_Dict[i[0]]

        if current_anc != '-':
            fd_header_index = fd_header.index(current_anc)
            current_anc_percent = i[fd_header_index]
            temp_output = [i[0], i[1], current_anc, current_anc_percent]
        else:
            temp_output = [i[0], i[1], current_anc, 'This Anc is not AA']

        output_list.append(temp_output)
        temp_output = list()

    write_csv(output_list, working_dir + output_name)


main()



