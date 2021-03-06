import logging,json
from flask_cors import CORS
from flask import Flask,jsonify,request
from threading import Thread
import subprocess,time
app = Flask(__name__)
CORS(app)

location = "/home/ubuntu/cicd_adapter"


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
        subprocess.call([location+"/update.sh"])
        return jsonify(result)
    except:
        return jsonify({"result": "fail"})


@app.route('/update_code', methods=['POST','GET'])
def update_code():
    result = {
        "result": "receive, system updated"
    }
    try:
        subprocess.call([location+"/update_code.sh"])
        return jsonify(result)
    except Exception as e:
        return jsonify({"result": "fail","exception": str(e)})


@app.route('/run_docker',methods=['POST','GET'])
def run_docker():
    result = {
        "result": "receive, docker container is running"
    }
    try:
        subprocess.call([location+"/run_docker.sh"])
        return jsonify(result)
    except Exception as e:
        print(e)
        return jsonify({"result": "fail:","exception": str(e)})


@app.route('/run_code',methods=['POST','GET'])
def run_code():
    result = {
        "result": "receive, system will restart in 5 second"
    }
    try:
        thread_restart = Thread(target=restart)
        thread_restart.start()
        return jsonify(result)
    except Exception as e:
        print(e)
        return jsonify({"result": "fail:","exception": str(e)})


@app.route("/start_ngrok", methods=['POST'])
def start_ngrok():
    thread_restart = Thread(target=run_ngrok_server)
    thread_restart.start()
    return jsonify({"status":"ngrok kick starting"})


def run_ngrok_server():
    time.sleep(5)
    subprocess.call([location + "/ngrok.sh"])


def restart():
    print("start")
    time.sleep(5)
    subprocess.call([location + "/run_code.sh"])


if __name__ == '__main__':
    # app.run(host="127.0.0.1", port=5000)
    app.run(host="0.0.0.0", port=8080)
    # app.run(host="172.31.28.201",port=8080)