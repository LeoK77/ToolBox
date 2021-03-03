from opencc import OpenCC  # opencc开源简繁转换
import os.path
import path_analysis.path_analysis as path_analysis


def tradition_to_simple(filename=''):
    # 转换为绝对路径
    abspath_src = os.path.abspath(filename)
    if not os.path.exists(abspath_src):
        print('ERROR! FILE ** ' + abspath_src + ' ** NOT EXIST')
        return

    abspath_dst = path_analysis.get_abspath_dst(abspath_src)

    # 方式是繁体转化为简体
    converter = OpenCC('t2s.json')
    # 逐行转化并写入到目标文件
    with open(abspath_dst, 'w', encoding='UTF-8') as dst:
        with open(abspath_src, 'r', encoding='UTF-8') as src:
            for sentence in src:
                dst.write(converter.convert(sentence))

    path_analysis.replace_or_not(abspath_src, abspath_dst)
