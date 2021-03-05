import urllib.parse as parse
import os
import path_analysis.path_analysis as path_analysis


def url_escape_to_chinese(filename=''):
    abspath_src = os.path.abspath(filename)
    if not os.path.exists(abspath_src):
        print('ERROR! ** ' + abspath_src + ' ** NOT EXIST!')
        return

    abspath_dst = path_analysis.get_abspath_dst(abspath_src)

    print(abspath_src)
    print(abspath_dst)

    with open(abspath_src, 'r', encoding='utf-8') as src_file:
        with open(abspath_dst, 'w', encoding='utf-8') as dst_file:
            for line in src_file.readlines():
                if line.find('%') & line.find('http'):
                    dst_file.write(parse.unquote(line))
                else:
                    dst_file.write(line)

    path_analysis.replace_or_not(abspath_src, abspath_dst)
