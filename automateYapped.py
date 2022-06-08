# For Yapped-Rune-Bear2.14 regulation.bin merge automation
# steps
# 1. copy base regulation from game to the merged folder then mass export base and merged to get csv files
# 2. open mod regulation and mass export
# 3. merge csv files -- compare each row in a csv
# 4. repeatedly do 2 and 3 by mod load order
# 5. copy merged csv to Yapped csv then mass import then save
# done
# if mod authors provide regulation mods in csv format, merging will be much quicker, since we don't have to mass export mod regulation.bin, which means less csv files when compare and mass import.
# have to manually open a regulation.bin file once in Yapped to eliminate error window for the automation to work

from pywinauto import application
from pywinauto.keyboard import send_keys
from shutil import copyfile
from distutils.dir_util import copy_tree
from tqdm import tqdm
import os
import pandas as pd
import numpy as np
import configparser


def massExport(regulation_path, Yapped_folder):
    app = application.Application(backend="uia")
    app.start(Yapped_folder + "/Yapped-Rune-Bear.exe", work_dir=Yapped_folder)
    # dlg_main = app.window(best_match="Yapped - Rune Bear Edition")
    dlg_main = app.top_window()  # this is more stable

    # dlg_main.menu_select("File -> Open")  # after this line code stuck. why?
    # dlg_main.menu_select("File -> #0") # stuck too
    # this works incredibly well! hail the keyboards!
    # print(app.windows())
    dlg_main.menu_select("File")
    send_keys("{DOWN}{ENTER}")
    # dlg_open = app.top_window()
    # dlg_open.print_control_identifiers()
    # dlg_main['File'].click_input()
    # submenu = app['Dialog']
    # submenu = dlg_main # this also works, so those menu buttons are allocated according to location?
    # submenu['Open'].select() # after this line code stuck. why?
    # print(app.windows())
    # submenu['Open'].click_input()  # this works, but moves mouse
    # print(app.windows())
    # this is actually not needed. dlg_open = dlg_main....
    dlg_open = app['Dialog']

    send_keys("{BACKSPACE}")
    # dlg_open.type_keys('testpath') # error:ElementNotEnabled
    # dlg_open.Edit.set_edit_text(regulation_path) # this works --update actual path contains '/' or '\', this method causes error
    # send_keys(regulation_path) # this works but too slow
    # dlg_open.Edit.type_keys(regulation_path, with_spaces=True)  # this works --update actually not working. keys won't be typed in
    # dlg_open.Edit.send_chars(regulation_path) # no method
    # in Yapped path must use '\' not '/'
    # this works https://stackoverflow.com/questions/48835228/pywinauto-typekeys-not-working
    dlg_open.Edit.type_keys(regulation_path.replace(
        '/', '\\'), with_spaces=True, set_foreground=False)

    send_keys("{ENTER}")  # haven't found another way
    print("start opening regulation.bin")
    # sleep(3)  # for open regulation.bin in case app not responding
    # this is better than time.sleep
    app.Dialog.wait("exists active", timeout=60)
    app.Dialog.Button0.click()
    print("finished opening regulation.bin")
    # dlg_main['Field Data'].click_input()
    # print(app.windows())
    # submenu = app['Dialog'] # didn't work. i know why "Open" work but this don't work, because "Mass Export" is further away from menu bar than open, thus not showing in Dialog window
    # submenu['Mass Export Data'].click_input()
    # dlg_main.menu_select("Field Data -> Mass Export Data") # this works --suddenly didn't work...
    dlg_main.menu_select("Field Data")
    send_keys("{DOWN}{DOWN}{DOWN}{DOWN}{DOWN}{DOWN}{DOWN}{ENTER}")
    # print(app.windows())
    app.Dialog.Button0.click()
    print("start mass export")
    # print(app.windows()) # seems when app not responding, will return []
    # sleep(15)  # for mass export
    app.Dialog.wait('exists active', timeout=60)
    app.Dialog.Button0.click()
    print("finished mass export")
    # app.top_window().Button0.click()
    # app.top_window().Button0.click()

    # send_keys("y", vk_packet=False)

    app.kill()


