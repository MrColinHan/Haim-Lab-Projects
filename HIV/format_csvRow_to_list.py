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

positions = "KC882681	KC882799	KC882698	KC882678	KC883209	KC882621	KC883353	MK729818	KC883323	KC882557	KC882563	KC882950	CY111166	KC883383	KC883223	KC883017	KR611836	CY111478	CY111422"
sep = re.sub("\s+",",",positions)

result = []
current_index = 0
for i in range(len(sep)):
    if sep[i] == ',':
        result.append(sep[current_index:i])
        current_index = i+1
    if i == len(sep)-1: 
        result.append(sep[current_index:])
print(result)