import csv
from sympy import *
# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/1.3.20_trimer_distance/"
in_csv_name = "wrong-forgot_reverse(pairs).csv"
in_csv2_name = "(position)5fuu_dis_pairs.csv.csv"
out_csv_name = "compare.csv"

# ========================================================================================================

input_csv_file = working_dir + in_csv_name
input_csv2_file = working_dir + in_csv2_name
output_csv_file = working_dir + out_csv_name
input_csv_list = []
input_csv2_list = []
output_csv_list = []



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


read_csv(input_csv_file, input_csv_list)
read_csv(input_csv2_file, input_csv2_list)

print(len(input_csv_list))
print(len(input_csv2_list))

row = 0
count = 0
while row < len(input_csv_list):
    if input_csv_list[row] != input_csv2_list[row]:

        if (input_csv_list[row][2] == 'No Available Position') or (input_csv2_list[row][2] == 'No Available Position') \
                or (abs(float(input_csv_list[row][2]) - float(input_csv2_list[row][2])) > 10.0):
            count += 1
            print(f"{input_csv_list[row][2]} VS {input_csv2_list[row][2]}")

    row += 1

print(f"{count} not same")

