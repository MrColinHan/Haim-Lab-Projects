#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 21:21:14 2018

@author: Han
"""

# This script can combine multiple fasta files into one fasta file and use a 
# couple blank rows to separate each file's content

# Instruction: 
# replace inputDir with the directory of the folder and then run the file
# replace separatorDir with the directory of the separator.fas


import os

inputDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/12.18/16-17 USA/GroupedOutput/"
separatorDir = r"/Users/Han/Documents/Haim Lab(2018 summer)/Haim Lab Projects/Flu/CombineFastaFiles/separator.fas"

############################################################

allFiles = []
def listFiles():
    #for filename in glob.glob(os.path.join(inputDir,'*.fas')):
    count = 0
    if os.path.exists(inputDir+"Output.fas"):# check if there's already an Output.fas in the folder
        print("Output.fas already exists")
        os.remove(inputDir+"Output.fas")
        print("Output.fas is removed")
    else:
        print("No Output.fas")

    for filename in os.listdir(inputDir):
        if filename.endswith('.fas'):
            allFiles.append(filename)
            count = count + 1

    print ("Current number of files in this folder: "+str(count))
    print ("Files: "+str(allFiles))
    print ("\r\n")
        
def separator():
    file = open(separatorDir,"r")
    contents = file.read()
    return (contents)

separ = separator()
    

def createOutput():
    count = 0
    output= open(inputDir+"Output.fas","w+") 
    print("Output.fas is created")
    for filename in allFiles:
        file = open(inputDir+filename,"r")
        if file.mode == "r":
            contents = file.read()
            #for i in contents:
            output.write(contents)
            #output.write("\r\n"+"\r\n"+"\r\n"+"\r\n")
            output.write("\r\n"+ separ + "\r\n" + separ +"\r\n")
            count = count + 1
            #print(contents)
            #print("\r\n")
    print (str(count)+" files have been combined into Output.fas")
    print ("Current number of files in this folder: "+ str(count+1))
    output.close

listFiles()
createOutput()



























































