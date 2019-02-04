import math
import xlrd
import xlsxwriter
import openpyxl
import numpy as np

file_location = "/Users/Han/Documents/Haim Lab(2018 summer)/Edclidean Distance/6.18.18 Coordinates for Changze.xlsx"
workbook = xlrd.open_workbook(file_location)
sheet = workbook.sheet_by_index(0)
col1 = sheet.cell_value(0,0)
col2 = sheet.cell_value(0,1)
col3 = sheet.cell_value(0,2)
col4 = sheet.cell_value(0,3)
nRows = sheet.nrows
nCols = sheet.ncols

def dataInfor():
    print("This file contains " + str(nRows) +
          " rows and " + str(nCols) + " columns. " + "Each column stands for '" +
                           col1 + ", "+ col2 + ", " + col3 + ", " + col4 + "'.")

#get data of row y
def GetRowData(y):
    row = []
    for col in range (nCols):
        row.append(sheet.cell_value((y-1),col))
    return row

#get data of column x
def GetColData(x):
    col = []
    for row in range (nRows):
        col.append(sheet.cell_value(row,(x-1)))
    return col

#get data of a specific posotion(y,x), the yth row and xth column
def GetDataAt(y,x):
    return (sheet.cell_value((y-1),(x-1)))

#set an empty dictionary for positions and their atoms' coordinates
AtomDictionary = {}

#the key of the dictionary are the positions
def positions():
    for row in range(2,nRows):
        if (GetDataAt(row,1)) not in AtomDictionary:
            AtomDictionary [GetDataAt(row,1)] = []
    return AtomDictionary

#updata dictionary with keys and empty values
AtomDictionary = positions()

#match the coordinates of atoms with their positions
def atomsCoord():
    for row in range(2,(nRows+1)):
        AtomDictionary[GetDataAt(row,1)].append(GetRowData(row)[1:])
    return AtomDictionary

#Final dictionary with positions as keys and atoms coordinates as values
AtomDictionary = atomsCoord()
      
#calculate euclidean distance
def EuclideanDistance(p,q):
    return (math.sqrt((q[0]-p[0])**2 + (q[1]-p[1])**2 +(q[2]-p[2])**2))

#calculate the shortest distance between any two positions(a,b)
def shortest(a,b):
    short = 0
    #atom=[]
    for i in AtomDictionary[a]:
        for j in AtomDictionary[b]:
            if short == 0:
                short = EuclideanDistance(i,j)
            if EuclideanDistance(i,j) < short:
                short = EuclideanDistance(i,j)
                #atom=[i,j]
                
    return short

#simple test
z = [1,5,6]
x = [7,9,1]
c = [3.6,7.7,11.3]
v = [9.9,14.2,0]  

def test1():
    return shortest([z,x],[c,v])

#set an empty dictionary for {pisition&position , distance}
distanceDict = {}
#compute all the shortest distance
def allShortest():
    for i in AtomDictionary.keys():
        for j in AtomDictionary.keys():
            if i != j:
                distanceDict[str(i)+"&"+str(j)] = shortest(i,j)
                
    return distanceDict
#final dictionary
#distanceDict = allShortest()################step 2#####################


test2 = { '519.0&321.0': 61.93898199034272,
 '519.0&321A': 63.05187085249731,
 '519.0&322.0': 61.9261400218034,
 '519.0&323.0': 61.79635307200579,
 '519.0&324.0': 63.94307358111588,
 '519.0&325.0': 62.1929198783913,
 '519.0&326.0': 62.72302162683172,
 '519.0&327.0': 57.166410531010264,
 '519.0&328.0': 56.543810244800454,
 '519.0&329.0': 53.46807401618278,
 '519.0&330.0': 50.662671672544086,
 '519.0&331.0': 47.89482646382592,
 '519.0&332.0': 46.69481592211281,
 '519.0&333.0': 45.80362607916539,
 '519.0&334.0': 44.77948586127358,
 '519.0&335.0': 48.13371434867665,
 '519.0&336.0': 45.51842977300514,
 '519.0&337.0': 41.6477135146697,}


#convert dictionary to list
def DictToList(a):
    result = []
    for i in a:
        #if result = []:
            result.append([i,a[i]])
    return result

#convert distance dictionary to list#########################################
#distanceList = DictToList(distanceDict)

test3 = DictToList(test2)     

#mergesort
def merge(a,b):
    """ Function to merge two arrays """
    c = []
    while len(a) != 0 and len(b) != 0:
        if a[0] < b[0]:
            c.append(a[0])
            a.remove(a[0])
        else:
            c.append(b[0])
            b.remove(b[0])
    if len(a) == 0:
        c += b
    else:
        c += a
    return c


