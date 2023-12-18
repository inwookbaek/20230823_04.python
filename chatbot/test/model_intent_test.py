# NerModel모듈 사용(1)
from chatbot.utils.Preprocess import Preprocess
from chatbot.models.intent.IntentModel import IntentModel

p = Preprocess(word2index_dic="./chatbot/train_tools/dict/chatbot_dict.bin",
               userdic="./chatbot/utils/user_dic.tsv")

ner = NerModel(model_name='./chatbot/models/ner/ner_model.keras', preprocess=p)
query = '오늘 오전 13시 10분에 탕수육을 주문하고 싶어요'
predicts = ner.predict(query)
print(predicts)
