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

"""
    For Project COVID-19:
        pre-process input before this program: 
            replace all missing value cell as "Null"
            transpose copy the column data into row datasion matrix. 
            
            for dynamic input, if predictor value < its cutoff, set as "Null" because we want to ignore those data
        
        Main purpose of this program is calculating Precision based on confusion matrix
            
            
        this program can do 2 things: 
        1. for static confusion matrix output. 
        
        
        2. for dynamics confusion matrix output
            during pre-process in excel, if value < static cutoff, then become Null. 
        
        how to read output: 
            each row: [sample_number, fisher_pvalue, FPR%, FNR%, TPR%, TNR%, precision]
        
        Note: 
            shouldn't say 'True'. Work 'Actual' is more accurate. 
            
            if < cutoff, then Neg  (but for dyna pred, in each round, if <= then Neg)
            if >= cutoff, then Pos
    
"""

# ==========================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/9.6.20_covid_dyna_confusionMatrix/(NEW)dyna_up_to_90%/"
input_name = "dynamics_input.csv"
output_name = r"Dia(dyna)_Luc<=500.csv"
missing_value = "Null"

dynamics = True  #True: dynamics confusion matrix
end_percent = 90  # Neg group goes up to 70% of the entire sample size

label_row_index = 0  # usually it is always the first row
pred_value_row_index = 1  # row number in csv file that contains true value (index start from 0)
true_value_row_index = 5

# < than cutoff will be Neg
pred_negative_cutoff = 1  # this is static cutoff for predictor (will be ignored in dynamics cal)
true_negative_cutoff = 500

# ==========================================================================================
input_file = working_dir + input_name  # full directory for input file
output_file = working_dir + output_name

input_file_list = []  # store the input csv file
output_list = []  # store value for csv output

# variables for step 1 =====================
pred_values = []
true_values = []  # empty list to store true values read from input file
label_values = []  # this is usually the first row

pred_name = None  # save the name of this predictor (usually first cell of its row)
true_name = None

# variables for step 2 =====================
label_pred_true_dict = {}  # {label_1:(pred_1, true_1), label_2:(pred_2, true_2), ...... }


def read_csv(filedir, listname):
    file = open(filedir)
    reader = csv.reader(file)
    for row in reader:
        listname.append(row)


