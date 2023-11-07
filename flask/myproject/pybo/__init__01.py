from flask import Flask

#__name__이라는 변수에 'pybo' 문자열이 저장
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!!!'
