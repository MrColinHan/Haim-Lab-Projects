"""
Created on Oct 22 2020

@author: Changze Han
"""

"""
    For Project COVID-19 Sars CoV 2 sequence:
        This program reads a XML file downloaded from NCBI, then map the features to a 
        CSV sequence file which only contains accession number feature
        
        
        Inputs: 
                XML file
                CSV sequence file  (no headers)
        
        Outputs: CSV sequence file with all features
"""
import copy
import csv
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

# Inputs ================================================================================================
working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/10.19.20_sars-2_spike/"
xml_input_name = "A. NCBI features XML.xml"
csv_input_name = "E_AA_Spike_aligned_SARS2_(13768).csv"

csv_output_name = "F_AA(wFeatures)_Spike_aligned_SARS2_(13768).csv"

feature_required = {'INSDInterval_accession', 'organism', 'mol_type'
    , 'isolate', 'host', 'db_xref', 'country', 'collection_date'}
# ========================================================================================================
xml_input_file = working_dir + xml_input_name
csv_input_file = working_dir + csv_input_name
csv_output_file = working_dir + csv_output_name

csv_input_list = []
all_csv_accession = []
accession_feature_dict = {}

output_list = []
output_file = working_dir + csv_output_name


def read_csv(filedir, listname):  # output [len(true_list), pvalue, FPR, FNR, TPR, TNR]
    file = open(filedir)
    reader = csv.reader(file)
    for row in reader:
        listname.append(row)


def write_csv(x, y):  # write list x into file y
    with open(y, 'w+') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(x)
    file.close()


def main():
    global csv_input_list, all_csv_accession, accession_feature_dict, output_list

    read_csv(csv_input_file, csv_input_list)
    print(f"input csv file: {len(csv_input_list)} sequences:")
    for i in csv_input_list[:5]:
        print(i)
    print("\n")

    # generate list of all accession numbers
    for j in csv_input_list:
        all_csv_accession.append(j[0].strip())

    # generate empty dict based on accession numbers
    # {accession:features}
    accession_feature_dict = dict.fromkeys(all_csv_accession, None)
    print(f"loaded empty accession_feature_dict, len: {len(accession_feature_dict)}\n")

    # build XML tree
    xml_tree = ET.parse(xml_input_file)
    print("*********loaded xml_file to tree********")

    # find root node
    xml_root = xml_tree.getroot()
    print("*********found root node of tree********")

    # find all 'INSDSeq'
    all_INSDSeq = xml_root.findall('INSDSeq')

    # go through each sequence
    count_find = 0  # keep track how many accession found in the accession_feature_dict
    for seq in all_INSDSeq:

        # accession number for current sequence
        current_accession = seq.find('INSDSeq_feature-table')\
            .find('INSDFeature')\
            .find('INSDFeature_intervals')\
            .find('INSDInterval')\
            .find('INSDInterval_accession').text

        # check if this accession is in the CSV input sequences
        if current_accession in accession_feature_dict:
            count_find += 1
            print(f"***********{current_accession}***********")

            # initialize empty feature dict with value None
            feature_dict = dict.fromkeys(feature_required, None)

            # add accession
            feature_dict['INSDInterval_accession'] = current_accession

            # find the qualifiers
            current_feature_qualifiers = seq.find('INSDSeq_feature-table')\
                .find('INSDFeature')\
                .find('INSDFeature_quals')\
                .findall('INSDQualifier')

            # go through each qualifier
            for each_q in current_feature_qualifiers:
                # make sure name and value are not None
                if (each_q.find('INSDQualifier_name') is not None) and (each_q.find('INSDQualifier_value') is not None):
                    feature_dict[each_q.find('INSDQualifier_name').text] = each_q.find('INSDQualifier_value').text
                '''
                !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                Potential Bug: 
                'INSDQualifier' section doesnt always contain the features in feature_required
                It could contain less or more. My code took care the case when there's missing
                features because dict was initialized with None value. 
                But when there's more features added in the dict, len of the dict will vary. 
                Not a problem right now because it doesnt affect output. But, need to know this. 
            
                '''


            # add current access's feature_dict to the overall dict
            accession_feature_dict[current_accession] = feature_dict

    # check
    print(f"\nfound {count_find} accessions in the XML\n")

    # who's not found
    print(f"Accession numbers in CSV, but NOT found in XML:")
    for key in accession_feature_dict:
        if accession_feature_dict[key] == None:
            print(key)


    print("\nnow format output file")
    # now append features dict to csv
    # insert features by this order: {'INSDInterval_accession', 'organism', 'mol_type'
    #     , 'isolate', 'host', 'db_xref', 'country', 'collection_date'}
    output_list = copy.deepcopy(csv_input_list)
    for row in output_list:
        if accession_feature_dict[row[0].strip()] is not None:
            row.insert(1, accession_feature_dict[row[0].strip()]['collection_date'])
            row.insert(1, accession_feature_dict[row[0].strip()]['country'])
            row.insert(1, accession_feature_dict[row[0].strip()]['db_xref'])
            row.insert(1, accession_feature_dict[row[0].strip()]['host'])
            row.insert(1, accession_feature_dict[row[0].strip()]['isolate'])
            row.insert(1, accession_feature_dict[row[0].strip()]['mol_type'])
            row.insert(1, accession_feature_dict[row[0].strip()]['organism'])
            row.insert(1, accession_feature_dict[row[0].strip()]['INSDInterval_accession'])
        else:
            row.insert(1, None)
            row.insert(1, None)
            row.insert(1, None)
            row.insert(1, None)
            row.insert(1, None)
            row.insert(1, None)
            row.insert(1, None)
            row.insert(1, None)

    # write output
    write_csv(output_list, csv_output_file)


main()



