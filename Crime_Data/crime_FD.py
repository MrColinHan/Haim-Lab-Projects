"""
Feb 22, 2021

@author: Changze Han
"""

'''
    For Crime data project: 
        this program calculates the crime frequency distribution for each week_day in each area

'''

import csv
import pandas as pd
import numpy as np
import datetime
# Inputs ================================================================================================
working_dir = r"/Users/Han/MacMini_Local/HaimLab_CrimeData/"
input_filename = "Crime_Data_2010-2019.csv"
output_filename = "2010-2019_FD_byYear.csv"

# col index starts from 0
date_col = 2  # crime date
area_col = 5  # crime area
cd_col = 8  # crime code

# crime code category
cd_category_dict = \
    {"Grand Theft Auto": (510, 520, 349, 446),
     "Homicide": (110, 113),
     "Rape": (122, 121),
     "Arson": (648, ),
     "Burglary": (310, 320),
     "Financial crimes": (649, 661, 653, 660, 354, 345, 654, 942, 347, 668, 670),
     "Assault": (230, 624, 625, 231, 626, 236, 622, 930, 623, 860),
     "Theft": (341, 440, 343, 441, 664, 662, 352, 351, 450, 443, 442, 480, 452, 485, 475, 487, 451, 473, 666, 474, 350),
     "Robbery": (210, 220),
     "Burglary/Theft from Vehicle": (330, 420, 410, 421, 331),
     "Vandalism": (740, 745, 924),
     "Kidnapping": (910, 920),
     "Child abuse": (235, 627, 237, 870, 922, 237, 812, 813, 922, 870, 760),
     "Weapons": (251, 753, 761),
     "Court order violations": (900, 901, 902)}
# ========================================================================================================
input_file = working_dir + input_filename
output_file = working_dir + output_filename
input_list = list()
output_list = list()
output_list.append(["# of crimes", "year", "week", "area"] + list(cd_category_dict.keys()))


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

week_rows_dict = dict()  # divide the rows by week number
def main():
    global input_list, input_file, output_folder, date_col, week_rows_dict

    read_csv(input_file, input_list)
    print(f"file size {len(input_list)} including header")

    header = input_list[0]
    content = input_list[1:]

    for row in content:
        row_yy = int(row[date_col].split()[0].split('/')[2])
        row_mm = int(row[date_col].split()[0].split('/')[0])
        row_dd = int(row[date_col].split()[0].split('/')[1])
        #print((row_mm, row_dd, row_yy))
        # isocalendar returns (year, week, weekday)
        # [0] takes the year num, [1] takes the week num, [2] takes the day num
        row_year_week = f"{datetime.date(row_yy, row_mm, row_dd).isocalendar()[0]}_" \
                        f"{datetime.date(row_yy, row_mm, row_dd).isocalendar()[1]}"
                        #f"{datetime.date(row_yy, row_mm, row_dd).isocalendar()[2]}"

        if row_year_week not in week_rows_dict:
            week_rows_dict[row_year_week] = [row]
        else:
            week_rows_dict[row_year_week].append(row)

    t_count = len(input_list)-1
    for k in week_rows_dict:
        print(f"  week {k} has {len(week_rows_dict[k])} rows data")
        t_count -= len(week_rows_dict[k])

    if t_count == 0:
        print("Week count CORRECT!")
    else:
        raise Exception(f"Week count WRONG")

    print("\n========== for each week, divide again by area, then compute FD for each area under each week=========\n")

    for wek in week_rows_dict:
        print(f"{wek}: ------{len(week_rows_dict[wek])}")
        # for this week, divide rows based on area
        area_rows_dict = dict()
        for r in week_rows_dict[wek]:
            if r[area_col] not in area_rows_dict:
                area_rows_dict[r[area_col]] = [r]
            else:
                area_rows_dict[r[area_col]].append(r)

        # compute Crime FD for each area
        for a in area_rows_dict:
            print(f"   {a}   size {len(area_rows_dict[a])}")

            # crime count dict for this area in this week
            cd_count_dict = cd_category_dict.fromkeys(cd_category_dict, 0)  # empty dict with all cd as keys

            for day in area_rows_dict[a]:  # each day record in this area

                for cd in cd_category_dict:  # go though cd category dict
                    #print(day)
                    #print(int(day[cd_col]))
                    if int(day[cd_col]) in cd_category_dict[cd]:  # match cd
                        cd_count_dict[cd] += 1
                        break

            # double check the order of crime name before writing output
            if list(cd_count_dict.keys()) == output_list[0][4:]:
                wek_area_count_list = cd_count_dict.values()
                wek_area_fd_list = [x/sum(wek_area_count_list)*100 for x in wek_area_count_list]
                output_list.append([sum(wek_area_count_list), wek.split('_')[0], wek.split('_')[1], a] + wek_area_fd_list)
            else:
                raise Exception("crime name order doesnt match header row, CHECK!!!")





    write_csv(output_list, output_file)


main()
