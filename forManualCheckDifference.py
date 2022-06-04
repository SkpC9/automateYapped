from tqdm import tqdm
import os
import pandas as pd

base_csv_folder = './base'  # pre extract from Yapped
mod_csv_folder = './mod'  # pre extract from Yapped

for root, dirs, files in os.walk(mod_csv_folder, topdown=False):
    for name in tqdm(files):
        # if name not in ['AtkParam_Npc.csv']:
        #     continue
        tqdm.write("current csv file: " + name)
        # mod_csv = pd.read_csv(os.path.join(mod_csv_folder, name), sep=';', index_col=False, dtype="string").set_index("Row ID")
        mod_csv = pd.read_csv(os.path.join(
            mod_csv_folder, name), sep=';', index_col=False, dtype="string").drop('Row Name', axis=1).set_index('Row ID')
        base_csv = pd.read_csv(os.path.join(
            base_csv_folder, name), sep=';', index_col=False, dtype="string").drop('Row Name', axis=1).set_index('Row ID')
        # sort for easier comparison
        mod_csv.index = mod_csv.index.astype('int')
        base_csv.index = base_csv.index.astype('int')
        mod_csv.sort_index(inplace=True)
        base_csv.sort_index(inplace=True)
        mod_csv['Row Name'] = ''
        mod_csv.insert(loc=0, column='Row Name', value=mod_csv.pop('Row Name'))
        base_csv['Row Name'] = ''
        base_csv.insert(loc=0, column='Row Name',
                        value=base_csv.pop('Row Name'))
        mod_csv.to_csv(os.path.join(mod_csv_folder, name), sep=';', index=True)
        base_csv.to_csv(os.path.join(base_csv_folder, name),
                        sep=';', index=True)
