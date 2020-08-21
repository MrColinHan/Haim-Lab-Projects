"""
Created on Aug 20 2020

@author: Changze Han
"""

from sklearn.metrics import confusion_matrix, classification_report
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import numpy as np
import csv
import scipy.stats as stats
"""
    For Project COVID-19:
        plot a confusion matrix for two given rows' data (true row and predicted row)
        
        input file: csv, for each value row, first cell should be label. [DiaSorin,	Neg, Pos, Pos, Pos, ...]
        
        outputs: 
            confusion matrix, and precision reports printed in console. 
"""

# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/8.20.20_COVID-19_confusionMatrix/"
input_name = r"csv_input.csv"
output_fig_name = r"BSL3___cbELISA.png"

true_value_row_index = 46  # row number in csv file that contains true value (index start from 0)
pred_value_row_index = 45

true_row_name = "True"   # label for matrix rows, default is True
pred_col_name = "Predicted"  # label for matrix columns, default is Predicted
# ==========================================================================================
input_file = working_dir + input_name  # full directory for input file
output_file = working_dir + output_fig_name

input_file_list = []

true_values = []  # empty list to store true values read from input file
pred_values = []


def read_csv(filedir, listname):
    file = open(filedir)
    reader = csv.reader(file)
    for row in reader:
        listname.append(row)


read_csv(input_file, input_file_list)
true_values = input_file_list[true_value_row_index][1:]  # take out first cell which is the label name
pred_values = input_file_list[pred_value_row_index][1:]
if len(true_values) != len(pred_values):  # check for error
    raise Exception("True value list length != Pred value list length ")

true_row_name = input_file_list[true_value_row_index][0]  # give label to the matrix figure
pred_col_name = input_file_list[pred_value_row_index][0]

# now remove possible "" at the end of list
while '' in true_values:
    true_values.remove("")
while '' in pred_values:
    pred_values.remove("")
if len(true_values) != len(pred_values):  # check for error
    raise Exception("After removing "", True value list length != Pred value list length ")

print(f"True data: {true_row_name}: {true_values}")
print(f"Pred data: {pred_col_name}: {pred_values}")


def plot_confusion_matrix():
    data_matrix = confusion_matrix(true_values, pred_values)
    print(f"\ndata_matrix: {data_matrix}")

    # calculate fisher exact p value:
    oddsratio, pvalue = stats.fisher_exact(data_matrix)
    print(f"\nfisher exact test: {pvalue}")

    # calculate false positive rate and false negative rate
    TN = data_matrix[0, 0]
    FP = data_matrix[0, 1]
    FN = data_matrix[1, 0]
    TP = data_matrix[1 ,1]
    print(f"\nTN, FP, FN, TP:{TN, FP, FN, TP}")
    FPR = FP/(FP+TN)
    FNR = FN/(FN+TP)
    print(f"FPR: {FPR}")
    print(f"FNR: {FNR}")

    # now construct the figure
    data_frame = pd.DataFrame(data_matrix, columns=np.unique(true_values), index=np.unique(true_values))
    data_frame.index.name = true_row_name
    data_frame.columns.name = pred_col_name
    plt.figure(figsize=(10, 7))
    sn.set(font_scale=1.4)
    sn.heatmap(data_frame, cmap="Blues", annot=True, annot_kws={"size": 16})
    plt.savefig(output_file)
    plt.show()


def show_matrix_report():
    print("\nmatrix report: ")
    print(classification_report(true_values, pred_values))


plot_confusion_matrix()

show_matrix_report()
