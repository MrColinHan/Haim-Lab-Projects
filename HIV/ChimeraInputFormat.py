#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 01:07:37 2019

@author: Han
"""

'''
    Translate positions copied from excel into Chimera's command line input format
'''


import re

positions = "268         65           138         122         281"

print(re.sub("\s+",",",positions))
    