# 2. 동적으로 변수처리 방법
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello Flask!!'
    # return render_template("hello.html", name="홍길동")

@app.route('/info/<name>') # http://localhost:5000/infor/홍길동
def get_name(name):
    return f"Hello {name}"

@app.route('/user/<int:id>')
def get_user(id):
    return f"User Id = {id}"

# http://127.0.0.1:5000/JSON/1000/자장면 1개 주문할게요
@app.route('/JSON/<int:dest_id>/<message>')
def send_message(dest_id, message):
    json = {
        "bot_id": dest_id,
        "message": message
    }
    return json

if __name__ == '__main__':
    app.run()
