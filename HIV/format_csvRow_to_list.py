#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 01:07:37 2019

@author: Han
"""

'''
    Translate a row copied from excel row into : 
    
        1. a list format:   ['KC882681', 'KC882799', 'KC882698']
        
        2. Chimera's command line input format : [295, 332, 339, 392]  (need to remove the brackets)
'''


import re

Chimera = True
check_gly = True
positions = "352	410	397	618	518	308	462	375	6	597	50	19	778	553	446	343	360	345	423	854	412	306	405	92	313	178	171	319	320	340	295	585	143	363	557	655	110	620	325	31	290	426	386	185	269	588	328	373	621	99	58	169	350	357	419	137	33	164	5	344	326	448	147	743	407	150	152	61	29	315	417	188	149	335	467	392	297	347	337	444	406	411	130	139	144	151	145	87	398	408	148	394	49	293	330	138	146	413	409	396	354	404	400	141	401	140	142"
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
