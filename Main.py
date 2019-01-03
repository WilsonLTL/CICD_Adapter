import logging,json
from flask_cors import CORS
from flask import Flask,jsonify,request
import subprocess
app = Flask(__name__)
CORS(app)


@app.route('/',methods=['POST','GET'])
def enter_api_system():
    result = {
        "result": "enter api system"
    }
    return jsonify(result)


@app.route('/update_docker',methods=['POST','GET'])
def update_docker():
    result = {
        "result": "receive, docker container updated"
    }
    try:
        subprocess.call(["./update.sh"])
        return jsonify(result)
    except:
        return jsonify({"result": "fail"})


@app.route('/run_docker', methods=['POST','GET'])
def run_docker():
    result = {
        "result": "receive, docker container is running"
    }
    try:
        subprocess.call(["./run_docker.sh"])
        return jsonify(result)
    except:
        return jsonify({"result": "fail"})



if __name__ == '__main__':
    # app.run(host="127.0.0.1", port=5000)
    app.run(host="0.0.0.0", port=8080)
    # app.run(host="172.31.28.201",port=8080)