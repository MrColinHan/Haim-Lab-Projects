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

positions = "133	377	266	723	490	72	727	168	561	728	167	267	166	524	169	455"
print(re.sub("\s+",",",positions))
    