def mergeExportedCsv(base_csv_folder, merged_csv_folder, mod_csv_folder):
    """src: mod_csv_folder (if mod only provides regulation.bin file, it's Yapped_csv_folder)
    dst: merged_csv_folder

    base_csv_folder is for comparison
    """
    print("start merge csv")
    # this two is for mod compatibility check, currently unused
    files_modified_by_mod = dict()
    RowIDs_modified_in_file = dict()
    for root, _, files in os.walk(mod_csv_folder, topdown=False):
        # delete those not endswith .csv, in case some mod put bin and csv in the same folder
        for name in tqdm([f for f in files if f.endswith(".csv")]):
            tqdm.write("current csv file: " + name)
            # mod_csv = pd.read_csv(os.path.join(mod_csv_folder, name), sep=';', index_col=False, dtype="string").set_index("Row ID")
            # don't know why game regulation.bin have dulplicate RowIDs. can't use that as index for update...
            # have to use the auto generated index... hope row numbers are not changed...
            mod_csv = pd.read_csv(os.path.join(
                mod_csv_folder, name), sep=';', index_col=False, dtype="string").drop('Row Name', axis=1).set_index('Row ID')
            # copy Row ID for comparison
            mod_csv.insert(loc=0, column='RowIDcopy', value=mod_csv.index)
            base_csv = pd.read_csv(os.path.join(
                base_csv_folder, name), sep=';', index_col=False, dtype="string").drop('Row Name', axis=1).set_index('Row ID')
            base_csv.insert(loc=0, column='RowIDcopy',
                            value=base_csv.index)
            merged_csv = pd.read_csv(os.path.join(
                merged_csv_folder, name), sep=';', index_col=False, dtype="string").drop('Row Name', axis=1).set_index('Row ID')
            merged_csv.insert(loc=0, column='RowIDcopy',
                              value=merged_csv.index)
            # sort by index
            mod_csv.index = mod_csv.index.astype('int')
            base_csv.index = base_csv.index.astype('int')
            merged_csv.index = merged_csv.index.astype('int')
            mod_csv.sort_index(inplace=True)
            base_csv.sort_index(inplace=True)
            merged_csv.sort_index(inplace=True)
            # if delete a line in csv, import will cause error in Yapped. So the lines are fixed --actually there are mods that add new rows, so have to use RowID as index....
            # first find rows in mod_csv which are different from base_csv
            # update_csv = mod_csv[~mod_csv.apply(tuple, 1).isin(base_csv.apply(tuple, 1))]  # compare whole row for now -- apply(tuple) too slow for dtype=string, float
            # use those rows to update merged_csv
            # if Row ID dulplicate, add suffix to avoid error when update --not needed if use merge

            compare_csv = mod_csv.reset_index().merge(base_csv, indicator='PandasIndicator', how='left').set_index(
                'Row ID')  # https://stackoverflow.com/questions/11976503/how-to-keep-index-when-using-pandas-merge
            update_csv = compare_csv[np.where(compare_csv['PandasIndicator'] == 'left_only', True, False)].drop(
                'PandasIndicator', axis=1)  # much faster than apply(tuple)

            # currently have to ensure that update_csv doesn't have dulplicates, or the combine_first will give wrong result
            if sum(update_csv.index.duplicated()):
                update_csv = update_csv[update_csv.groupby(
                    level=0).cumcount().le(0)]
            # RowIDs_modified = update_csv.index
            # since there are duplicate RowIDs, can't use count==1 to check mod compatibility
            RowIDs_modified = update_csv.index
            if(not RowIDs_modified.empty):
                RowIDs_modified_in_file[name] = RowIDs_modified
                files_modified_by_mod[name] = 1
                tqdm.write("file modified by mod")
                # actually only update those different from merge
                compare_csv = update_csv.reset_index().merge(
                    merged_csv, indicator='PandasIndicator', how='left').set_index('Row ID')
                num_rows_to_update = sum(
                    np.where(compare_csv['PandasIndicator'] == 'left_only', True, False))
                if not num_rows_to_update == 0:
                    tqdm.write("number of rows to update = " +
                               str(num_rows_to_update))
                # if sum(merged_csv.index.duplicated()):
                #     tqdm.write(name+"duplicated")
                #     base_csv=base_csv[base_csv.groupby(level=0).cumcount().le(0)] # this works for duplicate
                # merged_csv.update(update_csv) # should use merge instead
                # compare_csv=merged_csv.reset_index().merge(update_csv, indicator='PandasIndicator', how='right').set_index('Row ID') # should use combine not merge
                # this combine_first is exactly what i want. no need to worry about duplicates(as long as mod didn't change rows with dulplicate RowIDs).
                merged_csv = update_csv.combine_first(merged_csv)
            # save merged_csv
            # merged_csv.insert(loc=1, column='Row Name', value=['']) # doesn't work
            merged_csv.drop('RowIDcopy', axis=1, inplace=True)
            merged_csv['Row Name'] = ''
            merged_csv.insert(loc=0, column='Row Name',
                              value=merged_csv.pop('Row Name'))
            merged_csv.to_csv(os.path.join(
                merged_csv_folder, name), sep=';', index=True)  # line_terminator=';\n' for manual compare use. be careful, this may shift column of csv.
    print("finished merge csv")
    return files_modified_by_mod, RowIDs_modified_in_file


