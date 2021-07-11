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
    abspath = os.path.abspath(filename)
    with open(abspath, 'rb') as src:
        while True:
            src_data = src.read(2048)
            if not src_data:
                break
            m.update(src_data)
    hash_sum = m.hexdigest()
    # hash_result = 'Src: ' + abspath + '\n' \
    #               + 'HashType: ' + str(hash_type) + '\n' \
    #               + 'HashSum:\n' \
    #               + '\t--\t' + hash_sum.lower() + '\n' \
    #               + '\t--\t' + hash_sum.upper() + '\n'
    return hash_sum.upper()
