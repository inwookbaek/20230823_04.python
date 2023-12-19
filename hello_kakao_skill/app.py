# 1. 스킬서버예제(1)
from flask import Flask, request

app = Flask(__name__)

@app.route('/api/sayHello', methods=['GET'])
def hello():
    return "Hello Kakao-Chatbot!!"

# 1) 카카오톡 텍스트형 응답
@app.route('/api/sayHello', methods=['POST'])
def seyHello():
    body = request.get_json()
    # print(body)
    
    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "안녕하세요? 카카오톡 쳇봇!!!!"
                    }
                }
            ]
        }
    }
    
    return responseBody;

# 2) 카카오톡 이미지형 응답
@app.route('/api/showHello', methods=['POST'])
def showHello():
    body = request.get_json()
    # print(body)
    
    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleImage": {
                        "imageUrl": "https://t1.daumcdn.net/friends/prod/category/M001_friends_ryan2.jpg",
                        "altText": "hello I'm Kakao.Chatbot!!"
                    }
                }
            ]
        }
    }
    
    return responseBody;


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # web server
