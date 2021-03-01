"""
Feb 26, 2021

@author: Changze Han
"""

'''
    For Crime data project: 
        this program takes the centroids output of 'centroid_and_mean_dist.py'
        give two area name as input arguments. then it calculates the parallel distance between two areas: 
            e.g. two areas A, B
                 parallel dist: 
                    2010 A  vs  2010 B
                    2011 A  vs  2011 B
                
        
'''

import csv
import math

# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/2.26.21_crime_data/"
input_filename = r"crime centroids.csv"
output_filename = "parallel_dist.csv"

area_a = "Foothill"
area_b = "Mission"#"N Hollywood"

# col index starts from 0
year_col = 1  # crime date
area_col = 2  # crime code
feature_start_col = 3  # feature starting col
# ========================================================================================================
input_file = working_dir + input_filename
output_file = working_dir + output_filename

input_list = list()
output_list = list()


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
    read_csv(input_file, input_list)
    print(f"file size : {len(input_list)}")
    area_a_list = list()
    area_b_list = list()

    for row in input_list[1:]:
        if row[area_col] == area_a:
            area_a_list.append(row)
        if row[area_col] == area_b:
            area_b_list.append(row)
    print(f"{area_a} has {len(area_a_list)} rows")
    for i in area_a_list:
        print(i)
    print(f"{area_b} has {len(area_b_list)} rows")
    for i in area_b_list:
        print(i)

    for index in range(len(area_a_list)):
        a_features = [float(x) for x in area_a_list[index][feature_start_col:]]
        print(len(a_features))
        b_features = [float(x) for x in area_b_list[index][feature_start_col:]]
        print(len(b_features))

        dist = Euclidean(a_features, b_features)

        output_list.append([area_a_list[index][area_col], area_a_list[index][year_col], 'VS'
            , area_b_list[index][area_col], area_b_list[index][year_col], dist])





    write_csv(output_list, output_file)






main()