def write_csv(x,y):  # write list x into file y
    with open(y,'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()


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
    print(f"  sample#, fisherP, FPR%, FNR%, TPR%, TNR%, precision%:"
          f" {[len(true_list), pvalue, FPR, FNR, TPR, TNR, precision]}")
    #print(classification_report(true_list, pred_list))
    return [len(true_list), pvalue, FPR, FNR, TPR, TNR, precision]


def main():
    global pred_values, true_values, input_file_list, label_values, pred_name, true_name, \
        label_pred_true_dict, output_list

    read_csv(input_file, input_file_list)

    # step 1 ========================= import data
    pred_values = input_file_list[pred_value_row_index]  # save the target row for predictor value
    true_values = input_file_list[true_value_row_index]  # save the target row for true value
    label_values = input_file_list[label_row_index]  # save the sample name row for dict keys

    # separate out first cell which contains name of the predictor and true_value
    pred_name = pred_values[0]
    pred_values = pred_values[1:]  # remove first cell
    true_name = true_values[0]
    true_values = true_values[1:]
    label_values = label_values[1:]  # also remove first useless cell for label row
    print(f"step1 -- import data:\n  {pred_name} : {pred_values}\n  {true_name} : {true_values}")

    # step 2 ========================= construct dict
    # construct one dict {label_1:(pred_1, true_1), label_2:(pred_2, true_2), ...... }
    if len(label_values) == len(pred_values) == len(true_values):  # make sure 3 rows have same length
        label_pred_true_dict = dict(zip(label_values, zip(pred_values, true_values)))
    else:
        raise Exception("len(label) != len(predictor) != len(true_value)")
    print(f"\nstep 2  -- construct dict:\n  label-(pred,true)_dict: {label_pred_true_dict}")

    # step 3 ========================= clean dict
    # remove keys contain "Null"
    temp_keys_for_del = []  # temp list for keys will be deleted
    for key in label_pred_true_dict:
        if (label_pred_true_dict[key][0] == missing_value) or (label_pred_true_dict[key][1] == missing_value):
            temp_keys_for_del.append(key)
    for temp_key in temp_keys_for_del:  # now delete those keys
        del label_pred_true_dict[temp_key]
    print(f"\nstep 3 -- clean dict:\n  no-Null_dict:{label_pred_true_dict}")

    # convert "float" or "int" to float
    for key in label_pred_true_dict:
        label_pred_true_dict[key] = (float(label_pred_true_dict[key][0]), float(label_pred_true_dict[key][1]))
    print(f"  float_dict:{label_pred_true_dict}\n")

    # step 4 ========================= static or dynamics analysis
    if not dynamics:  # process static analysis
        static_pred_value = [v1 for (v1, v2) in list(label_pred_true_dict.values())]
        static_true_value = [v2 for (v1, v2) in list(label_pred_true_dict.values())]
        print(f"step 4 -- static analysis:\n"
              f"  static_pred_value:{static_pred_value}\n"
              f"  static_true_value:{static_true_value}\n")
        # convert float to "Pos""Neg" by cut off
        if len(static_pred_value) == len(static_true_value):  # check for length again
            temp_i = 0
            while temp_i < len(static_pred_value):
                if static_pred_value[temp_i] < pred_negative_cutoff:  # cutoff for predictor
                    static_pred_value[temp_i] = "Neg"
                else:
                    static_pred_value[temp_i] = "Pos"
                if static_true_value[temp_i] < true_negative_cutoff:  # cutoff for true value
                    static_true_value[temp_i] = "Neg"
                else:
                    static_true_value[temp_i] = "Pos"
                temp_i += 1  # iterate
            print(f"  cutoff_pred<{pred_negative_cutoff}:\n  {static_pred_value}"
                  f"\n  cutoff_true<{true_negative_cutoff}:\n  {static_true_value}")
        else:
            raise Exception("len(static predictor value) != len(static true value)")

        # compute confusion matrix
        output_list = plot_confusion_matrix(static_true_value, static_pred_value)
        print(f"***csv output row: {output_list}")
        write_csv([[f"predictor:{pred_name}<{pred_negative_cutoff}", f"true:{true_name}<{true_negative_cutoff}"]
                      , ['sample#', 'fisherP', 'FPR%', 'FNR%', 'TPR%', 'TNR%', 'precision%']
                      , output_list]
                  , output_file)

    else:  # process dynamics analysis
        print("step 4 -- sort dict based on predictor:")
        output_list.append(['Predictor'
                               , 'Pred_Neg_#'
                               , 'Pred_Neg_#Rate%'
                               , 'Pred_Neg_cutoff'
                               , 'Actual'
                               , 'Act_Neg_cutoff'
                               , 'all_sample#', 'fisherP', 'FPR%', 'FNR%', 'TPR%', 'TNR%', 'precision%'])
        # sort the 'label_pred_true_dict' into list of tuples [(pred, true, label), ...]
        sorted_p_t_l_list = sorted([(p, t, l) for (l, (p, t)) in label_pred_true_dict.items()])
        print(f"  sortted_p-t-l_list:{sorted_p_t_l_list}")

        print("\nstep 5 -- dynamics analysis:")
        # organize values
        dyna_pred_values = [p for (p, t, l) in sorted_p_t_l_list]
        dyna_true_values = [t for (p, t, l) in sorted_p_t_l_list]
        print(f"  dyna_pred_values:{dyna_pred_values}\n  dyna_true_values:{dyna_true_values}")

        if len(dyna_true_values) != len(dyna_pred_values):  # final check the length
            raise Exception("len(dyna_true_values) != len(dyna_pred_values)")

        all_sample_size = len(dyna_pred_values)  # keep a record
        current_pred_neg_size = 0  # Pred Neg size start from 0 sample
        one_in_all_rate = current_pred_neg_size/all_sample_size*100
        print(f"\n  all sample size: {all_sample_size}, one sample is {one_in_all_rate}%\n")

        while one_in_all_rate <= end_percent:
            if current_pred_neg_size == 0:
                new_pred_negative_cutoff = 0
            else:
                new_pred_negative_cutoff = dyna_pred_values[current_pred_neg_size - 1]  # set a new pred cutoff
            print(f"++++++ current Neg size:{current_pred_neg_size}({one_in_all_rate} <= {end_percent})"
                  f", new_pred_neg_cutoff={new_pred_negative_cutoff}++++++")

            # apply cutoff and convert float to "Neg" "Pos"
            temp_dyna_pred_values = copy.deepcopy(dyna_pred_values)  # now everything works on this deepcopy version
            temp_dyna_true_values = copy.deepcopy(dyna_true_values)
            temp_i = 0
            while temp_i < len(temp_dyna_pred_values):
                if temp_dyna_pred_values[temp_i] <= new_pred_negative_cutoff:  # this needs to be <=
                    temp_dyna_pred_values[temp_i] = "Neg"
                else:
                    temp_dyna_pred_values[temp_i] = "Pos"
                if temp_dyna_true_values[temp_i] < true_negative_cutoff:
                    temp_dyna_true_values[temp_i] = "Neg"
                else:
                    temp_dyna_true_values[temp_i] = "Pos"
                temp_i += 1
            print(f"  dyna_pred_values:{temp_dyna_pred_values}\n  dyna_true_values:{temp_dyna_true_values}")

            # now compute confusion matrix
            output_list.append([pred_name]
                               + [current_pred_neg_size]
                               + [one_in_all_rate]
                               + [f"<={new_pred_negative_cutoff}"]
                               + [true_name]
                               + [f"<{true_negative_cutoff}"]
                               + plot_confusion_matrix(temp_dyna_true_values, temp_dyna_pred_values))

            current_pred_neg_size += 1
            one_in_all_rate = current_pred_neg_size / all_sample_size * 100
        write_csv(output_list, output_file)


main()
