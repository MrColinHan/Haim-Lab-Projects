"""
Feb 22, 2021

@author: Changze Han
"""

'''
    For Crime data project: 
        Data source: https://catalog.data.gov/dataset/crime-data-from-2010-to-2019
        
        this program take the CSV file and separated it into individual csv files for each year. 
        use the collumn "DATE OCC"
        
        date format must be  '10/30/2011 12:00:00 AM'

'''

import csv
# Inputs ================================================================================================
working_dir = r"/Users/Han/MacMini_Local/HaimLab_CrimeData/"
input_filename = "Crime_Data_from_2010_to_2019.csv"
output_foldername = "separated_csv/"

date_col = 2  # index starting from 0
# ========================================================================================================
input_file = working_dir + input_filename
output_folder = working_dir + output_foldername
input_list = list()


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


def main():
    global input_list, input_file, output_folder, date_col

    read_csv(input_file, input_list)
    year_rows_dict = dict()  # key = year, value = list of rows that belong to this year

    header = input_list[0]
    content = input_list[1:]
    for row in content:
        row_year = row[date_col].split()[0].split('/')[2]
        if row_year not in year_rows_dict:
            year_rows_dict[row_year] = [header, row]  # initialize this year with the header row
        else:
            year_rows_dict[row_year].append(row)

    print(f"File size: {len(input_list)} including header\n")
    print(f"after separating, all years: {list(year_rows_dict.keys())}\n")
    count = len(input_list) -1
    for k in year_rows_dict:
        print(f"   {k}: size {len(year_rows_dict[k])} including header row")
        count -= (len(year_rows_dict[k])-1)
        write_csv(year_rows_dict[k], f"{output_folder}{k}.csv")
    if count == 0:
        print(f"\n...check final number...\nCORRECT!")
    else:
        print(f"\n...check final number...\nWRONG! number doesnt add up")





main()


