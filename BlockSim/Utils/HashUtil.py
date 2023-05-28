
# 首先引入hash库，然后看看hash函数的用法，输入什么，输出什么。
# 根据传入的参数进行选择哪一种hash函数,有SM3，和keccak256+
import pickle
import ecdsa
import hashlib
from gmssl import sm3, func, sm2

from Crypto.Hash import keccak

from Utils.Sm2pair import create_key_pair


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


# 示例交易列表
# transactions = [
#     "tx1",
#     "tx2",
#     "tx3",
#     "tx4",
#     "tx5"
# ]

# # 计算Merkle root
# merkle_root_hash = merkle_root(transactions, 'Keccak')
# print("Merkle root hash:", merkle_root_hash, len(merkle_root_hash))
# sigalt = 'Secp256k1'
# p1, p2 = getPair(sigalt)
# data = '1232'
# sig = sign(p1, p2, data, sigalt)
# print(verify(p1, p2, data, sig, sigalt))


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
        with open(f'Keys/private_key_{i}.pkl', 'wb') as f:
            pickle.dump(private_key, f)

        # 将公钥保存到本地
        with open(f'Keys/public_key_{i}.pkl', 'wb') as f:
            pickle.dump(public_key, f)


def getPriKey(i):
    with open(f'Keys/private_key_{i}.pkl', 'rb') as f:
        return pickle.load(f)


def getPubKey(i):
    with open(f'Keys/public_key_{i}.pkl', 'rb') as f:
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


# genKeys()

# private_key = getPriKey(1)
# public_key = getPubKey(1)
# # # 从本地读取第一个私钥
# # with open('private_key_0.pkl', 'rb') as f:
# #     private_key = pickle.load(f)

# # # 从本地读取第一个公钥
# # with open('public_key_0.pkl', 'rb') as f:
# #     public_key = pickle.load(f)
# # 要签名的消息
# message = "Hello, world!"
# signature = sign2(1, message)
# print(verify2(1, message, signature))
# isValid = verify2(1, '1'+message, signature)
# if isValid:
#     print('Signature is valid')
# else:
#     print('Signature is invalid')
# # 对消息进行签名
# signature = private_key.sign(message)

# # 验证签名
# if public_key.verify(signature, message):
#     print("Signature is valid")
# else:
#     print("Signature is invalid")
# print(getHash('123'))


# def getPair(signAlg):
#     if (signAlg == 'Secp256k1'):
#         return getPair1()
#     elif (signAlg == 'SM2'):
#         return getPair2()


# def sign(private_key, public_key, data, signAlg):
#     if (signAlg == 'Secp256k1'):
#         return sign1(private_key, data)
#     elif (signAlg == 'SM2'):
#         return sign2(private_key, public_key, data)


# def verify(private_key, public_key, data, signature, signAlg):
#     if (signAlg == 'Secp256k1'):
#         return verify1(public_key, data, signature)
#     elif (signAlg == 'SM2'):
#         return verify2(private_key, public_key, data)


# def getPair1():
#     priv = PrivateKey()
#     return priv, priv.pubkey


# def sign1(priKey, msg):
#     sig = priKey.ecdsa_sign(msg.encode('utf-8'))
#     return sig


# def verify1(pubKey, msg, sign):
#     return pubKey.ecdsa_verify(msg.encode('utf-8'), sign)


# pri, pub = getPair()
# print(binascii.hexlify(pri.private_key).decode('utf-8'))
# print(binascii.hexlify(pub.serialize()).decode('utf-8'))
# sig = sign(pri, '123')
# v2 = checkSign(pub, '123', sign=sig)
# print(v2)

# def getPair2():
#     return create_key_pair()


# def sign2(private_key, public_key, data):
#     sm2_crypt = sm2.CryptSM2(private_key, public_key)
#     random_hex_str = func.random_hex(sm2_crypt.para_len)
#     sign = sm2_crypt.sign(data.encode('utf-8'), random_hex_str)  # 16进制
#     return sign


# def verify2(private_key, public_key, data, signature):
#     sm2_crypt = sm2.CryptSM2(private_key, public_key)
#     hash_data = data.encode('utf-8')
#     result = sm2_crypt.verify(signature, hash_data)
#     return result


# pri, pub = generate_key_pair()
# # print(pri, len(pri), pub, len(pub))
# sig = sign2(pri, pub, '123')
# ver = verify2(pri, pub, '123', sig)
# print(ver)
