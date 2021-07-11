from opencc import OpenCC  # OpenCC开源简繁转换
import os.path
import path_analysis


def tradition_to_simple(src_path: str):
    abspath_src = os.path.abspath(src_path)
    if not os.path.exists(abspath_src):
        print('ERROR! FILE ** ' + abspath_src + ' ** NOT EXIST')
        return
    abspath_dst = path_analysis.get_abspath_dst(abspath_src)
    # 方式是繁体转化为简体
    converter = OpenCC('t2s.json')
    with open(abspath_dst, 'w', encoding='UTF-8') as dst:
        with open(abspath_src, 'r', encoding='UTF-8') as src:
            for sentence in src:
                dst.write(converter.convert(sentence))
    path_analysis.replace_or_not(abspath_src, abspath_dst)


if __name__ == '__main__':
    tradition_to_simple(
        r'C:\Users\LeoK77\Documents\WorkSpace\Blog-Hexo-LeoK77\node_modules\hexo-theme-butterfly\_config.yml'
    )
