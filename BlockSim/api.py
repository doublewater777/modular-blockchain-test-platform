import requests


def genTx(hashAlg, signAlg):
    # 根据哈希算法和签名算法生成交易，
    payload = {'hashAlg': hashAlg, 'signAlg': signAlg}
    res = requests.get("http://127.0.0.1:7777/createTx", params=payload)


# def getTx():
#     # 获取交易池


def exeTx(signAlg):
    # 执行交易
    payload = {'signAlg': signAlg}
    res = requests.get("http://127.0.0.1:7777/executeTx", params=payload)
    return res.json()


if __name__ == '__main__':
    genTx('Keccak', 'Secp256k1')
    i, j = exeTx('Secp256k1')
    # i = res[0]
    # j = res[1]
    print(i, 'resi')
    print(j, 'resj')
