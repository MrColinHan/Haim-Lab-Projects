import csv



inputDir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/5.10.21 B gp120 gp160dynaFD/6.7.21/"

input_file = "c NEW patient-day FD(glycan&cd4).csv"
output_file = "NEW domAA_c_glycan&cd4.csv"



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


input_list = list()
read_csv(inputDir + input_file, input_list)

output_list = list()
header = input_list[0]
for row in input_list[1:]:
    number_list = [float(x) for x in row]
    max_fd = max(number_list)
    max_fd_index = number_list.index(max_fd)
    output_list.append([f"{header[max_fd_index]}-{max_fd}"])

write_csv(output_list, inputDir+output_file)