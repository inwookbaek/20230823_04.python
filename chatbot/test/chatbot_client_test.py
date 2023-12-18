# 챗봇 클라이언트 테스트 프로그램
import socket
import json

# 쳇봇엔진서버접속정보
host = "127.0.0.1"
port = 5050

# 클라이언트프로그램시작
while True:
    
    query = input("질문을 입력하세요 => ") # 질문입력
    print(f"질문 : {query}")
    if(query=='q'): exit(0)
    
    print("-"*60)
    mySocket = socket.socket()
    mySocket.connect((host, port))
    
    # 쳇봇엔진에 질의요청
    json_data = {
        'Query': query,
        'BotType': "myBotService"
    }
    message = json.dumps(json_data)
    mySocket.send(message.encode())
        
    # 쳇봇엔진답변출력
    data = mySocket.recv(2048).decode()
    ret_data = json.loads(data)
    print(f"답변 : {ret_data['Answer']}")
    print(type(ret_data), ret_data)
    
    # 쳇봇엔진서버연결된 소켓 닫기
    mySocket.close()    
