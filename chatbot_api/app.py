# chatbot rest api 서버 구현하기
from flask import Flask, request, jsonify, abort, render_template
import socket
import json

# 챗봇엔진서버접속정보
host = "127.0.0.1"  # chatbot api server ip address
port = 5050         # chatbot api server port no

# flask app
app = Flask(__name__)

# ./chatbot_api/templates/hell.html
@app.route('/', methods=["GET"])
def index():
    return render_template("hello.html")
    # return "Hello!!!"
    
# 1) chatbot server와 통신
def get_answer_from_engine(bottype, query):
    # chatbot server와 연결
    mySocket = socket.socket()
    mySocket.connect((host, port))
    
    # chatbot server에 request(query)
    json_data = {
        'Query': query,
        'BotType': bottype
    }
    
    # chatbot server에 query 전송
    message = json.dumps(json_data)
    mySocket.send(message.encode()) 
    
    # chatbot server에서 답변 리턴
    data = mySocket.recv(2048).decode()
    ret_data = json.loads(data)
    
    # chatbot server에 연결된 socket 자원 해제
    mySocket.close()
    
    return ret_data

# 2) chatbot엔진 query 전송 API
# http://localhost:5000/query/TEST
@app.route('/query/<bot_type>', methods=["POST"]) 
def query(bot_type):
    
    body = request.get_json()
    
    try:
        if bot_type == 'TEST':
            # chatbot api test
            ret = get_answer_from_engine(bottype=bot_type, query=body['query'])
            return jsonify(ret)
            
        elif bot_type == "KAKAO": # 카카오톡 skill 처리
            pass
        elif bot_type == "NAVER": # 네이버톡톡 Web Hook 처리
            pass
        else:
            # 정의되지 않은 bot_type인 경우 404 오류 발생
            abort(404)
    except Exception as e:
        # 예외발생시 500 에러 발생
        abort(500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # web server
