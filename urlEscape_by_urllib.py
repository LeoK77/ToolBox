import urllib.parse as parse
import os
import path_analysis


def url_escape_to_chinese(src_path: str):
    abspath_src = os.path.abspath(src_path)
    if not os.path.exists(abspath_src):
        print('ERROR! ** ' + abspath_src + ' ** NOT EXIST!')
        return
    abspath_dst = path_analysis.get_abspath_dst(abspath_src)
    with open(abspath_src, 'r', encoding='utf-8') as src_file:
        with open(abspath_dst, 'w', encoding='utf-8') as dst_file:
            for line in src_file.readlines():
                if line.find('http') != -1:
                    dst_file.write(parse.unquote(line))
                else:
                    dst_file.write(line)
    path_analysis.replace_or_not(abspath_src, abspath_dst)


if __name__ == '__main__':
    root_dir_path = r'C:/Users/LeoK77/Documents/WorkSpace/Blog-Hexo-LeoK77/source'
    all_path = path_analysis.get_all_path(root_dir_path)
    for article_path in all_path:
        basename, ext = os.path.splitext(article_path)
        if ext == '.md':
            url_escape_to_chinese(article_path)
