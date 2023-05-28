from flask import Flask, render_template, request,make_response
from flask_cors import CORS
from Main import main
from InputsConfig import InputsConfig as p
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':  # 判断是否是 POST 请求
        # 获取表单数据
        
        hashAlg = request.args.get('hashAlg')  # 传入表单对应输入字段的 hash 值
        signAlg = request.args.get('signAlg')  # 传入表单对应输入字段的 sign 值
        # 保存表单数据到数据库
        print(hashAlg,signAlg)
        eventTime,result = main(hashAlg, signAlg)
        print('result',result)
        totalBlocks = result[0][0]
        trans = result[0][6]
        performance = result[0][10]
        BlockExeTime = result[0][9]
        BlockExeTimeAvg = round(BlockExeTime/totalBlocks,2)
        transThrought = round(trans/performance,2)
        res = [BlockExeTimeAvg,transThrought,performance]
        # res = [237.97, 4.81, 390.2932348251343]
        resp = make_response(json.dumps(res),200)
        
        resp.headers['Access-Control-Allow-Origin'] = '*'
        # print(res,'res')
        return resp
        return render_template('index.html', InputsConfig=p, blocksResults=sta.blocksResults, Profit=sta.profits, Chain=sta.chain)

    # return render_template('index.html', movies=movies,InputsConfig=p,blocksResults=sta.blocksResults,Profit=sta.profits,Chain=sta.chain)
    # return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)