def massImportAndSave(regulation_path, Yapped_folder):
    app = application.Application(backend="uia")
    app.start(Yapped_folder + "/Yapped-Rune-Bear.exe", work_dir=Yapped_folder)
    dlg_main = app.top_window()
    dlg_main.menu_select("File")
    send_keys("{DOWN}{ENTER}")
    dlg_open = app['Dialog']
    dlg_open.Edit.type_keys(regulation_path.replace(
        '/', '\\'), with_spaces=True, set_foreground=False)
    send_keys("{ENTER}")
    print("start opening regulation.bin")
    # sleep(3)  # for open regulation.bin in case app not responding
    app.Dialog.wait('exists active', timeout=60)
    app.Dialog.Button0.click()
    print("finished opening regulation.bin")
    dlg_main.menu_select("Field Data")
    send_keys("{DOWN}{DOWN}{DOWN}{DOWN}{DOWN}{DOWN}{ENTER}")
    app.Dialog.Button0.click()
    print("start mass import")
    # sleep(15)  # for mass import
    app.Dialog.wait('exists active', timeout=60)
    app.Dialog.Button0.click()
    print("finished mass import")

    # save
    dlg_main.menu_select("File")
    send_keys("{DOWN}{DOWN}{ENTER}")
    app.Dialog.Button0.click()

    app.kill()
    pass