def mergesort(x):
    """ Function to sort an array using merge sort algorithm """
    if len(x) == 0 or len(x) == 1:
        return x
    else:
        middle = round(len(x)/2)
        a = mergesort(x[:middle])
        b = mergesort(x[middle:])
        return merge(a,b)

#sort distance
def SortDistance(a):
    secondHalf = []    
    for i in a:
        secondHalf.append(i[1])
    return mergesort(secondHalf)

#match the positions with sorted distance
def finalSortResult(a):
    result = []
    secondHalf = SortDistance(a)
    for i in secondHalf:
        for j in a:
            if i == j[1]:
                result.append(j)
    return result

#Sorted:

#def Sorted():
    #return finalSortResult(distanceList)

# convert into a matrix
test4 = { 500.0: [[-267.61, -129.697, 44.94],
  [-266.879, -129.805, 46.199],
  [-266.38, -131.228, 46.456],
  [-266.593, -131.787, 47.531],
  [-267.754, -129.329, 47.365],
  [-269.141, -129.958, 47.427],
  [-269.912, -129.459, 48.641],
  [-271.191, -130.144, 48.805],
  [-272.334, -129.732, 48.267],
  [-272.362, -128.634, 47.524],
  [-273.451, -130.418, 48.47]],
 501.0: [[-265.701, -131.803, 45.468],
  [-265.191, -133.166, 45.574],
  [-263.683, -133.226, 45.349],
  [-263.177, -132.739, 44.338],
  [-265.905, -134.08, 44.575],
  [-265.304, -135.786, 44.556]],
 502.0: [[-262.973, -133.831, 46.296],
  [-261.524, -133.977, 46.205],
  [-261.13, -135.446, 46.354],
  [-261.805, -136.207, 47.047],
  [-260.832, -133.124, 47.271],
  [-259.314, -133.08, 47.164],
  [-258.697, -132.32, 48.327],
  [-257.179, -132.339, 48.258],
  [-256.561, -131.645, 49.422]],
 503.0: [[-260.042, -135.842, 45.7],
  [-259.579, -137.225, 45.764],
  [-258.803, -137.528, 47.042],
  [-258.891, -136.799, 48.029],
  [-258.712, -137.556, 44.55],
  [-259.473, -138.183, 43.398],
  [-258.518, -138.768, 42.375],
  [-257.741, -137.732, 41.702],
  [-256.701, -137.977, 40.912],
  [-256.308, -139.226, 40.704],
  [-256.051, -136.975, 40.337]],
 504.0: [[-258.04, -138.616, 47.005],
  [-257.277, -139.073, 48.16],
  [-255.85, -138.532, 48.147],
  [-255.507, -137.676, 47.332],
  [-257.26, -140.602, 48.204],
  [-258.636, -141.227, 48.372],
  [-258.676, -142.642, 47.819],
  [-258.556, -142.659, 46.363],
  [-259.588, -142.604, 45.527],
  [-260.825, -142.528, 46.001],
  [-259.386, -142.624, 44.217]],
 505.0: [[-255.023, -139.039, 49.056],
  [-253.632, -138.612, 49.152],
  [-252.68, -139.747, 48.79],
  [-252.897, -140.898, 49.169],
  [-253.294, -138.103, 50.568],
  [-251.808, -137.796, 50.682],
  [-254.128, -136.876, 50.903]]}

#use matrix(AtomDictionary) to build the matrix
def matrix(x):
    result = []
    for i in x.keys():
        insideList = []
        result.append(insideList)
        insideList.append(i)
        for j in x.keys():
            insideList.append(str(i)+"&"+str(j)+": "+str(shortest(i,j)))
    return result


#write into excel

data = matrix(AtomDictionary)
#q = {9:0,8:0,7:0,6:0,5:0,4:0,3:0}
#z=[[0,1,2,3,4,5,6],[7,6,5,4,3,2,1],[9,8,7,6,5,4,3]]
def addFirstRow():
    row=["Euclidean"]
    for i in AtomDictionary.keys():
        row.append(i)
    data.insert(0,row)
    return data

MatrixData = addFirstRow()

wb = openpyxl.Workbook()
sheet = wb.get_active_sheet()
sheet.title='Sheet #1'
 
#Generate data


#z.insert(0,[6,6,6,6,6,6,6])


#Loop to set the value of each cell
for i in range(len(MatrixData)):
    for j in range(len(MatrixData[i])):
        #print(data[i][j])
        sheet.cell(row=i+1, column=j+1).value=MatrixData[i][j]
    
#wb.save('testInsert.xlsx')
wb.save('Euclidean Matrix.xlsx')


