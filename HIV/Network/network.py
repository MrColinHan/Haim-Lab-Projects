"""
Created on Jan 02 2020

@author: Changze Han
"""

import csv
import networkx as nx
import matplotlib.pyplot as plt

'''
    For HIV Project: 
    Network visualization program. 
    Input: csv file contains a two cols of positions and one col of values. (NO 1st Row Headers!!!)
            | 2 | 1 | 0.04|
            | 3 | 1 | 0.9|
            | 4 | 1 | 0.1|
            | 5 | 1 | 0.08|
            ......
            
    Output: circular network graph. 
'''
# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/1.2.20_matlab_network/"
input_csv_name = r"B_Co-vo.csv"
target_position = 332
threshold = 0.001
second_layer = False  # add sub relations 

position_range = (1, 856)
# ========================================================================================================
input_csv_file = working_dir + input_csv_name
first_layer_list = []  # store the position pairs of target position, list of tuples
second_layer_list = []  # list of list of tuples
input_csv_list = []  # store the input csv file


def read_csv(file_dir, list_name):
    file = open(file_dir)
    reader = csv.reader(file)
    for row in reader:
        list_name.append(row)


# use position p to find associated positions that have value <= threshold.
# return a list of position pairs
def find_association(p):
    local_out_list = []
    for row in input_csv_list:  # each csv row
        if int(row[0]) == p:  # check if 1st col position is the target position p
            if float(row[2]) <= threshold:  # check value threshold
                local_out_list.append((row[0], row[1]))  # add this position pair to output list
                # local_out_list.append(row)  # change above line to this line to see the p_value
        if int(row[1]) == p:  # check if 2nd col position is the target position p
            if float(row[2]) <= threshold:
                local_out_list.append((row[1], row[0]))  # add this position pair to output list
                # local_out_list.append(row)  # change above line to this line to see the p_value
    return local_out_list


read_csv(input_csv_file, input_csv_list)
print(f"Input CSV file contains {len(input_csv_list)} rows")

first_layer_list = find_association(target_position)
print(f"{len(first_layer_list)} nodes will be labeled on the circle.")  # test print
print(first_layer_list)  # test print


G = nx.Graph()
G.add_nodes_from(list(range(position_range[0], position_range[1]+1)))  # add a circle of points based on input

G.add_edges_from([(332, 184)])


colors=range(856)
vmin = min(colors)
vmax = max(colors)
cmap=plt.cm.jet
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin = 1, vmax=856))
sm._A = []
plt.colorbar(sm)

all_pos = nx.circular_layout(G)  # all coordinates
nx.draw(G, all_pos, with_labels=False, node_color=range(856), node_size=10, cmap=plt.cm.jet)




pos = {}
for p in all_pos:
    if (p == 332) or (p == 184):
        pos[p] = all_pos[p]

labels = {}
for i in G.nodes:
    if (i == 332) or (i == 184):
        labels[i] = i
#print(all_pos)
print(pos)
print(labels)

nx.draw_networkx_labels(G, pos, labels)



plt.show()

