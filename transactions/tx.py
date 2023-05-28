import random,time
import HashUtil

class Transaction(object):
    """ Defines the Ethereum Block model.

    :param int id: the uinque id or the hash of the transaction
    :param int timestamp: the time when the transaction is created. In case of Full technique, this will be array of two value (transaction creation time and receiving time)
    :param int sender: the id of the node that created and sent the transaction
    :param int to: the id of the recipint node
    :param int value: the amount of cryptocurrencies to be sent to the recipint node
    :param int size: the transaction size in MB
    :param int gasLimit: the maximum amount of gas units the transaction can use. It is specified by the submitter of the transaction
    :param int usedGas: the amount of gas used by the transaction after its execution on the EVM
    :param int gasPrice: the amount of cryptocurrencies (in Gwei) the submitter of the transaction is willing to pay per gas unit
    :param float fee: the fee of the transaction (usedGas * gasPrice)
    """

    def __init__(self,
                 id=0,
                 timestamp=0 or [],
                 sender=0,
                 to=0,
                 value=0,
                 size=0.000546,
                 fee=0, signature='', ver=''):
        self.id = id
        self.timestamp = timestamp
        self.sender = sender
        self.to = to
        self.value = value
        self.size = size
        self.fee = fee
        self.signature = signature
    def to_dict(self):
        return {'id': self.id, 'timestamp': self.timestamp,'sender':self.sender,'to':self.to,'value':self.value,'size':self.size,'fee':self.fee}


class LightTransaction():
    pending_transactions = []  # shared pool of pending transactions
    create_time = 0 #创建所需时间
    exe_time = 0 #执行所需时间
    def create_transactions(hashAlg,signAlg):

        LightTransaction.pending_transactions = []
        pool = LightTransaction.pending_transactions
        Psize = 6000
        t1 = time.time()
        for i in range(Psize):
            # assign values for transactions' attributes. You can ignore some attributes if not of an interest, and the default values will then be used
            tx = Transaction()

            # tx.id = random.randrange(100000000000)
            tx.sender = random.randint(0, 2)
            tx.to = random.randint(0, 2)
            tx.size = random.expovariate(1 / 0.000546)
            tx.fee = random.expovariate(1 / 0.000062)

            # hash交易
            hashdata = str(tx.sender) + ',' + str(tx.to) + \
                       ',' + str(tx.size) + ',' + str(tx.fee)
            tx.id = HashUtil.getHash(hashdata, hashAlg)

            tx.signature = HashUtil.sign2(
                tx.sender, hashdata, signAlg)

            pool += [tx]
        t2 = time.time()
        t = t2-t1
        LightTransaction.create_time=t
        random.shuffle(pool)
        return str(t)

    ##### Select and execute a number of transactions to be added in the next block #####

    def execute_transactions(signAlg):

        transactions = []  # prepare a list of transactions to be included in the block
        size = 0  # calculate the total block gaslimit
        count = 0
        blocksize = 1.0
        pool = LightTransaction.pending_transactions

        # sort pending transactions in the pool based on the gasPrice value
        pool = sorted(pool, key=lambda x: x.fee, reverse=True)
        t1 = time.time()
        while count < len(pool):
            # 验证签名
            txObj = pool[count]
            hashdata = str(txObj.sender) + ',' + str(txObj.to) + \
                       ',' + str(txObj.size) + ',' + str(txObj.fee)
            ver = HashUtil.verify2(
                txObj.sender, hashdata, txObj.signature, signAlg)
            if (blocksize >= pool[count].size and ver):
                blocksize -= pool[count].size
                transactions += [pool[count]]
                size += pool[count].size
            count += 1
        t2 = time.time()
        LightTransaction.exe_time = t2-t1
        return transactions, size,LightTransaction.create_time,LightTransaction.exe_time

    