import hashlib
import time
import datetime
import urllib.parse as parse
import os


def hash_check(filename: str) -> str:
    m = hashlib.sha256()
    abspath = os.path.abspath(filename)
    with open(abspath, 'rb') as src:
        while True:
            src_data = src.read(2048)
            if not src_data:
                break
            m.update(src_data)
    hash_result = m.hexdigest()
    # 返回hash_sum——全部大写的形式
    return hash_result.upper()


# 获得root_path目录下的所有文件路径
def get_all_path(root_dir_path: str) -> list:
    root_dir_path = os.path.abspath(root_dir_path)
    if not os.path.exists(root_dir_path):
        print('ERROR! ** ' + root_dir_path + ' ** NOT EXIST!!')
        exit(0)
    all_file_path = []
    # 如果是 文件 或者是 空文件夹，直接添加到all_path中
    if os.path.isfile(root_dir_path) or (not os.listdir(root_dir_path)):
        all_file_path.append(root_dir_path)
    else:
        for root, dirs, files in os.walk(root_dir_path):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                if not os.listdir(dir_path):
                    all_file_path.append(dir_path)
            for basename in files:
                all_file_path.append(os.path.join(root, basename))
    return all_file_path


# 返回 abspath_dst ，在源文件名后面加日期
def get_abspath_dst(abspath_src: str) -> str:
    abspath_src = os.path.abspath(abspath_src)
    if not os.path.exists(abspath_src):
        print('ERROR! ** ' + abspath_src + '** NOT  EXIST!')
        exit(0)
    path_without_ext, extended_name = os.path.splitext(abspath_src)
    abspath_dst = path_without_ext + datetime.datetime.now().strftime('-%Y-%m-%d-%H-%M-%S') + extended_name
    return abspath_dst


# 是否用abspath_dst替代abspath_src
# 如果两者hash不一致，则替代，如果hash一致，则不替代
def replace_or_not(abspath_src: str, abspath_dst: str):
    if hash_check(abspath_src) == hash_check(abspath_dst):
        os.remove(abspath_dst)
    else:
        os.replace(abspath_dst, abspath_src)


# 被转义的特殊字符转义回去
def url_escape_to_chinese(filename: str):
    abspath_src = os.path.abspath(filename)
    if not os.path.exists(abspath_src):
        print('ERROR! ** ' + abspath_src + ' ** NOT EXIST!')
        return
    abspath_dst = get_abspath_dst(abspath_src)
    with open(abspath_src, 'r', encoding='utf-8') as src_file:
        with open(abspath_dst, 'w', encoding='utf-8') as dst_file:
            for line_cur in src_file.readlines():
                if line_cur.find('http') != -1:
                    dst_file.write(parse.unquote(line_cur))
                else:
                    dst_file.write(line_cur)
    replace_or_not(abspath_src, abspath_dst)


# 如果hash结果与存储的结果不一致，则更新时间并更新存储库里的hash值
def time_update(filename: str):
    abspath_src = os.path.abspath(filename)
    if not os.path.exists(abspath_src):
        print('ERROR! ** ' + abspath_src + ' ** NOT EXIST!')
        return
    abspath_dst = get_abspath_dst(abspath_src)
    with open(abspath_src, 'r', encoding='utf-8') as src_file:
        with open(abspath_dst, 'w', encoding='utf-8') as dst_file:
            for line_cur in src_file.readlines():
                if line_cur.find('updated:') == 0:
                    line_cur = line_cur.split()[0]
                    line_cur += ' '
                    # 将更新时间设置为此文件的修改时间
                    change_time = os.path.getmtime(abspath_src)
                    change_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(change_time))
                    line_cur += change_time
                    print(abspath_src + '----updated:----' + change_time)
                    line_cur += '\n'
                dst_file.write(line_cur)
    replace_or_not(abspath_src, abspath_dst)


if __name__ == '__main__':
    root_path = r'C:/Users/LeoK77/Documents/WorkSpace/Blog-Hexo-LeoK77/source'
    all_path = get_all_path(root_path)
    hash_record_dict = {}
    hash_record_file = 'hash_record.txt'
    if not os.path.exists(hash_record_file):
        with open(hash_record_file, 'w', encoding='utf-8') as hash_config:
            for article_path in all_path:
                if article_path.find('.md') != -1:
                    hash_config.write(article_path + '------' + hash_check(article_path) + '\n')
        exit(0)
    with open(hash_record_file, 'r', encoding='UTF-8') as hash_record:
        for line in hash_record.readlines():
            # 当且仅当不是空行的时候才是存储hashRecord的行
            if len(line) != 0:
                list_tmp = list(line)
                list_tmp.pop()  # 删除换行符
                record_cur = ''.join(list_tmp).split('------')
                hash_record_dict[record_cur[0]] = record_cur[1]
    # url转义，将%XX形式转义回原来的字符
    for article_path in all_path:
        if article_path.find('.md') != -1:
            url_escape_to_chinese(article_path)
    # 进行hash比较，如果hash结果不匹配，则更改时间并重新hash
    for article_path in all_path:
        if article_path.find('.md') == -1:
            continue
        record_exists = False
        if hash_record_dict.get(article_path, 'no_record') != 'no_record':
            record_exists = True
            if hash_record_dict[article_path] != hash_check(article_path):
                time_update(article_path)
                hash_record_dict[article_path] = hash_check(article_path)
        if not record_exists:
            hash_record_dict[article_path] = hash_check(article_path)
    with open(hash_record_file, 'w', encoding='utf-8') as hash_config:
        for key, val_hash in hash_record_dict.items():
            hash_config.write(key + '------' + val_hash + '\n')
