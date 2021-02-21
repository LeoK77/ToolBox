from opencc import OpenCC  # opencc开源简繁转换
import os.path


def tradition_to_simple(filename=''):
    # 转换为绝对路径
    abspath_src = os.path.abspath(filename)
    if not os.path.exists(abspath_src):
        print('ERROR! FILE ** ' + abspath_src + ' ** NOT EXIST')
        return
    # 父目录 —— os.path.dirname
    dir_name = os.path.dirname(abspath_src)
    # 文件名 —— os.path.basename
    basename_src = os.path.basename(abspath_src)
    # 将原文件重命名为 _old_basename
    basename_dst = '_old_' + basename_src
    abspath_dst = os.path.join(dir_name, basename_dst)
    os.replace(abspath_src, abspath_dst)
    # src 与 dst 值交换，因为
    string_tmp = abspath_src
    abspath_src = abspath_dst
    abspath_dst = string_tmp
    # 方式是繁体转化为简体
    converter = OpenCC('t2s.json')
    # 逐行转化并写入到目标文件
    with open(abspath_dst, 'w', encoding='UTF-8') as dst:
        with open(abspath_src, 'r', encoding='UTF-8') as src:
            for sentence in src:
                dst.write(converter.convert(sentence))
