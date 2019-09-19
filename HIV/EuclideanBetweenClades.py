#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 15:31:33 2019

@author: Han
"""

import math 
import csv
# Inputs ================================================================================================
inputFile = r"/Users/Han/Documents/Haim_Lab(2018_summer)/8.21.19_4pos_dist/7.23.19_distance_input(clade_all).csv"

# ========================================================================================================


# Euclidean fomular
def Euclidean(list1,list2):
    squareSum = 0
    for i in range(len(list1)):
        squareSum = squareSum + ((float(list2[i]) - float(list1[i]))**2)    
    return (math.sqrt(squareSum))

# calculate distance between 137AE and 6 centroids
#                            289A1 and 6 centroids
#                            295C ...
#                            ......

csvList = []

def readCSV(filedir,listname):
    file = open(filedir)
    reader = csv.reader(file)
    for row in reader:
        listname.append(row) 
        
readCSV(inputFile,csvList)

#for i in csvList[1:]:
    #print(i[0]+i[1])

_137AE = list(map(float,csvList[1][2:]))
_289A1 = list(map(float,csvList[3][2:]))
_295C = list(map(float,csvList[5][2:]))
_332AE = list(map(float,csvList[7][2:]))
_339AE = list(map(float,csvList[9][2:]))
_398C = list(map(float,csvList[11][2:]))
non_PNGS = {'137AE':_137AE,'289A1':_289A1,'295C':_295C,'332AE':_332AE,'339AE':_339AE,'398C':_398C}

_137cen = list(map(float,csvList[2][2:]))
_289cen = list(map(float,csvList[4][2:]))
_295cen = list(map(float,csvList[6][2:]))
_332cen = list(map(float,csvList[8][2:]))
_339cen = list(map(float,csvList[10][2:]))
_398cen = list(map(float,csvList[12][2:]))
_88cen = list(map(float,csvList[13][2:]))
_156cen = list(map(float,csvList[14][2:]))
_160cen = list(map(float,csvList[15][2:]))
_197cen = list(map(float,csvList[16][2:]))
_234cen = list(map(float,csvList[17][2:]))
_241cen = list(map(float,csvList[18][2:]))
_262cen = list(map(float,csvList[19][2:]))
_276cen = list(map(float,csvList[20][2:]))
_301cen = list(map(float,csvList[21][2:]))
_356cen = list(map(float,csvList[22][2:]))
_386cen = list(map(float,csvList[23][2:]))
_392cen = list(map(float,csvList[24][2:]))
_448cen = list(map(float,csvList[25][2:]))
centroids = {'137cen':_137cen,'289cen':_289cen,'295cen':_295cen,'332cen':_332cen,'339cen':_339cen,'398cen':_398cen, 
             '88cen': _88cen, '156cen': _156cen, '160cen': _160cen, '197cen': _197cen, '234cen': _234cen, 
             '241cen': _241cen, '262cen': _262cen, '276cen': _276cen, '301cen': _301cen, '356cen': _356cen,
             '386cen': _386cen, '392cen': _392cen, '448cen': _448cen, }

#for i in non_PNGS:
    #print(non_PNGS[i][1])

#for i in centroids:
    #print(centroids[i][1])

'''for n_Z in non_PNGS:   # 0.6 cutoff
    print("")
    for cen in centroids:
        print(n_Z + " vs " + cen + " : " + str(Euclidean(non_PNGS[n_Z],centroids[cen]))) 
# 0.6 cutoff
        
_339A1 = list(map(float,csvList[26][2:]))
_339B = list(map(float,csvList[27][2:]))
_339C = list(map(float,csvList[28][2:]))
# 339AE vs 339B
print("339AE VS B "+str(Euclidean(_339AE,_339B)))
# 339AE vs 339C
print("339AE VS C "+str(Euclidean(_339AE,_339C)))
# 339AE vs 339A1
print("339AE VS A1 "+str(Euclidean(_339AE,_339A1)))
print("average: ")
print((Euclidean(_339AE,_339B) + Euclidean(_339AE,_339C) + Euclidean(_339AE,_339A1))/3)
print("compare with 339AE vs 339cen : 2.99276717271171")

print("\n")

#===============================================  # 0.6 cutoff
_332A1 = list(map(float,csvList[29][2:]))
_332B = list(map(float,csvList[30][2:]))
_332C = list(map(float,csvList[31][2:]))
# 332AE vs 332B
print("332AE VS B "+str(Euclidean(_332AE,_332B)))
# 332AE vs 332C
print("332AE VS C "+str(Euclidean(_332AE,_332C)))
# 332AE vs 332A1
print("332AE VS A1 "+str(Euclidean(_332AE,_332A1)))
print("average: ")
print((Euclidean(_332AE,_332B) + Euclidean(_332AE,_332C) + Euclidean(_332AE,_332A1))/3)
print("compare with 332AE vs 332cen : 4.235169506770827")
print("\n")


#=============================================== 339:B VS AE  0.6 cutoff
B_339_1979_1986 = list(map(float,csvList[54][2:]))
B_339_1987_1994 = list(map(float,csvList[55][2:]))
B_339_1995_1999 = list(map(float,csvList[56][2:]))
B_339_2000_2004 = list(map(float,csvList[57][2:]))
B_339_2005_2009 = list(map(float,csvList[58][2:]))
B_339_2010_2015 = list(map(float,csvList[59][2:]))

AE_339_1986_1994 = list(map(float,csvList[60][2:]))
AE_339_1995_1999 = list(map(float,csvList[61][2:]))
AE_339_2000_2004 = list(map(float,csvList[62][2:]))
AE_339_2005_2007 = list(map(float,csvList[63][2:]))
AE_339_2008_2015 = list(map(float,csvList[64][2:]))

print("339:B VS AE  0.6 cutoff: ")
print("B_339_1987_1994 VS AE_339_1986_1994: " +str(Euclidean(B_339_1987_1994,AE_339_1986_1994)))
print("B_339_1995_1999 VS AE_339_1995_1999: " +str(Euclidean(B_339_1995_1999,AE_339_1995_1999)))
print("B_339_2000_2004 VS AE_339_2000_2004: " +str(Euclidean(B_339_2000_2004,AE_339_2000_2004)))
print("B_339_2005_2009 VS AE_339_2005_2007: " +str(Euclidean(B_339_2005_2009,AE_339_2005_2007)))
print("B_339_2010_2015 VS AE_339_2008_2015: " +str(Euclidean(B_339_2010_2015,AE_339_2008_2015)))
print("\n")
'''
#=============================================== 169:B(no KR,CN) VS C(no INNP,BR) 0.75 cutoff

B_169_1979_1986 = list(map(float,csvList[32][2:]))
B_169_1987_1994 = list(map(float,csvList[33][2:]))
B_169_1995_1999 = list(map(float,csvList[34][2:]))
B_169_2000_2004 = list(map(float,csvList[35][2:]))
B_169_2005_2009 = list(map(float,csvList[36][2:]))
B_169_2010_2015 = list(map(float,csvList[37][2:]))

C_169_1986_1994 = list(map(float,csvList[38][2:]))
C_169_1995_1999 = list(map(float,csvList[39][2:]))
C_169_2000_2004 = list(map(float,csvList[40][2:]))
C_169_2005_2009 = list(map(float,csvList[41][2:]))
C_169_2010_2015 = list(map(float,csvList[42][2:]))

print("169 B(no KR,CN) VS C(no INNP,BR) 0.75 cutoff: ")
print("*** B_169_1979_1986 VS C_169_1986_1994: " +str(Euclidean(B_169_1979_1986,C_169_1986_1994)))
print("B_169_1987_1994 VS C_169_1986_1994: " +str(Euclidean(B_169_1987_1994,C_169_1986_1994)))
print("B_169_1995_1999 VS C_169_1995_1999: " +str(Euclidean(B_169_1995_1999,C_169_1995_1999)))
print("B_169_2000_2004 VS C_169_2000_2004: " +str(Euclidean(B_169_2000_2004,C_169_2000_2004)))
print("B_169_2005_2009 VS C_169_2005_2009: " +str(Euclidean(B_169_2005_2009,C_169_2005_2009)))
print("B_169_2010_2015 VS C_169_2010_2015: " +str(Euclidean(B_169_2010_2015,C_169_2010_2015)))
print("\n")


#=============================================== 181:B(no KR,CN) VS C(no INNP,BR) 0.75 cutoff
B_181_1979_1986 = list(map(float,csvList[43][2:]))
B_181_1987_1994 = list(map(float,csvList[44][2:]))
B_181_1995_1999 = list(map(float,csvList[45][2:]))
B_181_2000_2004 = list(map(float,csvList[46][2:]))
B_181_2005_2009 = list(map(float,csvList[47][2:]))
B_181_2010_2015 = list(map(float,csvList[48][2:]))

C_181_1986_1994 = list(map(float,csvList[49][2:]))
C_181_1995_1999 = list(map(float,csvList[50][2:]))
C_181_2000_2004 = list(map(float,csvList[51][2:]))
C_181_2005_2009 = list(map(float,csvList[52][2:]))
C_181_2010_2015 = list(map(float,csvList[53][2:]))

print("181:B(no KR,CN) VS C(no INNP,BR) 0.75 cutoff: ")
print("*** B_181_1979_1986 VS C_181_1986_1994: " +str(Euclidean(B_181_1979_1986,C_181_1986_1994)))
print("B_181_1987_1994 VS C_181_1986_1994: " +str(Euclidean(B_181_1987_1994,C_181_1986_1994)))
print("B_181_1995_1999 VS C_181_1995_1999: " +str(Euclidean(B_181_1995_1999,C_181_1995_1999)))
print("B_181_2000_2004 VS C_181_2000_2004: " +str(Euclidean(B_181_2000_2004,C_181_2000_2004)))
print("B_181_2005_2009 VS C_181_2005_2009: " +str(Euclidean(B_181_2005_2009,C_181_2005_2009)))
print("B_181_2010_2015 VS C_181_2010_2015: " +str(Euclidean(B_181_2010_2015,C_181_2010_2015)))
print("\n")

#=============================================== 295:B(no KR,CN) VS C(no INNP,BR) 0.75 cutoff
B_295_1979_1986 = list(map(float,csvList[65][2:]))
B_295_1987_1994 = list(map(float,csvList[66][2:]))
B_295_1995_1999 = list(map(float,csvList[67][2:]))
B_295_2000_2004 = list(map(float,csvList[68][2:]))
B_295_2005_2009 = list(map(float,csvList[69][2:]))
B_295_2010_2015 = list(map(float,csvList[70][2:]))

C_295_1986_1994 = list(map(float,csvList[71][2:]))
C_295_1995_1999 = list(map(float,csvList[72][2:]))
C_295_2000_2004 = list(map(float,csvList[73][2:]))
C_295_2005_2009 = list(map(float,csvList[74][2:]))
C_295_2010_2015 = list(map(float,csvList[75][2:]))

print("295:B(no KR,CN) VS C(no INNP,BR) 0.75 cutoff: ")
print("*** B_295_1979_1986 VS C_295_1986_1994: " +str(Euclidean(B_295_1979_1986,C_295_1986_1994)))
print("B_295_1987_1994 VS C_295_1986_1994: " +str(Euclidean(B_295_1987_1994,C_295_1986_1994)))
print("B_295_1995_1999 VS C_295_1995_1999: " +str(Euclidean(B_295_1995_1999,C_295_1995_1999)))
print("B_295_2000_2004 VS C_295_2000_2004: " +str(Euclidean(B_295_2000_2004,C_295_2000_2004)))
print("B_295_2005_2009 VS C_295_2005_2009: " +str(Euclidean(B_295_2005_2009,C_295_2005_2009)))
print("B_295_2010_2015 VS C_295_2010_2015: " +str(Euclidean(B_295_2010_2015,C_295_2010_2015)))
print("\n")

#=============================================== 289:B(no KR,CN) VS C(no INNP,BR) 0.75 cutoff
B_289_1979_1986 = list(map(float,csvList[76][2:]))
B_289_1987_1994 = list(map(float,csvList[77][2:]))
B_289_1995_1999 = list(map(float,csvList[78][2:]))
B_289_2000_2004 = list(map(float,csvList[79][2:]))
B_289_2005_2009 = list(map(float,csvList[80][2:]))
B_289_2010_2015 = list(map(float,csvList[81][2:]))

C_289_1986_1994 = list(map(float,csvList[82][2:]))
C_289_1995_1999 = list(map(float,csvList[83][2:]))
C_289_2000_2004 = list(map(float,csvList[84][2:]))
C_289_2005_2009 = list(map(float,csvList[85][2:]))
C_289_2010_2015 = list(map(float,csvList[86][2:]))

print("289:B(no KR,CN) VS C(no INNP,BR) 0.75 cutoff:  ")
print("*** B_289_1979_1986 VS C_289_1986_1994: " +str(Euclidean(B_289_1979_1986,C_289_1986_1994)))
print("B_289_1987_1994 VS C_289_1986_1994: " +str(Euclidean(B_289_1987_1994,C_289_1986_1994)))
print("B_289_1995_1999 VS C_289_1995_1999: " +str(Euclidean(B_289_1995_1999,C_289_1995_1999)))
print("B_289_2000_2004 VS C_289_2000_2004: " +str(Euclidean(B_289_2000_2004,C_289_2000_2004)))
print("B_289_2005_2009 VS C_289_2005_2009: " +str(Euclidean(B_289_2005_2009,C_289_2005_2009)))
print("B_289_2010_2015 VS C_289_2010_2015: " +str(Euclidean(B_289_2010_2015,C_289_2010_2015)))
print("\n")


#=============================================== 332:B(no KR,CN) VS C(no INNP,BR) 0.75 cutoff
B_332_1979_1986 = list(map(float,csvList[87][2:]))
B_332_1987_1994 = list(map(float,csvList[88][2:]))
B_332_1995_1999 = list(map(float,csvList[89][2:]))
B_332_2000_2004 = list(map(float,csvList[90][2:]))
B_332_2005_2009 = list(map(float,csvList[91][2:]))
B_332_2010_2015 = list(map(float,csvList[92][2:]))

C_332_1986_1994 = list(map(float,csvList[93][2:]))
C_332_1995_1999 = list(map(float,csvList[94][2:]))
C_332_2000_2004 = list(map(float,csvList[95][2:]))
C_332_2005_2009 = list(map(float,csvList[96][2:]))
C_332_2010_2015 = list(map(float,csvList[97][2:]))

print("332:B(no KR,CN) VS C(no INNP,BR) 0.75 cutoff:  ")
print("*** B_332_1979_1986 VS C_332_1986_1994: " +str(Euclidean(B_332_1979_1986,C_332_1986_1994)))
print("B_332_1987_1994 VS C_332_1986_1994: " +str(Euclidean(B_332_1987_1994,C_332_1986_1994)))
print("B_332_1995_1999 VS C_332_1995_1999: " +str(Euclidean(B_332_1995_1999,C_332_1995_1999)))
print("B_332_2000_2004 VS C_332_2000_2004: " +str(Euclidean(B_332_2000_2004,C_332_2000_2004)))
print("B_332_2005_2009 VS C_332_2005_2009: " +str(Euclidean(B_332_2005_2009,C_332_2005_2009)))
print("B_332_2010_2015 VS C_332_2010_2015: " +str(Euclidean(B_332_2010_2015,C_332_2010_2015)))
print("\n")

#=============================================== 339:B(no KR,CN) VS C(no INNP,BR) 0.75 cutoff
B_339_1979_1986 = list(map(float,csvList[98][2:]))
B_339_1987_1994 = list(map(float,csvList[99][2:]))
B_339_1995_1999 = list(map(float,csvList[100][2:]))
B_339_2000_2004 = list(map(float,csvList[101][2:]))
B_339_2005_2009 = list(map(float,csvList[102][2:]))
B_339_2010_2015 = list(map(float,csvList[103][2:]))

C_339_1986_1994 = list(map(float,csvList[104][2:]))
C_339_1995_1999 = list(map(float,csvList[105][2:]))
C_339_2000_2004 = list(map(float,csvList[106][2:]))
C_339_2005_2009 = list(map(float,csvList[107][2:]))
C_339_2010_2015 = list(map(float,csvList[108][2:]))

print("339:B(no KR,CN) VS C(no INNP,BR) 0.75 cutoff:  ")
print("*** B_339_1979_1986 VS C_339_1986_1994: " +str(Euclidean(B_339_1979_1986,C_339_1986_1994)))
print("B_339_1987_1994 VS C_339_1986_1994: " +str(Euclidean(B_339_1987_1994,C_339_1986_1994)))
print("B_339_1995_1999 VS C_339_1995_1999: " +str(Euclidean(B_339_1995_1999,C_339_1995_1999)))
print("B_339_2000_2004 VS C_339_2000_2004: " +str(Euclidean(B_339_2000_2004,C_339_2000_2004)))
print("B_339_2005_2009 VS C_339_2005_2009: " +str(Euclidean(B_339_2005_2009,C_339_2005_2009)))
print("B_339_2010_2015 VS C_339_2010_2015: " +str(Euclidean(B_339_2010_2015,C_339_2010_2015)))
print("\n")

#=============================================== 386:B(no KR,CN) VS C(no INNP,BR) 0.75 cutoff
B_386_1979_1986 = list(map(float,csvList[109][2:]))
B_386_1987_1994 = list(map(float,csvList[110][2:]))
B_386_1995_1999 = list(map(float,csvList[111][2:]))
B_386_2000_2004 = list(map(float,csvList[112][2:]))
B_386_2005_2009 = list(map(float,csvList[113][2:]))
B_386_2010_2015 = list(map(float,csvList[114][2:]))

C_386_1986_1994 = list(map(float,csvList[115][2:]))
C_386_1995_1999 = list(map(float,csvList[116][2:]))
C_386_2000_2004 = list(map(float,csvList[117][2:]))
C_386_2005_2009 = list(map(float,csvList[118][2:]))
C_386_2010_2015 = list(map(float,csvList[119][2:]))

print("386:B(no KR,CN) VS C(no INNP,BR) 0.75 cutoff:  ")
print("*** B_386_1979_1986 VS C_386_1986_1994: " +str(Euclidean(B_386_1979_1986,C_386_1986_1994)))
print("B_386_1987_1994 VS C_386_1986_1994: " +str(Euclidean(B_386_1987_1994,C_386_1986_1994)))
print("B_386_1995_1999 VS C_386_1995_1999: " +str(Euclidean(B_386_1995_1999,C_386_1995_1999)))
print("B_386_2000_2004 VS C_386_2000_2004: " +str(Euclidean(B_386_2000_2004,C_386_2000_2004)))
print("B_386_2005_2009 VS C_386_2005_2009: " +str(Euclidean(B_386_2005_2009,C_386_2005_2009)))
print("B_386_2010_2015 VS C_386_2010_2015: " +str(Euclidean(B_386_2010_2015,C_386_2010_2015)))
print("\n")

#=============================================== 392:B(no KR,CN) VS C(no INNP,BR) 0.75 cutoff
B_392_1979_1986 = list(map(float,csvList[120][2:]))
B_392_1987_1994 = list(map(float,csvList[121][2:]))
B_392_1995_1999 = list(map(float,csvList[122][2:]))
B_392_2000_2004 = list(map(float,csvList[123][2:]))
B_392_2005_2009 = list(map(float,csvList[124][2:]))
B_392_2010_2015 = list(map(float,csvList[125][2:]))

C_392_1986_1994 = list(map(float,csvList[126][2:]))
C_392_1995_1999 = list(map(float,csvList[127][2:]))
C_392_2000_2004 = list(map(float,csvList[128][2:]))
C_392_2005_2009 = list(map(float,csvList[129][2:]))
C_392_2010_2015 = list(map(float,csvList[130][2:]))

print("392:B(no KR,CN) VS C(no INNP,BR) 0.75 cutoff:  ")
print("*** B_392_1979_1986 VS C_392_1986_1994: " +str(Euclidean(B_392_1979_1986,C_392_1986_1994)))
print("B_392_1987_1994 VS C_392_1986_1994: " +str(Euclidean(B_392_1987_1994,C_392_1986_1994)))
print("B_392_1995_1999 VS C_392_1995_1999: " +str(Euclidean(B_392_1995_1999,C_392_1995_1999)))
print("B_392_2000_2004 VS C_392_2000_2004: " +str(Euclidean(B_392_2000_2004,C_392_2000_2004)))
print("B_392_2005_2009 VS C_392_2005_2009: " +str(Euclidean(B_392_2005_2009,C_392_2005_2009)))
print("B_392_2010_2015 VS C_392_2010_2015: " +str(Euclidean(B_392_2010_2015,C_392_2010_2015)))
print("\n")
'''
#=============================================== 0.75 cutoff
print("B_169_1979_1986 VS C_169_1986_1994  0.75 cutoff: " +str(Euclidean(B_169_1979_1986,C_169_1986_1994)))
print("\n")
print("B_181_1979_1986 VS C_181_1986_1994  0.75 cutoff: " +str(Euclidean(B_181_1979_1986,C_181_1986_1994)))
print("\n")
print("B_289_1979_1986 VS C_289_1986_1994  0.75 cutoff: " +str(Euclidean(B_289_1979_1986,C_289_1986_1994)))
print("\n")
print("B_295_1979_1986 VS C_295_1986_1994  0.75 cutoff: " +str(Euclidean(B_295_1979_1986,C_295_1986_1994)))
print("\n")
print("B_332_1979_1986 VS C_332_1986_1994  0.75 cutoff: " +str(Euclidean(B_332_1979_1986,C_332_1986_1994)))
print("\n")
print("B_339_1979_1986 VS C_339_1986_1994  0.75 cutoff: " +str(Euclidean(B_339_1979_1986,C_339_1986_1994)))
print("\n")
print("B_386_1979_1986 VS C_386_1986_1994  0.75 cutoff: " +str(Euclidean(B_386_1979_1986,C_386_1986_1994)))
print("\n")
print("B_392_1979_1986 VS C_392_1986_1994  0.75 cutoff: " +str(Euclidean(B_392_1979_1986,C_392_1986_1994)))
print("\n")

#=============================================== 07-15 0.75 cutoff

B_169_2007_2015 = list(map(float,csvList[131][2:]))
C_169_2007_2015 = list(map(float,csvList[132][2:]))
#print("169:B (07-15) VS C (07-15) 0.75 cutoff:  ")
print("B_169_2007_2015 VS C_169_2007_2015  0.75 cutoff: " +str(Euclidean(B_169_2007_2015,C_169_2007_2015)))
print("\n")

B_181_2007_2015 = list(map(float,csvList[133][2:]))
C_181_2007_2015 = list(map(float,csvList[134][2:]))
#print("181:B (07-15) VS C (07-15) 0.75 cutoff:  ")
print("B_181_2007_2015 VS C_181_2007_2015  0.75 cutoff: " +str(Euclidean(B_181_2007_2015,C_181_2007_2015)))
print("\n")

B_289_2007_2015 = list(map(float,csvList[135][2:]))
C_289_2007_2015 = list(map(float,csvList[136][2:]))
#print("289:B (07-15) VS C (07-15) 0.75 cutoff:  ")
print("B_289_2007_2015 VS C_289_2007_2015  0.75 cutoff: " +str(Euclidean(B_289_2007_2015,C_289_2007_2015)))
print("\n")

B_295_2007_2015 = list(map(float,csvList[137][2:]))
C_295_2007_2015 = list(map(float,csvList[138][2:]))
#print("295:B (07-15) VS C (07-15) 0.75 cutoff:  ")
print("B_295_2007_2015 VS C_295_2007_2015  0.75 cutoff: " +str(Euclidean(B_295_2007_2015,C_295_2007_2015)))
print("\n")

B_332_2007_2015 = list(map(float,csvList[139][2:]))
C_332_2007_2015 = list(map(float,csvList[140][2:]))
#print("332:B (07-15) VS C (07-15) 0.75 cutoff:  ")
print("B_332_2007_2015 VS C_332_2007_2015  0.75 cutoff: " +str(Euclidean(B_332_2007_2015,C_332_2007_2015)))
print("\n")

B_339_2007_2015 = list(map(float,csvList[141][2:]))
C_339_2007_2015 = list(map(float,csvList[142][2:]))
#print("339:B (07-15) VS C (07-15) 0.75 cutoff:  ")
print("B_339_2007_2015 VS C_339_2007_2015  0.75 cutoff: " +str(Euclidean(B_339_2007_2015,C_339_2007_2015)))
print("\n")

B_386_2007_2015 = list(map(float,csvList[143][2:]))
C_386_2007_2015 = list(map(float,csvList[144][2:]))
#print("386:B (07-15) VS C (07-15) 0.75 cutoff:  ")
print("B_386_2007_2015 VS C_386_2007_2015  0.75 cutoff: " +str(Euclidean(B_386_2007_2015,C_386_2007_2015)))
print("\n")

B_392_2007_2015 = list(map(float,csvList[145][2:]))
C_392_2007_2015 = list(map(float,csvList[146][2:]))
#print("392:B (07-15) VS C (07-15) 0.75 cutoff:  ")
print("B_392_2007_2015 VS C_392_2007_2015  0.75 cutoff: " +str(Euclidean(B_392_2007_2015,C_392_2007_2015)))
print("\n")
'''

#print("=================  7.28.19 ================= " + "\n")
#=============================================== 164:B(no KR,CN) VS C(no INNP,BR) 0.75 cutoff
B_164_1979_1986 = list(map(float,csvList[147][2:]))
B_164_1987_1994 = list(map(float,csvList[148][2:]))
B_164_1995_1999 = list(map(float,csvList[149][2:]))
B_164_2000_2004 = list(map(float,csvList[150][2:]))
B_164_2005_2009 = list(map(float,csvList[151][2:]))
B_164_2010_2015 = list(map(float,csvList[152][2:]))

C_164_1986_1994 = list(map(float,csvList[153][2:]))
C_164_1995_1999 = list(map(float,csvList[154][2:]))
C_164_2000_2004 = list(map(float,csvList[155][2:]))
C_164_2005_2009 = list(map(float,csvList[156][2:]))
C_164_2010_2015 = list(map(float,csvList[157][2:]))

print("164:B(no KR,CN) VS C(no INNP,BR) 0.75 cutoff:  ")
print("*** B_164_1979_1986 VS C_164_1986_1994: " +str(Euclidean(B_164_1979_1986,C_164_1986_1994)))
print("B_164_1987_1994 VS C_164_1986_1994: " +str(Euclidean(B_164_1987_1994,C_164_1986_1994)))
print("B_164_1995_1999 VS C_164_1995_1999: " +str(Euclidean(B_164_1995_1999,C_164_1995_1999)))
print("B_164_2000_2004 VS C_164_2000_2004: " +str(Euclidean(B_164_2000_2004,C_164_2000_2004)))
print("B_164_2005_2009 VS C_164_2005_2009: " +str(Euclidean(B_164_2005_2009,C_164_2005_2009)))
print("B_164_2010_2015 VS C_164_2010_2015: " +str(Euclidean(B_164_2010_2015,C_164_2010_2015)))
print("\n")


#=============================================== 165:B(no KR,CN) VS C(no INNP,BR) 0.75 cutoff
B_165_1979_1986 = list(map(float,csvList[158][2:]))
B_165_1987_1994 = list(map(float,csvList[159][2:]))
B_165_1995_1999 = list(map(float,csvList[160][2:]))
B_165_2000_2004 = list(map(float,csvList[161][2:]))
B_165_2005_2009 = list(map(float,csvList[162][2:]))
B_165_2010_2015 = list(map(float,csvList[163][2:]))

C_165_1986_1994 = list(map(float,csvList[164][2:]))
C_165_1995_1999 = list(map(float,csvList[165][2:]))
C_165_2000_2004 = list(map(float,csvList[166][2:]))
C_165_2005_2009 = list(map(float,csvList[167][2:]))
C_165_2010_2015 = list(map(float,csvList[168][2:]))

print("165:B(no KR,CN) VS C(no INNP,BR) 0.75 cutoff:  ")
print("*** B_165_1979_1986 VS C_165_1986_1994: " +str(Euclidean(B_165_1979_1986,C_165_1986_1994)))
print("B_165_1987_1994 VS C_165_1986_1994: " +str(Euclidean(B_165_1987_1994,C_165_1986_1994)))
print("B_165_1995_1999 VS C_165_1995_1999: " +str(Euclidean(B_165_1995_1999,C_165_1995_1999)))
print("B_165_2000_2004 VS C_165_2000_2004: " +str(Euclidean(B_165_2000_2004,C_165_2000_2004)))
print("B_165_2005_2009 VS C_165_2005_2009: " +str(Euclidean(B_165_2005_2009,C_165_2005_2009)))
print("B_165_2010_2015 VS C_165_2010_2015: " +str(Euclidean(B_165_2010_2015,C_165_2010_2015)))
print("\n")

#=============================================== 172:B(no KR,CN) VS C(no INNP,BR) 0.75 cutoff
B_172_1979_1986 = list(map(float,csvList[169][2:]))
B_172_1987_1994 = list(map(float,csvList[170][2:]))
B_172_1995_1999 = list(map(float,csvList[171][2:]))
B_172_2000_2004 = list(map(float,csvList[172][2:]))
B_172_2005_2009 = list(map(float,csvList[173][2:]))
B_172_2010_2015 = list(map(float,csvList[174][2:]))

C_172_1986_1994 = list(map(float,csvList[175][2:]))
C_172_1995_1999 = list(map(float,csvList[176][2:]))
C_172_2000_2004 = list(map(float,csvList[177][2:]))
C_172_2005_2009 = list(map(float,csvList[178][2:]))
C_172_2010_2015 = list(map(float,csvList[179][2:]))

print("172:B(no KR,CN) VS C(no INNP,BR) 0.75 cutoff:  ")
print("*** B_172_1979_1986 VS C_172_1986_1994: " +str(Euclidean(B_172_1979_1986,C_172_1986_1994)))
print("B_172_1987_1994 VS C_172_1986_1994: " +str(Euclidean(B_172_1987_1994,C_172_1986_1994)))
print("B_172_1995_1999 VS C_172_1995_1999: " +str(Euclidean(B_172_1995_1999,C_172_1995_1999)))
print("B_172_2000_2004 VS C_172_2000_2004: " +str(Euclidean(B_172_2000_2004,C_172_2000_2004)))
print("B_172_2005_2009 VS C_172_2005_2009: " +str(Euclidean(B_172_2005_2009,C_172_2005_2009)))
print("B_172_2010_2015 VS C_172_2010_2015: " +str(Euclidean(B_172_2010_2015,C_172_2010_2015)))
print("\n")


#=============================================== 178:B(no KR,CN) VS C(no INNP,BR) 0.75 cutoff
B_178_1979_1986 = list(map(float,csvList[180][2:]))
B_178_1987_1994 = list(map(float,csvList[181][2:]))
B_178_1995_1999 = list(map(float,csvList[182][2:]))
B_178_2000_2004 = list(map(float,csvList[183][2:]))
B_178_2005_2009 = list(map(float,csvList[184][2:]))
B_178_2010_2015 = list(map(float,csvList[185][2:]))

C_178_1986_1994 = list(map(float,csvList[186][2:]))
C_178_1995_1999 = list(map(float,csvList[187][2:]))
C_178_2000_2004 = list(map(float,csvList[188][2:]))
C_178_2005_2009 = list(map(float,csvList[189][2:]))
C_178_2010_2015 = list(map(float,csvList[190][2:]))

print("178:B(no KR,CN) VS C(no INNP,BR) 0.75 cutoff:  ")
print("*** B_178_1979_1986 VS C_178_1986_1994: " +str(Euclidean(B_178_1979_1986,C_178_1986_1994)))
print("B_178_1987_1994 VS C_178_1986_1994: " +str(Euclidean(B_178_1987_1994,C_178_1986_1994)))
print("B_178_1995_1999 VS C_178_1995_1999: " +str(Euclidean(B_178_1995_1999,C_178_1995_1999)))
print("B_178_2000_2004 VS C_178_2000_2004: " +str(Euclidean(B_178_2000_2004,C_178_2000_2004)))
print("B_178_2005_2009 VS C_178_2005_2009: " +str(Euclidean(B_178_2005_2009,C_178_2005_2009)))
print("B_178_2010_2015 VS C_178_2010_2015: " +str(Euclidean(B_178_2010_2015,C_178_2010_2015)))
print("\n")


#=============================================== 184:B(no KR,CN) VS C(no INNP,BR) 0.75 cutoff
B_184_1979_1986 = list(map(float,csvList[191][2:]))
B_184_1987_1994 = list(map(float,csvList[192][2:]))
B_184_1995_1999 = list(map(float,csvList[193][2:]))
B_184_2000_2004 = list(map(float,csvList[194][2:]))
B_184_2005_2009 = list(map(float,csvList[195][2:]))
B_184_2010_2015 = list(map(float,csvList[196][2:]))

C_184_1986_1994 = list(map(float,csvList[197][2:]))
C_184_1995_1999 = list(map(float,csvList[198][2:]))
C_184_2000_2004 = list(map(float,csvList[199][2:]))
C_184_2005_2009 = list(map(float,csvList[200][2:]))
C_184_2010_2015 = list(map(float,csvList[201][2:]))

print("184:B(no KR,CN) VS C(no INNP,BR) 0.75 cutoff:  ")
print("*** B_184_1979_1986 VS C_184_1986_1994: " +str(Euclidean(B_184_1979_1986,C_184_1986_1994)))
print("B_184_1987_1994 VS C_184_1986_1994: " +str(Euclidean(B_184_1987_1994,C_184_1986_1994)))
print("B_184_1995_1999 VS C_184_1995_1999: " +str(Euclidean(B_184_1995_1999,C_184_1995_1999)))
print("B_184_2000_2004 VS C_184_2000_2004: " +str(Euclidean(B_184_2000_2004,C_184_2000_2004)))
print("B_184_2005_2009 VS C_184_2005_2009: " +str(Euclidean(B_184_2005_2009,C_184_2005_2009)))
print("B_184_2010_2015 VS C_184_2010_2015: " +str(Euclidean(B_184_2010_2015,C_184_2010_2015)))
print("\n")


#=============================================== 289(clade all): B VS A1 
B_289_1979_1986 = list(map(float,csvList[202][2:]))
B_289_1987_1994 = list(map(float,csvList[203][2:]))
B_289_1995_1999 = list(map(float,csvList[204][2:]))
B_289_2000_2004 = list(map(float,csvList[205][2:]))
B_289_2005_2009 = list(map(float,csvList[206][2:]))
B_289_2010_2015 = list(map(float,csvList[207][2:]))

A1_289_1986_1994 = list(map(float,csvList[208][2:]))
A1_289_1995_1999 = list(map(float,csvList[209][2:]))
A1_289_2000_2004 = list(map(float,csvList[210][2:]))
A1_289_2005_2009 = list(map(float,csvList[211][2:]))
A1_289_2010_2015 = list(map(float,csvList[212][2:]))

print("289: B VS A1 0.75 cutoff:  ")
print(f"***B_289_1979_1986 VS A1_289_1986_1994: {Euclidean(B_289_1979_1986,A1_289_1986_1994)}")
print(f"B_289_1987_1994 VS A1_289_1986_1994: {Euclidean(B_289_1987_1994,A1_289_1986_1994)}")
print(f"B_289_1995_1999 VS A1_289_1995_1999: {Euclidean(B_289_1995_1999,A1_289_1995_1999)}")
print(f"B_289_2000_2004 VS A1_289_2000_2004: {Euclidean(B_289_2000_2004,A1_289_2000_2004)}")
print(f"B_289_2005_2009 VS A1_289_2005_2009: {Euclidean(B_289_2005_2009,A1_289_2005_2009)}")
print(f"B_289_2010_2015 VS A1_289_2010_2015: {Euclidean(B_289_2010_2015,A1_289_2010_2015)}")

#=============================================== 295(clade all): C VS B 
C_295_1986_1994 = list(map(float,csvList[213][2:]))
C_295_1995_1999 = list(map(float,csvList[214][2:]))
C_295_2000_2004 = list(map(float,csvList[215][2:]))
C_295_2005_2009 = list(map(float,csvList[216][2:]))
C_295_2010_2015 = list(map(float,csvList[217][2:]))

B_295_1979_1986 = list(map(float,csvList[218][2:]))
B_295_1987_1994 = list(map(float,csvList[219][2:]))
B_295_1995_1999 = list(map(float,csvList[220][2:]))
B_295_2000_2004 = list(map(float,csvList[221][2:]))
B_295_2005_2009 = list(map(float,csvList[222][2:]))
B_295_2010_2015 = list(map(float,csvList[223][2:]))

print("295: C VS B 0.75 cutoff:  ")
print(f"***C_295_1986_1994 VS B_295_1979_1986: {Euclidean(C_295_1986_1994,B_295_1979_1986)}")
print(f"C_295_1986_1994 VS B_295_1987_1994: {Euclidean(C_295_1986_1994,B_295_1987_1994)}")
print(f"C_295_1995_1999 VS B_295_1995_1999: {Euclidean(C_295_1995_1999,B_295_1995_1999)}")
print(f"C_295_2000_2004 VS B_295_2000_2004: {Euclidean(C_295_2000_2004,B_295_2000_2004)}")
print(f"C_295_2005_2009 VS B_295_2005_2009: {Euclidean(C_295_2005_2009,B_295_2005_2009)}")
print(f"C_295_2010_2015 VS B_295_2010_2015: {Euclidean(C_295_2010_2015,B_295_2010_2015)}")
#=============================================== 332(clade all): AE VS B 
AE_332_1986_1994 = list(map(float,csvList[224][2:]))
AE_332_1995_1999 = list(map(float,csvList[225][2:]))
AE_332_2000_2004 = list(map(float,csvList[226][2:]))
AE_332_2005_2007 = list(map(float,csvList[227][2:]))
AE_332_2008_2015 = list(map(float,csvList[228][2:]))

B_332_1979_1986 = list(map(float,csvList[229][2:]))
B_332_1987_1994 = list(map(float,csvList[230][2:]))
B_332_1995_1999 = list(map(float,csvList[231][2:]))
B_332_2000_2004 = list(map(float,csvList[232][2:]))
B_332_2005_2009 = list(map(float,csvList[233][2:]))
B_332_2010_2015 = list(map(float,csvList[234][2:]))

print("332: AE VS B 0.75 cutoff:  ")
print(f"***AE_332_1986_1994 VS B_332_1979_1986: {Euclidean(AE_332_1986_1994,B_332_1979_1986)}")
print(f"AE_332_1986_1994 VS B_332_1987_1994: {Euclidean(AE_332_1986_1994,B_332_1987_1994)}")
print(f"AE_332_1995_1999 VS B_332_1995_1999: {Euclidean(AE_332_1995_1999,B_332_1995_1999)}")
print(f"AE_332_2000_2004 VS B_332_2000_2004: {Euclidean(AE_332_2000_2004,B_332_2000_2004)}")
print(f"AE_332_2005_2007 VS B_332_2005_2009: {Euclidean(AE_332_2005_2007,B_332_2005_2009)}")
print(f"AE_332_2008_2015 VS B_332_2010_2015: {Euclidean(AE_332_2008_2015,B_332_2010_2015)}")
#=============================================== 339(clade all): AE VS B
AE_339_1986_1994 = list(map(float,csvList[235][2:]))
AE_339_1995_1999 = list(map(float,csvList[236][2:]))
AE_339_2000_2004 = list(map(float,csvList[237][2:]))
AE_339_2005_2007 = list(map(float,csvList[238][2:]))
AE_339_2008_2015 = list(map(float,csvList[239][2:]))

B_339_1979_1986 = list(map(float,csvList[240][2:]))
B_339_1987_1994 = list(map(float,csvList[241][2:]))
B_339_1995_1999 = list(map(float,csvList[242][2:]))
B_339_2000_2004 = list(map(float,csvList[243][2:]))
B_339_2005_2009 = list(map(float,csvList[244][2:]))
B_339_2010_2015 = list(map(float,csvList[245][2:]))

print("339: AE VS B 0.75 cutoff:  ")
print(f"***AE_339_1986_1994 VS B_339_1979_1986: {Euclidean(AE_339_1986_1994,B_339_1979_1986)}")
print(f"AE_339_1986_1994 VS B_339_1987_1994: {Euclidean(AE_339_1986_1994,B_339_1987_1994)}")
print(f"AE_339_1995_1999 VS B_339_1995_1999: {Euclidean(AE_339_1995_1999,B_339_1995_1999)}")
print(f"AE_339_2000_2004 VS B_339_2000_2004: {Euclidean(AE_339_2000_2004,B_339_2000_2004)}")
print(f"AE_339_2005_2007 VS B_339_2005_2009: {Euclidean(AE_339_2005_2007,B_339_2005_2009)}")
print(f"AE_339_2008_2015 VS B_339_2010_2015: {Euclidean(AE_339_2008_2015,B_339_2010_2015)}")

'''
_289cen = list(map(float,csvList[4][2:]))
_295cen = list(map(float,csvList[6][2:]))
_332cen = list(map(float,csvList[8][2:]))
_339cen = list(map(float,csvList[10][2:]))
'''
print("\n")
print("current centroids VS 4 dyna_non-Z: 0.75")

print(f"_289cen VS A1_289_1986_1994: {Euclidean(_289cen,A1_289_1986_1994)}")
print(f"_289cen VS A1_289_1995_1999: {Euclidean(_289cen,A1_289_1995_1999)}")
print(f"_289cen VS A1_289_2000_2004: {Euclidean(_289cen,A1_289_2000_2004)}")
print(f"_289cen VS A1_289_2005_2009: {Euclidean(_289cen,A1_289_2005_2009)}")
print(f"_289cen VS A1_289_2010_2015: {Euclidean(_289cen,A1_289_2010_2015)}")

print(f"C_295_1986_1994 VS _295cen: {Euclidean(C_295_1986_1994,_295cen)}")
print(f"C_295_1995_1999 VS _295cen: {Euclidean(C_295_1995_1999,_295cen)}")
print(f"C_295_2000_2004 VS _295cen: {Euclidean(C_295_2000_2004,_295cen)}")
print(f"C_295_2005_2009 VS _295cen: {Euclidean(C_295_2005_2009,_295cen)}")
print(f"C_295_2010_2015 VS _295cen: {Euclidean(C_295_2010_2015,_295cen)}")

print(f"AE_332_1986_1994 VS _332cen: {Euclidean(AE_332_1986_1994,_332cen)}")
print(f"AE_332_1995_1999 VS _332cen: {Euclidean(AE_332_1995_1999,_332cen)}")
print(f"AE_332_2000_2004 VS _332cen: {Euclidean(AE_332_2000_2004,_332cen)}")
print(f"AE_332_2005_2007 VS _332cen: {Euclidean(AE_332_2005_2007,_332cen)}")
print(f"AE_332_2008_2015 VS _332cen: {Euclidean(AE_332_2008_2015,_332cen)}")

print(f"AE_339_1986_1994 VS _339cen: {Euclidean(AE_339_1986_1994,_339cen)}")
print(f"AE_339_1995_1999 VS _339cen: {Euclidean(AE_339_1995_1999,_339cen)}")
print(f"AE_339_2000_2004 VS _339cen: {Euclidean(AE_339_2000_2004,_339cen)}")
print(f"AE_339_2005_2007 VS _339cen: {Euclidean(AE_339_2005_2007,_339cen)}")
print(f"AE_339_2008_2015 VS _339cen: {Euclidean(AE_339_2008_2015,_339cen)}")