def main():
    # first set config file
    config = configparser.ConfigParser()
    try:
        with open('./automateYapped.ini') as config_file:
            config.read_file(config_file)
            base_regulation_path = config['Paths']['base_regulation_path']
            base_csv_folder = config['Paths']['base_csv_folder']
            Yapped_folder = config['Paths']['Yapped_folder']
            Yapped_csv_folder = config['Paths']['Yapped_csv_folder']
            merged_regulation_path = config['Paths']['merged_regulation_path']
            merged_csv_folder = config['Paths']['merged_csv_folder']
            temp_list = []
            for (index, mod_info) in config.items('mods_info'):
                if mod_info[0]=='(':
                    # v1.1 1.0
                    raise ValueError('invalid ini config')
                if '?' in mod_info:
                    # v1.1.1
                    raise ValueError('invalid ini config')
                temp_list.append(mod_info.strip())
            mods_info = temp_list
    except Exception as e:
        print('no valid ini config found. creating one with default values')
        # default value
        config.clear()
        config['Paths'] = {
            'base_regulation_path': r"E:/SteamLibrary/steamapps/common/ELDEN RING/Game/regulation.bin",
            'base_csv_folder': r"G:/Games/VortexResource/Games/eldenring/tools/Yapped/basecsv/",
            'Yapped_folder': r"G:/Games/VortexResource/Games/eldenring/tools/Yapped/",
            'Yapped_csv_folder': r"G:\Games\VortexResource\Games\eldenring\tools\Yapped\Projects\ExampleMod\CSV\ER",
            'merged_regulation_path': r"G:\Games\VortexResource\Games\eldenring\mods\merged_regulationbin\mod\regulation.bin",
            'merged_csv_folder': r"G:\Games\VortexResource\Games\eldenring\mods\merged_regulationbin\mergedcsv",
        }
        config['mods_info'] = {
            0: r"G:\Games\VortexResource\Games\eldenring\mods\Grand Merchant - Standard - 1.08-129-1-08-1651255230",
            1: r"G:\Games\VortexResource\Games\eldenring\mods\CRAFTING IS FREE-404-v1-1651149952",
        }
        with open('automateYapped.ini', 'w') as config_file:
            config.write(config_file)
        print('Please change the values according to your file locations, then restart program')
        input("Press Enter to exit")
        return

    input("Press Enter to start. (Please don't touch keyboard or mouse after start. wait until all done)")

    # step 1
    # copy file
    copyfile(base_regulation_path, merged_regulation_path)  # may be not needed

    # get base and merged csv
    # base. only need to run this once
    print("start base regulation.bin mass export")
    # massExport(base_regulation_path, Yapped_folder)
    print("finished base mass export")
    print("start copy to base")
    # copy_tree(Yapped_csv_folder, base_csv_folder)
    print("finished copy")

    # merged
    # merged can be directly copied from base to save time
    print("start copy to merged")
    # copy_tree(base_csv_folder, merged_csv_folder)
    print("finished copy")

    # step 2 ~ 4
    # start merging
    print("\nstart merging")
    for mod_index, mod_path in enumerate(mods_info):
        print("mod index = ", mod_index)
        # update automatically find .bin file, no need to spcify rel path
        # if there are csv files, will use csv files first to reduce time
        mod_flag = 'bin'
        mod_csv_folder = ''
        # find csv
        for root, dirs, files in os.walk(mod_path, topdown=False):
            for name in files:
                if name.endswith('.csv'):
                    mod_flag = 'csv'
                    mod_csv_folder = root
                    break
            if not mod_csv_folder=='':
                break

        if mod_flag in ['bin']:
            print("this mod provides regulation.bin")
            # find bin
            regulation_path = ''
            for root, dirs, files in os.walk(mod_path, topdown=False):
                for name in files:
                    if name.endswith('.bin'):
                        regulation_path= os.path.join(root, name)
                        break
                if not regulation_path == '':
                    break
            # for use with Vortex
            # massExport(regulation_path, Yapped_folder)
            # start merge csv
            # mergeExportedCsv(
            #     base_csv_folder, merged_csv_folder, Yapped_csv_folder)
        elif mod_flag in ['csv']:
            print("this mod provides csv file(s)")
            mergeExportedCsv(
                base_csv_folder, merged_csv_folder, mod_csv_folder)
        else:
            pass
        print('--------------')

    print("finished merging")

    # step 5
    # copy
    print("start copy")
    copy_tree(merged_csv_folder, Yapped_csv_folder)
    print("finished copy")

    print("start mass import and save")
    massImportAndSave(merged_regulation_path, Yapped_folder)
    print("finished mass import and save")

    print("all done")
    input("Press Enter to exit")


if __name__ == '__main__':
    main()
