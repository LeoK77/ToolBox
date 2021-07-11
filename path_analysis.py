import os.path
import datetime
import hash_check
import shutil


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
    if hash_check.hash_check(abspath_src) == hash_check.hash_check(abspath_dst):
        os.remove(abspath_dst)
    else:
        os.replace(abspath_dst, abspath_src)


class FilePath:
    def __init__(self, full_path: str, root_dir_path: str):
        self.full_path = full_path
        self.root_dir_path = root_dir_path
        self.filepath_without_root_dir = full_path.replace(root_dir_path, '', 1)

    def get_full_path(self) -> str:
        return self.full_path

    def get_root_dir_path(self) -> str:
        return self.root_dir_path

    def get_filepath_without_root_dir(self) -> str:
        return self.filepath_without_root_dir


# 获得root_path目录下的所有文件路径
def get_all_filepath_class(root_dir_path: str, git_dir_ignore=True) -> list:
    root_dir_path = os.path.abspath(root_dir_path)
    if not os.path.exists(root_dir_path):
        print('ERROR! ** ' + root_dir_path + ' ** NOT EXIST!!')
        exit(0)
    all_file_path = []
    if os.path.isfile(root_dir_path):
        return []
    elif os.listdir(root_dir_path):
        for root, dirs, filenames in os.walk(root_dir_path):
            if git_dir_ignore and root.find('.git') != -1:
                continue
            for filename in filenames:
                full_path = os.path.join(root, filename)
                all_file_path.append(FilePath(full_path, root_dir_path))
    return all_file_path


def copy_files(src_path: str, dst_path: str):
    all_filepath = get_all_filepath_class(src_path)
    for filepath in all_filepath:
        filepath_without_root_dir = filepath.get_filepath_without_root_dir()
        dst_path_dir = dst_path + filepath_without_root_dir.replace(
            os.path.basename(filepath_without_root_dir), ""
        )
        if not os.path.exists(dst_path_dir):
            os.makedirs(dst_path_dir)
        shutil.copy(src_path + filepath_without_root_dir, dst_path_dir)
