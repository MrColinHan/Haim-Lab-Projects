#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 13:10:55 2019

@author: Han
"""

from re import compile
import Bio
from Bio import Phylo


working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/9.25.19_new_accession/14-15_season/"                     
seq_filename = r"G.14-15_season_H1N1_USA_nwk_tree_75.txt"

input_file = working_dir + seq_filename


ACCESSION_MATCHER = compile(r'[A-Za-z]{2}\d{6}|[A-Za-z]{1}\d{5}|[A-Za-z]{3}\d{5}')


print(Bio.__version__)

tree = Phylo.read(input_file, 'newick')
print(tree)

tree.rooted = True
Phylo.draw(tree)
Phylo.draw_ascii(tree)

test = ';(((KT836475:3.0E-6,(KT836453:3.0E-6,(KT836443:3.0E-6,KT836435:3.0E-6):3.0E-6):3.0E-6):3.0E-6,(KT836531:3.0E-6,KT836476:3.0E-6):3.0E-6):3.0E-6,(KT836462:3.0E-6,(KT836709:3.0E-6,KT836520:3.0E-6):3.0E-6):3.0E-6):3.0E-6,(KT880179:3.0E-6,KT880176:6.0E-6):5.92E-4);'


def getAccessNum(string):
    #extract accession from the given string, returns the first match if there are multiple matches
    return ACCESSION_MATCHER.findall(string)

print(getAccessNum(test))