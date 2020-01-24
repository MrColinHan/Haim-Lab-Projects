"""
Created on Jan 03 2020

@author: Changze Han
"""

''' Not Finished (no need to use this program so far)'''

from Bio.PDB import *
import nglview as nv

working_dir = r"/Users/Han/Documents/Haim_Lab(2018_summer)/1.3.20_trimer_distance/"
pdb_name = r"5fuu.pdb"
pdb_file = working_dir + pdb_name

download_pdb = PDBList()
download_pdb.retrieve_pdb_file('5fuu')




#parser = PDBParser()
#structure = parser.get_structure('5fuu', pdb_file)

#view = nv.show_biopython(structure)
#view




