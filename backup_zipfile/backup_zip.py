import zipfile
import datetime
import os


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


# zipfile文件压缩
def backup_zipfile(src_path='', des_path=''):
    # src目录合法
    src_path = os.path.abspath(src_path)
    if not os.path.exists(src_path):
        print('ERROR! ** ' + src_path + ' ** NOT EXIST!!')
        return
    src_name = os.path.basename(src_path)
    src_dir = os.path.dirname(src_path)
    # 目的地址规范化，默认地址是 D:/DataBackup-ZIP
    if des_path == '':
        des_path = r'D:/DataBackup-ZIP'
    des_path = os.path.abspath(des_path)
    des_path = os.path.join(des_path, src_name)
    if not os.path.exists(des_path):
        os.makedirs(des_path)
    des_path = os.path.join(des_path,
                            src_name +
                            datetime.datetime.now().strftime('-%Y-%m-%d-%H-%M-%S') +
                            '.zip')
    # 获取src路径下的所有文件，zipfile需要有所有文件路径
    all_path = get_all_path(src_path)

    print('FILE ** ' + src_path + ' START')
    with zipfile.ZipFile(des_path, 'w', zipfile.ZIP_DEFLATED) as zipfile_example:
        for file_with_path in all_path:
            # 写入时去除根路径，仅保留最顶层文件夹名字
            zipfile_example.write(file_with_path, file_with_path.replace(src_dir, '', 1))
    print('FILE ** ' + src_path + 'FINISH\n')
