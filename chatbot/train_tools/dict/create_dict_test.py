# 단어사전테스트
import pickle
from chatbot.utils.Preprocess import Preprocess

# 1. 단어사전로딩
f = open('./chatbot/train_tools/dict/chatbot_dict.bin', 'rb')
word_index = pickle.load(f)
f.close()

sent = "내일 오전 10시에 탕수육 주문하고 싶어 ㅋㅋ"

# 2. 전처리객체생성
p = Preprocess(userdic='../utils/user_dic.tsv')
pos = p.pos(sent)

# 3. 테스트문장을 입력값으로 키워드, index를 출력
keywords = p.get_keywords(pos, without_tag=True)
for word in keywords:
    try:
        print(word, word_index[word])
    except KeyError:
        # 해당단어가 사전에 없는 경우 OOV로 처리
        print(word, word_index['OOV'])
