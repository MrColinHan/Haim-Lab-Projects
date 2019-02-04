#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 01:24:12 2019

@author: Han
"""
import re
# copy positions from excel and translated int0 [[88,88],[168,168],......]

a = "2	166	192	273	298	304	327	456	469	480	503	504	508	511	542	557	579	585	633	696	707	709	725	729	742	744	747	761	770	772	780	828	838	845	846	848"

b = re.sub("\s+", ",", a.strip())

txtlist = b.split(",")

strToIntlist = []

for i in txtlist:
    strToIntlist.append(int(i))

FinalList = []
for i in strToIntlist:
    innerList = []
    innerList.append(i)
    innerList.append(i)
    FinalList.append(innerList)

print(FinalList)
    
