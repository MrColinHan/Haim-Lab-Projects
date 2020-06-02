#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 11:16:05 2019

@author: Han
"""

'''
    This program convert a csv file to a fasta file. 
    
    csv file format: 
    
    | KJ704790	| M	| R	| V	| K	| E	| N | ...
    | KJ704793	| M	| R	| A	| K	| E	| N | ...
    | AY247218	| M	| R	| V	| K	| G	| N | ...
    
'''

import csv

# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/4.28.20_Germlin_co-ev/population_b_160/"
input_name = r"C_gp160_1142_noGap_noPNGS.csv"
output_name = r"C_gp160_1142_noGap_noPNGS.fasta"
# ==========================================================================================
input_file = working_dir + input_name
input_list = []
output_file = working_dir + output_name
output_list = []


def read_csv(filedir, listname):
    file = open(filedir)
    reader = csv.reader(file)
    for row in reader:
        listname.append(row)


def write(x, y):  # write the list x into y file
    output= open(y,"w+")
    for i in x:
        output.write(i)
    output.close
    
 
def main():
    global input_list
    global output_list

    read_csv(input_file, input_list)

    count_fas_output = 0  # keep track number of sequences written in the output
    for row in input_list:
        current_accession = row[0]
        current_sequence = ""
        for item in row[1:]:  # exclude accession number
            current_sequence += item
        output_list.append(f">{current_accession}\n")
        output_list.append(f"{current_sequence}\n")
        count_fas_output += 1

    print(f"Input CSV file '{input_name}' contains: {len(input_list)} sequences.")

    print(f"Output Fas file '{output_name}' contains: {count_fas_output} sequences.")
    write(output_list, output_file)



main()





