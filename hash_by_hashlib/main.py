import hash_by_hashlib.hash_check as hash_check

if __name__ == '__main__':
    # 待校验的文件列表
    filenames = [
        r'C:\Users\LeoK77\Documents\WorkSpace\Blog-Hexo-LeoK77\node_modules\hexo-theme-butterfly\_config.yml'
    ]
    # 校验类型
    hash_type = hash_check.HashType.SHA256
    # 清空上次的校验内容
    with open(r'result.txt', 'w') as dst:
        pass
    # Hash结果打印在终端，并储存在文件“result.txt”中
    for filename in filenames:
        hash_check.hash_check(filename, hash_type)
