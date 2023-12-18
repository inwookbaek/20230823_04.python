# 쳇봇엔진의 NER모델
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model, load_model
from tensorflow.keras import preprocessing

# 개체명 인식 모델 모듈
class NerModel:
    
    # 생성자
    def __init__(self, model_name, preprocess):
        
        # BIO태그클래스별 레이블정의
        self.index_to_ner = {1: 'O', 2: 'B_DT', 3: 'B_FOOD', 4: 'I', 5: 'B_OG', 
                             6: 'B_PS', 7: 'B_LC', 8: 'NNP', 9: 'B_TI', 0: 'PAD',}
        
        # 의도분류모델을 로딩
        self.model = load_model(model_name)

        # 쳇봇 Preprocess객체
        self.p = preprocess
    
    
    # 개체명클래스예측
    def predict(self, query):
        
        # 형태소분석
        pos = self.p.pos(query)
        
        # 문장내 키워드 추출 & 불용어 제거
        keywords = self.p.get_keywords(pos, without_tag=True)
        sequences = [self.p.get_wordidx_sequence(keywords)]
        
        # 패딩처리
        max_len = 40
        padded_seqs = preprocessing.sequence.pad_sequences(sequences, 
                                                           padding='post', value=0, maxlen=max_len)
        
        predict = self.model.predict(np.array([padded_seqs[0]]))
        predict_class = tf.math.argmax(predict, axis=-1)
        
        tags = [self.index_to_ner[i] for i in predict_class.numpy()[0]]
        
        return list(zip(keywords, tags))
        
              
    # 예측된 클래스를 태깅
    def predict_tags(self, query):
        
        # 형태소분석
        pos = self.p.pos(query)
        
        # 문장내 키워드 추출 & 불용어 제거
        keywords = self.p.get_keywords(pos, without_tag=True)
        sequences = [self.p.get_wordidx_sequence(keywords)]
        
         # 패딩처리
        max_len = 40
        padded_seqs = preprocessing.sequence.pad_sequences(sequences, 
                                                           padding='post', value=0, maxlen=max_len)
        
        predict = self.model.predict(np.array([padded_seqs[0]]))
        predict_class = tf.math.argmax(predict, axis=-1)   
        
        tags = []
        for tag_idx in predict_class.numpy()[0]:
            if tag_idx == 1: continue
            tags.append(self.index_to_ner[tag_idx])
            
        if len(tags) == 0: return None
        
        return tags
