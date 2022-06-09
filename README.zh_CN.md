# automateYapped

你现在在使用中文

[English_Description](README.md)

## **简介**

用于自动化使用 Yapped 软件合并艾尔登法环的模组（mod）提供的regulation.bin文件。Yapped 用于提取 regulation.bin 和导入 csv 文件。 csv 文件按每一行合并。

此程序使用 [pywinauto](https://github.com/pywinauto/pywinauto) 实现自动化, 使用 [pandas](https://github.com/pandas-dev/pandas/) 来处理 csv 文件

结合 [Vortex](https://www.nexusmods.com/about/vortex/) 和 [ModEngine2](https://github.com/soulsmods/ModEngine2/releases) 使用此程序会更方便

如果模组作者提供csv文件，这个程序可以自动使用 csv 而不是 regulation.bin 来合并他们的 mod ，以减少程序消耗的时间

[介绍视频](https://www.bilibili.com/video/BV1NY4y1577a/)

## **使用说明**

1. 安装 [Yapped-Rune-Bear v2.14](https://github.com/vawser/Yapped-Rune-Bear/releases/tag/2.14)
2. 在Yapped中打开一个regulation.bin文件，以消除错误窗口，这样自动化才能正常工作
3. 从[release](https://github.com/SkpC9/automateYapped/releases)页面下载 automateYapped.exe 文件
4. 打开exe。初次打开将自动创建 ini 配置文件。按照配置文件中的示例根据你的文件路径设置这些值

    * 配置项说明:
        * **'base_regulation_path'** : 艾尔登法环游戏本体提供的 regulation.bin 文件
        * **'base_csv_folder'** : 存储从本体 regulation.bin 中提取出的 csv 文件
        * **'Yapped_folder'** : Yapped-Rune-Bear.exe 所在的文件夹
        * **'Yapped_csv_folder'** : Yapped 提取的 csv 文件会被 Yapped 存放到这个文件夹。默认值应该是 Yapped_folder+'/Projects/ExampleMod/CSV/ER'
        * **'merged_regulation_path'** : 此程序输出的 regulation.bin 文件
        * **'merged_csv_folder'** : 存储此程序运行中产生的 csv 文件
        * **'bin_file_relpath'** : 当前版本未使用，你可以在配置文件中删除这一行
        * **'csv_folder_relpath'** : 当前版本未使用，你可以在配置文件中删除这一行
        * 在 **[mods_info]** 中，各条目按照模组加载顺序排序（目前只能人工决定加载顺序）。每个值一个都是一个字符串 **mod_path**。目前，如果在 mod_path 中检测到csv文件，此程序将自动使用 csv 文件进行合并（csv 文件可以放在 mod_path 内的任何位置，甚至在regulation.bin 文件旁边。但如果有多个csv文件，这些csv文件必须在同一个文件夹中）。 如果 mod_path 中没有 csv 文件，此程序将使用 mod_path 中的 .bin 文件进行合并（可以重命名regulation.bin 文件以避免在 Vortex 中发生文件冲突，注意要保留其扩展名 .bin）。

5. 按照程序的指示操作. 按 Enter 开始，开始后不要触碰键盘和鼠标
6. 一直等到程序提示 all done，然后按 Enter 退出程序
7. 从merged_regulation_path（在ini文件中设置的）获取合并后的 regulation.bin 文件，enjoy！

## guide

A [guide](https://github.com/SkpC9/automateYapped/wiki/guide_for_vortex) for Vortex+Mod Engine 2+Seamless Co-op is added.
