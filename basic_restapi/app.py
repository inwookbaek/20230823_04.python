# 3. 기본적인 Rest Api 서버 구현하기
from flask import Flask, request, jsonify

app = Flask(__name__)

# 서버리소스
resource = []

# 1) 사용자정보조회
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    
    for user in resource:
        if user['user_id'] is user_id:
            return jsonify(user)
        
    return jsonify(None)
    
# 2) 사용자추가
@app.route('/user', methods=['POST'])
def add_user():
    user = request.get_json()
    resource.append(user)
    return jsonify(resource)
    
if __name__ == '__main__':
    app.run()
