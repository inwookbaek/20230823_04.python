# 쳇봇엔진 - 의도분류모델 테스트
from chatbot.utils.Preprocess import Preprocess
from chatbot.models.intent.IntentModel import IntentModel

p = Preprocess(word2index_dic="./chatbot/train_tools/dict/chatbot_dict.bin",
               userdic="./chatbot/utils/user_dic.tsv")

intent = IntentModel(model_name='./chatbot/models/intent/intent_model.keras', preprocess=p)

query = '오늘 탕수육 주문 가능한가요?'
predict = intent.predict_class(query)
predict_label = intent.labels[predict]

print(query)
print(f'질의를 예측한 의도클래스 = {predict}')
print(f'질의를 예측한 의도레이블 = {predict_label}')
