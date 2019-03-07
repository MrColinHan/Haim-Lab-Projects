#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 01:24:12 2019

@author: Han
"""
import re
# copy positions from excel and translated int0 [[88,88],[168,168],......]

a = "134 148 505 506"
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


