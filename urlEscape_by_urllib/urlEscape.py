import urllib.parse as parse
import os
import datetime
import hash_by_hashlib.hash_check as hash_check


# 获得root_path目录下的所有文件路径
def get_all_path(root_path='', all_path=None):
    root_path = os.path.abspath(root_path)
    if not os.path.exists(root_path):
        print('ERROR! ** ' + root_path + ' ** NOT EXIST!!')
        exit(0)
    if all_path is None:
        all_path = []
    # 如果是 文件 或者是 空文件夹，直接添加到all_path中
    if os.path.isfile(root_path) or (not os.listdir(root_path)):
        all_path.append(root_path)
    # 如果是 非空文件夹 则遍历添加文件夹内部内容
    else:
        # os.walk的经典用法：对以root_path为根的每个目录进行遍历
        for root, dirs, files in os.walk(root_path):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                # 只将空文件夹填入all_path，非空文件夹会由内部文件路径填入all_path
                if not os.listdir(dir_path):
                    all_path.append(dir_path)
            for basename in files:
                all_path.append(os.path.join(root, basename))
    return all_path


def url_escape_to_chinese(filename=''):
    abspath_src = os.path.abspath(filename)
    if not os.path.exists(abspath_src):
        print('ERROR! ** ' + abspath_src + ' ** NOT EXIST!')
        return

    # 父目录 —— os.path.dirname
    dir_name = os.path.dirname(abspath_src)
    # 文件名 —— os.path.basename
    basename_src = os.path.basename(abspath_src)
    # 将原文件重命名为 _old_basename
    basename_dst, basename_ext = os.path.splitext(basename_src)
    basename_dst += datetime.datetime.now().strftime('-%Y-%m-%d-%H-%M-%S')
    basename_dst += basename_ext
    abspath_dst = os.path.join(dir_name, basename_dst)

    # # src 与 dst 值交换
    # os.replace(abspath_src, abspath_dst)
    # string_tmp = abspath_src
    # abspath_src = abspath_dst
    # abspath_dst = string_tmp

    print(abspath_src)
    print(abspath_dst)

    with open(abspath_src, 'r', encoding='utf-8') as src_file:
        with open(abspath_dst, 'w', encoding='utf-8') as dst_file:
            for line in src_file.readlines():
                if line.find('%'):
                    dst_file.write(parse.unquote(line))
                else:
                    dst_file.write(line)

    if hash_check.hash_check(abspath_src) == hash_check.hash_check(abspath_dst):
        os.remove(abspath_dst)
    else:
        filename, ext = os.path.splitext(abspath_src)
        filename = filename + '_old' + ext
        os.replace(abspath_src, filename)
        os.replace(abspath_dst, abspath_src)
