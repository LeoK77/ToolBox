import zipfile
import datetime
import os
import path_analysis.path_analysis as path_analysis


# zipfile文件压缩
def backup_total_zip(src_path='', des_path=''):
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
    all_path = path_analysis.get_all_path(src_path)

    print('FILE ** ' + src_path + ' ** START')
    with zipfile.ZipFile(des_path, 'w', zipfile.ZIP_DEFLATED) as zipfile_example:
        for file_with_path in all_path:
            # 写入时去除根路径，仅保留最顶层文件夹名字
            zipfile_example.write(file_with_path, file_with_path.replace(src_dir, '', 1))
    print('FILE ** ' + src_path + ' ** FINISH\n')
