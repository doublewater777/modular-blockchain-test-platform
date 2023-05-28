import json
from flask import Flask,request
from tx import LightTransaction as LT
from HashUtil import genKeys
app = Flask(__name__)

@app.route("/")
def hello_world():
    return 'hello_world!'

@app.route('/createTx')
def create():
    if request.method == 'GET':
        hashAlg = request.args.get('hashAlg')
        signAlg = request.args.get('signAlg')
        time = LT.create_transactions(hashAlg=hashAlg,signAlg=signAlg)
        return time
    
@app.route('/executeTx')
def execute():
    if request.method == 'GET':
        signAlg = request.args.get('signAlg')
        transactions, size,create_time,exe_time = LT.execute_transactions(signAlg=signAlg)
        transaction_dict = [p.to_dict() for p in transactions]
        data = transaction_dict,size,create_time,exe_time
        return json.dumps(data)
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=7777,debug=True)

