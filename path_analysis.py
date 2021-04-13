import os.path
import datetime
import hash_check
import shutil


# 获得root_path目录下的所有文件路径
def get_all_path(root_path, all_path=None):
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
def get_abspath_dst(abspath_src):
    abspath_src = os.path.abspath(abspath_src)
    if not os.path.exists(abspath_src):
        print('ERROR! ** ' + abspath_src + '** NOT  EXIST!')
        exit(0)
    root, ext = os.path.splitext(abspath_src)
    abspath_dst = root + datetime.datetime.now().strftime('-%Y-%m-%d-%H-%M-%S') + ext
    return abspath_dst


# 是否用abspath_dst替代abspath_src
# 如果两者hash不一致，则替代，如果hash一致，则不替代
def replace_or_not(abspath_src, abspath_dst):
    if hash_check.hash_check(abspath_src) == hash_check.hash_check(abspath_dst):
        os.remove(abspath_dst)
    else:
        # root, ext = os.path.splitext(abspath_src)
        # os.replace(abspath_src, root + '_old' + ext)
        os.replace(abspath_dst, abspath_src)


def get_all_path_without_root(root_path, depth_root='', all_path=None, git_ignore=True):
    # 这个文件路径获取方法是有目的性的获取去除root_path的文件目录
    # 如果设置git_ignore为False，那么就不会忽视.git文件夹
    root_path = os.path.abspath(root_path)
    if depth_root == '':  # 如果depth设置为空，则默认设置成root_path
        depth_root = root_path
    if not os.path.exists(root_path):
        print('ERROR! ** ' + root_path + ' ** NOT EXIST!!')
        exit(0)
    if all_path is None:
        all_path = []
    # 如果是 文件 或者是 空文件夹，直接添加到all_path中
    # 并去除根目录，即depth_root
    if os.path.isfile(root_path) or (not os.listdir(root_path)):
        if os.path.isfile(root_path):
            all_path.append(root_path.replace(depth_root, ''))
    # 如果是 非空文件夹 则遍历添加文件夹内部内容
    else:
        for sub_dir in os.listdir(root_path):
            # 跳过git文件夹
            if git_ignore and sub_dir == '.git':
                continue
            # 继续遍历这个非空文件夹，depth_root不可设置为空，因为目的是获取所有的去除root_path的文件目录，而不是仅留存文件名
            get_all_path_without_root(os.path.join(root_path, sub_dir), depth_root, all_path)
    return all_path


def copy_files(src_path, dst_path):
    all_path_without_root = get_all_path_without_root(src_path)
    for path in all_path_without_root:
        # print(path.replace(os.path.basename(path), ""))
        dst_path_dir = dst_path + path.replace(os.path.basename(path), "")
        if not os.path.exists(dst_path_dir):
            os.makedirs(dst_path_dir)
        shutil.copy(src_path + path, dst_path_dir)


def get_both_path(root_path, depth_root='', all_path=None, git_ignore=True):
    # 返回一个二元组列表，第一项是全路径，第二项是不带root的路径
    root_path = os.path.abspath(root_path)
    if depth_root == '':  # 如果depth设置为空，则默认设置成root_path
        depth_root = root_path
    if not os.path.exists(root_path):
        print('ERROR! ** ' + root_path + ' ** NOT EXIST!!')
        exit(0)
    if all_path is None:
        all_path = []
    # 如果是 文件 或者是 空文件夹，直接添加到all_path中
    # 并去除根目录，即depth_root
    if os.path.isfile(root_path) or (not os.listdir(root_path)):
        if os.path.isfile(root_path):
            # print(root_path)
            # print(root_path.replace(depth_root, ''))
            # print((root_path, root_path.replace(depth_root, '')))
            # print()
            all_path.append((root_path, root_path.replace(depth_root, '')))
    # 如果是 非空文件夹 则遍历添加文件夹内部内容
    else:
        for sub_dir in os.listdir(root_path):
            # 跳过git文件夹
            if git_ignore and sub_dir == '.git':
                continue
            # 继续遍历这个非空文件夹，depth_root不可设置为空，因为目的是获取所有的去除root_path的文件目录，而不是仅留存文件名
            get_both_path(os.path.join(root_path, sub_dir), depth_root, all_path)
    return all_path
