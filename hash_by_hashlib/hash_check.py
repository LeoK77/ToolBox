import hashlib
import os.path
import enum


class HashType(enum.Enum):
    MD5 = 1
    SHA256 = 2
    SHA512 = 3


def hash_check(filename, hash_type=HashType.SHA256):
    # 确定校验类型
    if hash_type == HashType.MD5:
        m = hashlib.md5()
    elif hash_type == HashType.SHA256:
        m = hashlib.sha256()
    elif hash_type == HashType.SHA512:
        m = hashlib.sha512()
    else:
        print("ERROR! Type ** " + str(hash_type) + " ** NOT SUPPORT")
        return
    # 转换绝对路径
    abspath = os.path.abspath(filename)
    # 二进制形式读取文件并更新Hash对象
    with open(abspath, 'rb') as src:
        src_date = src.read(2048)
        while src_date:
            m.update(src_date)
            src_date = src.read(2048)
    # Hash结果
    hash_sum = m.hexdigest()
    hash_result = 'Src: ' + abspath + '\n' \
                  + 'HashType: ' + str(hash_type) + '\n' \
                  + 'HashSum:\n' \
                  + '\t--\t' + hash_sum.lower() + '\n' \
                  + '\t--\t' + hash_sum.upper() + '\n'
    print(hash_result)
    # 写入到 'result.txt' 文件中
    with open('result.txt', 'a', encoding='UTF-8') as result:
        result.write(hash_result)
