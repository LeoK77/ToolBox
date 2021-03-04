import backup_zipfile.backup_zip as backup_zip
import os

if __name__ == '__main__':
    root_path = r'D:/DataBackup'
    for path in os.listdir(root_path):
        path = os.path.join(root_path, path)
        backup_zip.backup_total_zip(path)
