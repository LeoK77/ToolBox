import path_analysis
import os

if __name__ == '__main__':
    dirname = r'C:\Users\LeoK77\Downloads\Video\硕鼠-bilibili\王道考研-计算机网络'
    pathList = path_analysis.get_all_path(dirname)
    for i in range(len(pathList)):
        basename = os.path.basename(pathList[i])
        dirname = os.path.dirname(pathList[i])
        basename = basename[4:]
        path = os.path.join(dirname, basename)
        os.replace(pathList[i], path)
        pathList[i] = path
    pathList.sort()
    for i in range(len(pathList)):
        basename = os.path.basename(pathList[i])
        dirname = os.path.dirname(pathList[i])
        numStr = ''
        if i + 1 < 10:
            numStr = '0'
        numStr += str(i + 1)
        basenameList = list(basename)
        basenameList.insert(0, numStr)
        basename = ''.join(basenameList)
        print(basename)
        path = os.path.join(dirname, basename)
        os.replace(pathList[i], path)
