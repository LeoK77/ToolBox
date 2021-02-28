import backup_zipfile.backup_zip as backup_zip
import os

if __name__ == '__main__':
    root_path = r'D:/DataBackup'
    root_paths = os.listdir(root_path)
    for path in root_paths:
        path = os.path.join(root_path, path)
        backup_zip.backup_zipfile(path)
