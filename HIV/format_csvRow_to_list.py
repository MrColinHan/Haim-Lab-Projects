#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 01:07:37 2019

@author: Han
"""

'''
    Translate a row copied from excel row into : 
    
        1. a list format:   ['KC882681', 'KC882799', 'KC882698']
        
        2. Chimera's command line input format : [295, 332, 339, 392]  (remember need to remove the brackets in Chimera)
'''


import re

Chimera = True
check_gly = True
positions = "688	525	89	854	259	274	134	375	315	730	148	689	9	705	270	142	143	178	724	135	362	744	140	677	137	130	787	20	620	147	309	795	387	721	46	4	816	183	340	149	767	845	379	345	818	280	494	156	781	624	150	403	145	344	346	232	356	360	550	291	163	167	177"

sep = re.sub("\s+", ",", positions)



result = []
current_index = 0
for i in range(len(sep)):
    if sep[i] == ',':
        if Chimera == True:
            result.append(int(sep[current_index:i]))
        else:
            result.append(sep[current_index:i])
        current_index = i+1
        
    if i == len(sep)-1: 
        if Chimera == True:
            result.append(int(sep[current_index:]))
        else:
            result.append(sep[current_index:])

# glycan mapping
child_position_mapping = {
    611: [1611],
    618: [1618],
    637: [1637],
    88: [1088, 1089, 1090, 1091, 1092, 1093, 1094],
    133: [1133],
    137: [1137, 1138, 1139, 1140],
    156: [1156, 1157, 1158, 1159, 1169],
    197: [1197, 1198],
    234: [1234, 1235],
    262: [1262, 1263, 1264, 1265, 1268, 1269],
    276: [1276],
    295: [1296, 1295],
    301: [1301, 1302],
    332: [1331, 1332, 1333, 1334, 1335, 1336, 1337, 1338, 1339, 1340],
    355: [1355],
    363: [1363, 1364],
    386: [1386, 1387],
    392: [1392, 1393],
    448: [1448, 1449, 1450],
    339: [1839],
    160: [1160, 1161]
}

if check_gly == True:
    for root_pos in result:
        if root_pos in child_position_mapping:
            print(f"gly:{root_pos}")
            result = result + child_position_mapping[root_pos]

print(result)
