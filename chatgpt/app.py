from flask import Flask, request, render_template
import openai

app = Flask(__name__)

# OpenAI API 키 설정
openai.api_key = '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'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']
    
    # ChatGPT에 사용자 입력 전달
    response = openai.Completion.create(
        engine="text-davinci-003",  # 적절한 엔진 선택
        prompt=user_input,
        max_tokens=150  # 원하는 길이로 조절
    )

    bot_reply = response['choices'][0]['text']
    return render_template('index.html', user_input=user_input, bot_reply=bot_reply)

if __name__ == '__main__':
    app.run(debug=True)
