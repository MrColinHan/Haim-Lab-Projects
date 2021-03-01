"""
Feb 23, 2021

@author: Changze Han
"""

'''
    For Crime data project: 
        this program performs two tasks: 
            1. calculates the crime FD centroids for each area in each year
            2. after getting the centroid, calculate mean disct between each centroid and the points that calculated that centroid

'''

import csv
import math
import pandas as pd
import numpy as np
import datetime
import statistics
# Inputs ================================================================================================
working_dir = r"/Users/Han/MacMini_Local/HaimLab_CrimeData/"
input_filename = "FD_year_week_area_2010-2019.csv"
centroid_output_filename = "centroids.csv"
dist_output_filename = "mean_dict.csv"

# col index starts from 0
year_col = 1  # crime date
week_col = 2  # crime area
area_col = 3  # crime code
feature_start_col = 4  # feature starting col
# ========================================================================================================
input_file = working_dir + input_filename
centroid_output_file = working_dir + centroid_output_filename
dist_output_file = working_dir + dist_output_filename
input_list = list()
centroid_output_list = list()
mean_dict_output_list = list()


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


# Euclidean fomular
def Euclidean(list1,list2):
    squareSum = 0
    for i in range(len(list1)):
        squareSum = squareSum + ((float(list2[i]) - float(list1[i]))**2)
    return (math.sqrt(squareSum))


def main():
    global centroid_output_list, mean_dict_output_list, input_list

    read_csv(input_file, input_list)
    print(f"input size: {len(input_list)}")

    header = input_list[0]
    content = input_list[1:]

    yearArea_rows_dict = dict()  # key: year-area   values: rows
    for r in content:
        y_a = f"{r[year_col]}_{r[area_col]}"
        if y_a not in yearArea_rows_dict:
            yearArea_rows_dict[y_a] = [r]
        else:
            yearArea_rows_dict[y_a].append(r)


    # exclude year-area pairs that have only 1 row. also check total number to see if they add up
    clean_yearArea_rows_dict = dict()  # save keys that have value len >1

    check_count = len(content)
    for k in yearArea_rows_dict:
        print(f"{k}: ---------- {len(yearArea_rows_dict[k])} rows")
        if len(yearArea_rows_dict[k]) >1:
            clean_yearArea_rows_dict[k] = yearArea_rows_dict[k]
        check_count -= len(yearArea_rows_dict[k])
    if check_count != 0:
        raise Exception("ERROR: Total count doenst add up after yearArea dict")
    print(f"\n total year-area pairs: {len(yearArea_rows_dict)}")
    print(f"\n after cleaning up(remove pairs with len(value)=1, probably from 2020), total year-area pairs: {len(clean_yearArea_rows_dict)}")

    # start calculating centroids and average euclidean dist
    print("\n............calculating centroids and average euclidean dist...........")
    centroid_output_list.append(["# of crimes", "year", "area"] + header[feature_start_col:])
    mean_dict_output_list.append(["# of crimes", "year", "area", "mean_euclidean"])

    for y_a_key in clean_yearArea_rows_dict:
        centroid_list = list()
        vector = list()
        crime_count = 0
        for p in clean_yearArea_rows_dict[y_a_key]:
            vector.append(p[feature_start_col:])
            crime_count += int(p[0])

        for i in range(len(vector[0])):
            i_list = list()
            for v in vector:
                i_list.append(float(v[i]))
            centroid_list.append(statistics.mean(i_list))
        centroid_output_list.append([crime_count, y_a_key.split("_")[0], y_a_key.split("_")[1]] + centroid_list)

        # now calculate average dist between this centroid and the vector
        euclid_dist_list = list()
        for vv in vector:
            euclid_dist_list.append(Euclidean(centroid_list, [float(x) for x in vv]))
        mean_dict_output_list.append([crime_count, y_a_key.split("_")[0], y_a_key.split("_")[1], statistics.mean(euclid_dist_list)])



    write_csv(centroid_output_list, centroid_output_file)
    write_csv(mean_dict_output_list, dist_output_file)






main()








