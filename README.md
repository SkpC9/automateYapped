# automateYapped

You are now in English

[中文介绍](README.zh_CN.md)

## **About**

This is for the automation of merging regulation.bin files from Elden Ring mods. Yapped is used for extracting regulation.bin and importing csv files. Csv files are merged by each row.

This program uses [pywinauto](https://github.com/pywinauto/pywinauto) for automation, and [pandas](https://github.com/pandas-dev/pandas/) for csv processing.

This program is developed with using [Vortex](https://www.nexusmods.com/about/vortex/) and [ModEngine2](https://github.com/soulsmods/ModEngine2/releases) in mind.

If mod authors provide csv files, this program can be configured to merge their mods using csv instead of regulation.bin to reduce the time cost

[Demonstration Video](https://youtu.be/qJuwR3drlrI)

## **Usage**

1. Install [Yapped-Rune-Bear v2.14](https://github.com/vawser/Yapped-Rune-Bear/releases/tag/2.14)
2. Open a regulation.bin file once in Yapped to eliminate error window, for the automation to work
3. Download automateYapped.exe file from [release](https://github.com/SkpC9/automateYapped/releases) page
4. Open the exe. Initial open will auto create ini config file. Follow the example to set those values according to your file paths

    * Config explanations:
        * **'base_regulation_path'** : the regulation.bin file provided by Elden Ring base game.
        * **'base_csv_folder'** : stores csv files extracted from base regulation.bin file.
        * **'Yapped_folder'** : the folder which Yapped-Rune-Bear.exe is in.
        * **'Yapped_csv_folder'** : Yapped extract csv files to this folder. By default it should be Yapped_folder+'/Projects/ExampleMod/CSV/ER'.
        * **'merged_regulation_path'** : the regulation.bin file that this program outputs. No need to manually create one.
        * **'merged_csv_folder'** : stores csv files that this program produces while runing.
        * **'bin_file_relpath'** : mod regulation.bin file relative path from mod path
        * **'csv_folder_relpath'** : mod csv folder relative path from mod path
        * In **[mods_info]** the items are sorted by mod load order(currently have to manually decide the order). Each value contains two strings seperated by '?', first is **mod_path**. Make sure that mod_path+bin_file_relpath is the mod regulation.bin file, and mod_path+csv_folder_relpath is the folder that contains mod csv files(if any). The second one is **mod_flag**. If set to 'bin', it means that mod regulation.bin file will be used for merge. If set to 'csv', it means that mod csv files will be used.

5. Do as the program instructed. Press Enter to start, don't touch keyboard or mouse after start.
6. Wait until it says all done, the press Enter to exit.
7. Get the merged regulation.bin file from merged_regulation_path(set in ini) and enjoy!

## guide

A [guide](https://github.com/SkpC9/automateYapped/wiki/guide_for_vortex) for Vortex+Mod Engine 2+Seamless Co-op is added.
