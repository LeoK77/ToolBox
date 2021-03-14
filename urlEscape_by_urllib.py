import urllib.parse as parse
import os
import path_analysis


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


if __name__ == '__main__':
    root_path = r'C:/Users/LeoK77/Documents/WorkSpace/Blog-Hexo-LeoK77/source/_posts'
    root_paths = path_analysis.get_all_path(root_path)
    for path in root_paths:
        basename, ext = os.path.splitext(path)
        if ext == '.md':
            url_escape_to_chinese(path)
