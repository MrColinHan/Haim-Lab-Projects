import os, csv, itertools

inputDir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/5.10.21 B gp120 gp160dynaFD/6.7.21/new c FD/"


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


allFiles = []
def listFiles():
    #for filename in glob.glob(os.path.join(inputDir,'*.fas')):
    count = 0

    for filename in os.listdir(inputDir):
        if filename.endswith('.csv'):
            allFiles.append(filename)
            count = count + 1

    print ("Current number of files in this folder: "+str(count))
    print ("Files: "+str(allFiles))
    print ("\r\n")

listFiles()

output_list = list()

for each_f in allFiles:

    temp_loc = inputDir + each_f

    temp_f_list = list()
    read_csv(temp_loc, temp_f_list)

    pat_day = temp_f_list[0][0]
    first_row = list(itertools.repeat(pat_day, 857))

    temp_f_list.insert(0, first_row)

    if len(output_list) == 0:
        output_list = temp_f_list
    else:
        output_list = [a + b for a, b in zip(output_list, temp_f_list)]


write_csv([list(x) for x in zip(*output_list)], inputDir + "combined_csv_output.csv")
write_csv(output_list, inputDir + "tempout.csv")



