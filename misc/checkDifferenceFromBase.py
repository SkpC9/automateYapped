# auto check what mod edits from base

from pywinauto import application
from pywinauto.keyboard import send_keys
from shutil import copyfile
from distutils.dir_util import copy_tree
from time import sleep
from tqdm import tqdm
import os
import pandas as pd
import numpy as np
from automateYapped import massExport


base_regulation_path = r"E:/SteamLibrary/steamapps/common/ELDEN RING/Game/regulation.bin"  # game original
base_csv_folder = './basecsv'
Yapped_folder = r"G:/Games/VortexResource/Games/eldenring/tools/Yapped/"
Yapped_csv_folder = r"G:\Games\VortexResource\Games\eldenring\tools\Yapped\Projects\ExampleMod\CSV\ER"
mod_path = r"G:\Games\VortexResource\Games\eldenring\mods\Grand Merchant - Standard - 1.08-129-1-08-1651255230"
mod_csv_folder = './modcsv'


massExport(base_regulation_path, Yapped_folder)
copy_tree(Yapped_csv_folder, base_csv_folder)

massExport(os.path.join(mod_path, r"mod\regulation.bin"), Yapped_folder)
copy_tree(Yapped_csv_folder, mod_csv_folder)

files_modified_by_mod = {}
files_with_duplicate_RowID = {}
RowIDs_modified_in_file = {}

for root, dirs, files in os.walk(mod_csv_folder, topdown=False):
    for name in tqdm(files):
        # if name not in ['AtkParam_Npc.csv']:
        #     continue
        tqdm.write("current csv file: " + name)
        mod_csv = pd.read_csv(os.path.join(
            mod_csv_folder, name), sep=';', index_col=False, dtype="string").drop('Row Name', axis=1).set_index('Row ID')
        base_csv = pd.read_csv(os.path.join(
            base_csv_folder, name), sep=';', index_col=False, dtype="string").drop('Row Name', axis=1).set_index('Row ID')
        # mod_csv = pd.read_csv(os.path.join(
        #     mod_csv_folder, name), sep=';', index_col=False, dtype="string").set_index('Row ID')
        # base_csv = pd.read_csv(os.path.join(
        #     base_csv_folder, name), sep=';', index_col=False, dtype="string").set_index('Row ID')
        mod_csv.insert(loc=0, column='RowIDcopy', value=mod_csv.index)
        base_csv.insert(loc=0, column='RowIDcopy', value=base_csv.index)
        compare_csv = mod_csv.reset_index().merge(base_csv, indicator='PandasIndicator', how='left').set_index(
            'Row ID')
        update_csv = compare_csv[np.where(compare_csv['PandasIndicator'] == 'left_only', True, False)].drop(
            'PandasIndicator', axis=1)

        if sum(base_csv.index.duplicated()):
            files_with_duplicate_RowID[name] = 1
        # if name in ['AtkParam_Npc.csv']:
        #     print(update_csv)
        RowIDs_modified = update_csv.index
        # print(RowIDs_modified)
        if(not RowIDs_modified.empty):
            print(RowIDs_modified)
            RowIDs_modified_in_file[name] = RowIDs_modified
            files_modified_by_mod[name] = 1

# print(RowIDs_modified_in_file['AtkParam_Npc.csv'])
print("")
print(files_modified_by_mod)
# print(files_with_duplicate_RowID)
