# 쳇봇엔진동작 테스트하기
from chatbot.config.DatabaseConfig import *
from chatbot.utils.Database import Database
from chatbot.utils.Preprocess import Preprocess

# 전처리객체생성
p = Preprocess(word2index_dic="./chatbot/train_tools/dict/chatbot_dict.bin",
               userdic="./chatbot/utils/user_dic.tsv")

# DB객체생성
db = Database(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db_name=DB_NAME)
db.connect()

# 발화자질문
query = '오전에 탕수육 10개 주문합니다'
# query = '화자의 질문의도를 파악합니다'
# query = "안녕하세요"
# query = '자장면 주문할게요!'

# 발화자의 의도파악
from chatbot.models.intent.IntentModel import IntentModel
intent = IntentModel(model_name ='./chatbot/models/intent/intent_model.keras', preprocess=p)
predict = intent.predict_class(query)
intent_name = intent.labels[predict]

# 개체명인식
from chatbot.models.ner.NerModel import NerModel
ner = NerModel(model_name='./chatbot/models/ner/ner_model.keras', preprocess=p)
predicts = ner.predict(query)
ner_tags = ner.predict_tags(query)

# 출력확인
print(f"질문 : {query}")
print(f"의도파악 : {intent_name}")
print(f"개체명인식 : {predicts}")
print(f"답변검색에 필요한 NER태그 = {ner_tags}")
print()

# 답변검색
from chatbot.utils.FindAnswer import FindAnswer

try:
    f = FindAnswer(db)
    # print(f.make_query(intent_name, ner_tags))
    answer_text, answer_image = f.search(intent_name, ner_tags)
    answer = f.tag_to_word(predicts, answer_text)
except:
    answer = "죄송합니다. 무슨 말인지 모르겠습니다!"
    
print(f"답변 = {answer}")

db.close()
