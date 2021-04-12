import path_analysis
import os

if __name__ == '__main__':
    dirname = r'C:\Users\LeoK77\Downloads\Video\硕鼠-bilibili\韩顺平-Linux'
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
    # for i in range(len(pathList)):
    #     path = pathList[i].replace("韩顺平 一周学会Linux", "韩顺平图解Linux")
    #     os.replace(pathList[i], path)
