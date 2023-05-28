
# 首先引入hash库，然后看看hash函数的用法，输入什么，输出什么。
# 根据传入的参数进行选择哪一种hash函数,有SM3，和keccak256+
import pickle
import ecdsa
from gmssl import sm3, func, sm2

from Crypto.Hash import keccak

from Sm2pair import create_key_pair


def getHash(msg, hashAlg):
    msg = msg.encode('utf-8')
    if (hashAlg == 'Keccak'):

        # 创建 Keccak-256 哈希对象
        hash_object = keccak.new(digest_bits=256)

        # 更新哈希对象的消息
        hash_object.update(msg)

        # 获取哈希值（以字节形式）
        hash_bytes = hash_object.digest()

        # 将字节形式的哈希值转换为十六进制字符串
        hash_hex = hash_bytes.hex()
        return hash_hex
    elif (hashAlg == 'SM3'):
        return sm3.sm3_hash(func.bytes_to_list(msg))





def merkle_root(transactions, hashAlg):
    if len(transactions) == 0:
        return None
    if len(transactions) == 1:
        return transactions[0]

    # 将交易列表按照比特币的排序规则排序
    sorted_transactions = sorted(transactions, key=lambda x: x)

    # 递归地计算左右子树的哈希值
    left_hash = merkle_root(
        sorted_transactions[:len(sorted_transactions)//2], hashAlg)
    right_hash = merkle_root(
        sorted_transactions[len(sorted_transactions)//2:], hashAlg)

    # 将左右子树的哈希值拼接起来，计算新的哈希值
    return getHash(left_hash, hashAlg)+getHash(right_hash, hashAlg)


# 循环生成三个私钥和公钥
def genKeys(signAlg):
    for i in range(3):
        # 生成私钥和公钥
        if (signAlg == 'Secp256k1'):
            private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
            public_key = private_key.get_verifying_key()
        else:
            private_key, public_key = create_key_pair()
        # 将私钥保存到本地
        with open(f'D:\\Coding\\BlockSim\\Keys\\private_key_{i}.pkl', 'wb') as f:
            pickle.dump(private_key, f)

        # 将公钥保存到本地
        with open(f'D:\\Coding\\BlockSim\\Keys\\public_key_{i}.pkl', 'wb') as f:
            pickle.dump(public_key, f)


def getPriKey(i):
    with open(f'D:\\Coding\\BlockSim\\Keys\\private_key_{i}.pkl', 'rb') as f:
        return pickle.load(f)


def getPubKey(i):
    with open(f'D:\\Coding\\BlockSim\\Keys\\public_key_{i}.pkl', 'rb') as f:
        return pickle.load(f)


def sign2(i, msg, signAlg):
    private_key = getPriKey(i)
    public_key = getPubKey(i)
    message = msg.encode('utf-8')
    if (signAlg == 'Secp256k1'):
        signature = private_key.sign(message)
    else:
        sm2_crypt = sm2.CryptSM2(private_key, public_key)
        random_hex_str = func.random_hex(sm2_crypt.para_len)
        signature = sm2_crypt.sign(message, random_hex_str)  # 16进制
    return signature


def verify2(i, msg, signature, signAlg):
    private_key = getPriKey(i)
    public_key = getPubKey(i)
    message = msg.encode('utf-8')
    if (signAlg == 'Secp256k1'):
        try:
            isValid = public_key.verify(signature, message)
            return isValid
        except Exception as err:
            return False
    else:
        sm2_crypt = sm2.CryptSM2(private_key, public_key)
        try:
            isValid = sm2_crypt.verify(signature, message)
            return isValid
        except Exception as err:
            return False

