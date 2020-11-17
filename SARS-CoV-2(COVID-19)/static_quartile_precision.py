"""
Created on Sep 6 2020

@author: Changze Han
"""

from sklearn.metrics import confusion_matrix, classification_report
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import numpy as np
import csv
import scipy.stats as stats
import copy
import re
"""
    For Project COVID-19:
        
        input: two lists of values, true list, predict list (copy from csv row)
        
        input data: 11.4.20_quartile_precision/quartile_precision_input.xlsx
        (company negative values already marked as 'Null' in input data)
        
        output: confusion matrix and some measures printed out in the console

"""

# Inputs ================================================================================================
pred_values = "1.739	2.301	2.667	2.817	3.104	3.197	3.681	4.100	5.154	5.305	5.551	5.954	6.374	6.617	8.330	8.593	8.832	8.971	9.835	10.100	10.600	10.697	11.200"
true_values = "81	0	320	160	285	80	129	152	0	150	640	35	413	320	260	160	224	719	200	791	1439	518	1271"

# how to divide into 4 parts, based on these length
quartile_lengths = [5, 6, 6, 6]  # each quartile's length

# < than cutoff will be Neg
true_negative_cutoff = 400
# ========================================================================================================
pred_values = re.sub("\s+", ",", pred_values).split(',')
pred_values = [float(i) for i in pred_values]

true_values = re.sub("\s+", ",", true_values).split(',')
true_values = [float(i) for i in true_values]

# check len
if len(pred_values) != len(true_values):
    raise Exception("ERROR: check length")

# now divide into quartiles
true_values_q1 = true_values[0: quartile_lengths[0]]

true_values_q2 = true_values[quartile_lengths[0]: quartile_lengths[0] + quartile_lengths[1]]

true_values_q3 = true_values[quartile_lengths[0] + quartile_lengths[1]:
                             quartile_lengths[0] + quartile_lengths[1] + quartile_lengths[2]]

true_values_q4 = true_values[quartile_lengths[0] + quartile_lengths[1] + quartile_lengths[2]:]
print(true_values_q1)
print(true_values_q2)
print(true_values_q3)
print(true_values_q4)

all_quartiles = (true_values_q1, true_values_q2, true_values_q3, true_values_q4)


def plot_confusion_matrix(true_list, pred_list):
    data_matrix = confusion_matrix(true_list, pred_list)
    print(f"\n  data_matrix: {data_matrix}")

    # calculate fisher exact p value:
    oddsratio, pvalue = stats.fisher_exact(data_matrix)
    print(f"  fisher exact test: {pvalue}")

    # calculate false positive rate and false negative rate
    TN = data_matrix[0, 0]
    FP = data_matrix[0, 1]
    FN = data_matrix[1, 0]
    TP = data_matrix[1, 1]
    print(f"  TN, FP, FN, TP:{TN, FP, FN, TP}")
    FPR = FP / (FP + TN) * 100
    FNR = FN / (FN + TP) * 100
    TPR = TP / (TP + FN) * 100
    TNR = TN / (TN + FP) * 100
    precision = TP / (TP + FP) * 100
    print(f"  sample#, precision%:"
          f" {[len(true_list), precision]}")
    #print(classification_report(true_list, pred_list))
    #return [len(true_list), FPR, FNR, TPR, TNR, precision]


def main():

    global all_quartiles

    for each in all_quartiles:
        print("\nQuartile: ================================")
        # all pred_values are considered as positive in this experiment
        labeled_pred_values = ['Pos'] * len(each)

        # apply cutoff on true_values
        labeled_true_values = list()
        for i in each:
            if i < true_negative_cutoff:
                labeled_true_values.append('Neg')
            else:
                labeled_true_values.append('Pos')

        print(f"pred labels:  {labeled_pred_values}\ntrue labels:  {labeled_true_values}")

        print(f"\nmatrix results:")
        if labeled_pred_values == labeled_true_values:  # then no need to calculate matrix

            print(f"pred values same as true values, sample number: {len(labeled_true_values)}, precision: 100\n")

        else:
            plot_confusion_matrix(labeled_true_values, labeled_pred_values)



main()