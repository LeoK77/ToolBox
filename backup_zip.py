import zipfile
import datetime
import os
import path_analysis as path_analysis


def backup_total_zip(src_dir_path: str, des_dir_path='D:/DataBackup-ZIP'):
    src_dir_path = os.path.abspath(src_dir_path)
    if not os.path.exists(src_dir_path):
        print('ERROR! ** ' + src_dir_path + ' ** NOT EXIST!!')
        return
    src_name = os.path.basename(src_dir_path)
    src_dir = os.path.dirname(src_dir_path)
    des_dir_path = os.path.abspath(des_dir_path)
    des_dir_path = os.path.join(des_dir_path, src_name)
    if not os.path.exists(des_dir_path):
        os.makedirs(des_dir_path)
    des_dir_path = os.path.join(des_dir_path,
                                src_name + datetime.datetime.now().strftime('-%Y-%m-%d-%H-%M-%S') + '.zip')
    all_path = path_analysis.get_all_path(src_dir_path)
    print('FILE ** ' + src_dir_path + ' ** START')
    with zipfile.ZipFile(des_dir_path, 'w', zipfile.ZIP_DEFLATED) as zipfile_example:
        for file_with_path in all_path:
            zipfile_example.write(file_with_path, file_with_path.replace(src_dir, '', 1))
    print('FILE ** ' + src_dir_path + ' ** FINISH\n')
