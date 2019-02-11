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

positions = "543	236	602	26	95	175	163	374	171	273	288	85	192	525	437"

print(re.sub("\s+",",",positions))
    