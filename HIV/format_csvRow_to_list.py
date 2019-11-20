#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 01:07:37 2019

@author: Han
"""

'''
    Translate positions copied from excel row into Chimera's command line input format
'''


import re

positions = "KU590454	KU592096	KU591140	KU592142	KX003406	KX413369	KX413331	KU591700	KU590828	KU591007	KX413665	KX413705	KX413561	KY044240	KX412630	KX412814	KX413953	KX413649	KY044247	KX412502	KX413545	KX413553	KX413737	KX413745	KX003471	KX414465"
sep = re.sub("\s+",",",positions)

result = []
current_index = 0
for i in range(len(sep)):
    if sep[i] == ',':
        result.append(sep[current_index:i])
        current_index = i+1

print(result)