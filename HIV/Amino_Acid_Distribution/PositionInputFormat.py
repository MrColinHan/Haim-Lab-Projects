#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 01:24:12 2019

@author: Han
"""
import re
# copy positions from excel and translated int0 [[88,88],[168,168],......]
# input format '160 161 162 163 164 165'

a = '370 371 376 377 475 476'
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


