"""
Changze Han
7.12.21
"""



import csv
# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/7.11.21 Figures/"
csv_name = "c 4tvp distance pairs.csv"
out_name = "selected_c_Distance_pairs_cd4.csv"
positions = ['97', '276', '279', '280', '281', '365', '460', '473', '474']
# glycan: ['137', '289', '295', '301', '332', '339', '362', '386', '392', '448']
# cd4: ['97', '276', '279', '280', '281', '365', '460', '473', '474']
# ========================================================================================================

def read_csv(filedir,listname):
    file = open(filedir)
    reader = csv.reader(file)
    for row in reader:
        listname.append(row)


def write_csv(x,y):  # write list x into file y
    with open(y,'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()


input_list = list()
output_list = list()


def main():
    read_csv(working_dir+csv_name, input_list)

    print(len(input_list))
    print(input_list[:3])

    for row in input_list:
        if (row[0] in positions) and (row[1] in positions):
            output_list.append(row)
    print(f"output len: {len((output_list))}")
    write_csv(output_list, working_dir+out_name)


main()