# 쳇봇엔진 - 의도분류모델
import tensorflow as tf
from tensorflow.keras.models import Model, load_model
from tensorflow.keras import preprocessing

# 의도분류모델모듈
class IntentModel:
    
    def __init__(self, model_name, preprocess):
        
        # 의도클래스별 레이블
        self.labels = {0: '인사', 1: '욕설', 2: '주문', 3: '예약', 4: '기타'}
        
        # 의도분류모델로딩
        self.model = load_model(model_name)
        
        # 챗봇 Preprocess
        self.p = preprocess
    
    # 의도클래스 예측 함수
    def predict_class(self, query):
        
        # 형태소분석
        pos = self.p.pos(query)
        
        # 문장내 키워드 출출(불용어 제거)
        keywords = self.p.get_keywords(pos, without_tag=True)
        sequences = [self.p.get_wordidx_sequence(keywords)]
    
        # 벡터최대크기
        from chatbot.config.GlobalParams import MAX_SEQ_LEN
        
        # 패딩처리
        padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding='post')
        
        predict = self.model.predict(padded_seqs)
        predict_class = tf.math.argmax(predict, axis=1)
        
        return predict_class.numpy()[0]
