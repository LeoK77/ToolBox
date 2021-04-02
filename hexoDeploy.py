import hashlib
import time
import datetime
import urllib.parse as parse
import os


def hash_check(filename):
    # hashtype——SHA256
    m = hashlib.sha256()
    # 转换绝对路径
    abspath = os.path.abspath(filename)
    # 二进制形式读取文件并更新Hash对象
    # 限制单次读取文件大小，防止读入文件过大而导致内存出错
    with open(abspath, 'rb') as src:
        src_data = src.read(2048)
        while src_data:
            m.update(src_data)
            src_data = src.read(2048)
    # Hash结果
    hash_sum = m.hexdigest()
    # hash_result = 'Src: ' + abspath + '\n' \
    #               + 'HashType: SHA256\n' \
    #               + 'HashSum:\n' \
    #               + '\t--\t' + hash_sum.lower() + '\n' \
    #               + '\t--\t' + hash_sum.upper() + '\n'
    # print(hash_result)
    # 返回hash_sum——全部大写的形式
    return hash_sum.upper()


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


# 返回 abspath_dst ，在源文件名后面加日期
def get_abspath_dst(abspath_src=''):
    abspath_src = os.path.abspath(abspath_src)
    if not os.path.exists(abspath_src):
        print('ERROR! ** ' + abspath_src + '** NOT  EXIST!')
        exit(0)
    root, ext = os.path.splitext(abspath_src)
    abspath_dst = root + datetime.datetime.now().strftime('-%Y-%m-%d-%H-%M-%S') + ext
    return abspath_dst


# 是否用abspath_dst替代abspath_src
# 如果两者hash不一致，则替代，如果hash一致，则不替代
def replace_or_not(abspath_src='', abspath_dst=''):
    if hash_check(abspath_src) == hash_check(abspath_dst):
        os.remove(abspath_dst)
    else:
        os.replace(abspath_dst, abspath_src)


# 被转义的特殊字符转义回去
def url_escape_to_chinese(filename=''):
    abspath_src = os.path.abspath(filename)
    if not os.path.exists(abspath_src):
        print('ERROR! ** ' + abspath_src + ' ** NOT EXIST!')
        return
    abspath_dst = get_abspath_dst(abspath_src)
    # print(abspath_src)
    # print(abspath_dst)
    with open(abspath_src, 'r', encoding='utf-8') as src_file:
        with open(abspath_dst, 'w', encoding='utf-8') as dst_file:
            for line in src_file.readlines():
                if line.find('http') != -1:
                    dst_file.write(parse.unquote(line))
                else:
                    dst_file.write(line)
    replace_or_not(abspath_src, abspath_dst)


# 检查是否进行了更新
# 如果hash结果与存储的结果不一致，则更新时间并更新存储库里的hash值
def time_update(filename):
    abspath_src = os.path.abspath(filename)
    if not os.path.exists(abspath_src):
        print('ERROR! ** ' + abspath_src + ' ** NOT EXIST!')
        return
    abspath_dst = get_abspath_dst(abspath_src)
    with open(abspath_src, 'r', encoding='utf-8') as src_file:
        with open(abspath_dst, 'w', encoding='utf-8') as dst_file:
            for line in src_file.readlines():
                if line.find('updated:') == 0:
                    line = line.split()[0]
                    line += ' '
                    # 将更新时间设置为此文件的修改时间
                    change_time = os.path.getmtime(path)
                    change_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(change_time))
                    line += change_time
                    print(abspath_src + '----updated:----' + change_time)
                    line += '\n'
                dst_file.write(line)
    replace_or_not(abspath_src, abspath_dst)


if __name__ == '__main__':
    root_path = r'C:/Users/LeoK77/Documents/WorkSpace/Blog-Hexo-LeoK77/source/_posts'
    root_paths = get_all_path(root_path)
    # 读取原本存储的hash信息
    hashRecord = []
    with open('hashConfig.txt', 'r', encoding='UTF-8') as hashConfig:
        for line in hashConfig.readlines():
            # 当且仅当不是空行的时候才是存储hashRecord的行
            if len(line) != 0:
                list_tmp = list(line)
                list_tmp.pop()  # 删除换行符
                hashRecord.append(''.join(list_tmp).split('------'))
    # 如果hashRecord为空，则对hashRecord进行初始化
    if len(hashRecord) == 0:
        for path in root_paths:
            if path.find('.md') == -1:
                break
            hashCheck = hash_check(path)
            record = [path, hashCheck]
            hashRecord.append(record)
    # url转义，将%XX形式转义回中文
    for path in root_paths:
        basename, ext = os.path.splitext(path)
        if ext == '.md':
            url_escape_to_chinese(path)
    # 进行hash比较，如果hash结果不匹配，则更改时间并重新hash
    with open('hashConfig.txt', 'w', encoding='utf-8') as hashConfig:
        for path in root_paths:
            if path.find('.md') == -1:
                break
            # 标志位，如果没有找到这个文件的hashRecord，说明这是一个新文件，需要单独添加到hashRecord里
            flag = False
            hashCheck = hash_check(path)
            for i in range(len(hashRecord)):
                if hashRecord[i][0] == path:
                    flag = True
                    if hashRecord[i][1] != hashCheck:
                        # 哈希值发生了更改，则更新时间并更新哈希值
                        time_update(path)
                        hashRecord[i][1] = hash_check(path)
            if not flag:
                # 增加新文件记录
                time_update(path)
                hashCheck = hash_check(path)
                record = [path, hashCheck]
                hashRecord.append(record)
        for record in hashRecord:
            hashConfig.write(record[0] + '------' + record[1] + '\n')
